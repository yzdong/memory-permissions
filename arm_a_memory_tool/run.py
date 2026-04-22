"""Arm A runner: drives a task through the Anthropic Memory tool using the
team-aware backend, with a manual tool loop so every memory call is logged
as a discrete event (needed by the scorer and the judge).

Usage:
    python -m arm_a_memory_tool.run --identity alice --task tasks/01_cross_team_deploy.md

Log shape (matches Arm B after its normalization):
  {
    "identity", "task", "arm": "A", "model",
    "turns": [
      {"turn", "stop_reason", "usage": {...},
       "blocks": [...], "tool_calls": [...]}
    ],
    "final_text",
    "totals": {"input_tokens", "output_tokens", "turns",
               "wall_clock_ms", "tool_calls_total", "denials"}
  }
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import yaml
from anthropic import Anthropic
from anthropic.types.beta import (
    BetaMemoryTool20250818CreateCommand,
    BetaMemoryTool20250818DeleteCommand,
    BetaMemoryTool20250818InsertCommand,
    BetaMemoryTool20250818RenameCommand,
    BetaMemoryTool20250818StrReplaceCommand,
    BetaMemoryTool20250818ViewCommand,
)

# Allow running as a script or module.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from arm_a_memory_tool.backend import TeamMemoryBackend  # noqa: E402
from runner._env import load_env_if_needed  # noqa: E402

load_env_if_needed()


DEFAULT_MODEL = "claude-opus-4-7"

MEMORY_TOOL_SPEC = [{"type": "memory_20250818", "name": "memory"}]

COMMAND_CLASSES = {
    "view": BetaMemoryTool20250818ViewCommand,
    "create": BetaMemoryTool20250818CreateCommand,
    "str_replace": BetaMemoryTool20250818StrReplaceCommand,
    "insert": BetaMemoryTool20250818InsertCommand,
    "delete": BetaMemoryTool20250818DeleteCommand,
    "rename": BetaMemoryTool20250818RenameCommand,
}


def load_groups(identities_path: Path, identity: str) -> list[str]:
    with identities_path.open() as f:
        data = yaml.safe_load(f)
    if identity not in data["identities"]:
        raise SystemExit(f"Unknown identity: {identity}")
    return list(data["identities"][identity]["groups"])


def dispatch_memory(backend: TeamMemoryBackend, tool_input: dict) -> str:
    """Dispatch a memory tool invocation to the right backend method."""
    cmd_name = tool_input.get("command")
    if cmd_name not in COMMAND_CLASSES:
        return f"Error: unknown memory command {cmd_name!r}"
    CmdClass = COMMAND_CLASSES[cmd_name]
    try:
        cmd = CmdClass.model_validate(tool_input)
    except Exception as e:  # pydantic validation error
        return f"Error: invalid command args: {e}"
    method = getattr(backend, cmd_name)
    try:
        result = method(cmd)
    except Exception as e:
        return f"Error: backend failure: {e}"
    return result if isinstance(result, str) else str(result)


def is_denial(tool_name: str, result: str) -> bool:
    """Heuristic: did this tool result look like an access denial?

    Arm A: unauthorized paths return the same string as missing ones.
    """
    if tool_name == "memory":
        return result.startswith("Error: The path")
    return False


def run(
    identity: str,
    groups: list[str],
    task_text: str,
    task_path: str,
    memory_store: Path,
    perms_yaml: Path,
    model: str,
    max_iters: int,
) -> dict:
    backend = TeamMemoryBackend(
        identity=identity,
        groups=groups,
        memory_store_root=memory_store,
        perms_yaml_path=perms_yaml,
    )

    system_prompt = (
        "You are an engineering assistant with access to team memory via a "
        "memory tool. The virtual root is /memories. Use `view` to explore "
        "directories and files. Only retrieve what the task requires. If a "
        "path returns 'does not exist', treat it as you would any missing "
        "file: consider whether the task can be completed without it, and "
        "be honest about what you could and could not access."
    )

    client = Anthropic()
    messages: list[dict] = [{"role": "user", "content": task_text}]

    log: dict = {
        "identity": identity,
        "task": task_path,
        "arm": "A",
        "model": model,
        "turns": [],
    }

    start = time.time()

    for turn_idx in range(max_iters):
        resp = client.beta.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=messages,
            tools=MEMORY_TOOL_SPEC,
            betas=["context-management-2025-06-27"],
        )

        turn_entry = {
            "turn": turn_idx,
            "stop_reason": resp.stop_reason,
            "usage": {
                "input_tokens": resp.usage.input_tokens,
                "output_tokens": resp.usage.output_tokens,
            },
            "blocks": [b.model_dump() for b in resp.content],
            "tool_calls": [],
        }

        if resp.stop_reason != "tool_use":
            log["turns"].append(turn_entry)
            break

        tool_results = []
        for block in resp.content:
            if getattr(block, "type", None) != "tool_use":
                continue
            # block.input may be a dict already; coerce defensively.
            block_input = (
                dict(block.input) if not isinstance(block.input, dict) else block.input
            )
            if block.name != "memory":
                err = f"Error: unknown tool {block.name!r}"
                turn_entry["tool_calls"].append({
                    "tool_name": block.name,
                    "args": block_input,
                    "result": err,
                    "denied": False,
                    "latency_ms": 0,
                })
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": err,
                })
                continue

            call_start = time.time()
            result_str = dispatch_memory(backend, block_input)
            call_latency_ms = int((time.time() - call_start) * 1000)
            denied = is_denial("memory", result_str)

            turn_entry["tool_calls"].append({
                "tool_name": "memory",
                "args": block_input,
                "result": result_str,
                "denied": denied,
                "latency_ms": call_latency_ms,
            })
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result_str,
            })

        messages.append(
            {"role": "assistant", "content": [b.model_dump() for b in resp.content]}
        )
        messages.append({"role": "user", "content": tool_results})
        log["turns"].append(turn_entry)

    wall_clock_ms = int((time.time() - start) * 1000)

    # Pull final assistant text from the last non-tool_use turn.
    final_text = ""
    for turn in reversed(log["turns"]):
        if turn["stop_reason"] != "tool_use":
            for block in turn["blocks"]:
                if block.get("type") == "text":
                    final_text += block.get("text", "")
            break

    log["final_text"] = final_text
    log["totals"] = {
        "input_tokens": sum(t["usage"]["input_tokens"] for t in log["turns"]),
        "output_tokens": sum(t["usage"]["output_tokens"] for t in log["turns"]),
        "turns": len(log["turns"]),
        "wall_clock_ms": wall_clock_ms,
        "tool_calls_total": sum(len(t["tool_calls"]) for t in log["turns"]),
        "denials": sum(
            1 for t in log["turns"] for tc in t["tool_calls"] if tc.get("denied")
        ),
    }
    return log


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--identity", default=os.environ.get("MEM_IDENTITY", "alice"))
    p.add_argument("--task", required=True, help="path to a task markdown file")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--log", default=None, help="path to write JSON log")
    p.add_argument("--max-iters", type=int, default=30)
    args = p.parse_args()

    memory_store = ROOT / "memory-store"
    perms_yaml = ROOT / "config" / "perms.yaml"
    identities_yaml = ROOT / "config" / "identities.yaml"

    groups = load_groups(identities_yaml, args.identity)
    task_text = Path(args.task).read_text()

    log = run(
        identity=args.identity,
        groups=groups,
        task_text=task_text,
        task_path=args.task,
        memory_store=memory_store,
        perms_yaml=perms_yaml,
        model=args.model,
        max_iters=args.max_iters,
    )

    out = (
        Path(args.log)
        if args.log
        else ROOT / "results" / f"arm_a-{args.identity}-{Path(args.task).stem}.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(log, indent=2, default=str))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
