"""Orchestrator: run every (task × arm × identity × repeat) cell, log each,
then score the batch.

Defaults to alice / bob / carol / dana across both arms and all four tasks.
Override with --arms, --identities, --tasks, --repeats.

After runs complete, invokes runner.scorer.score_all to produce per-run
.score.json files and (with --summary) an aggregate table.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TASKS = [
    "tasks/01_cross_team_deploy.md",
    "tasks/02_team_specific_override.md",
    "tasks/03_unauthorized_lure.md",
    "tasks/04_ambiguous_retrieval.md",
]
ARMS = ["arm_a_memory_tool", "arm_b_filesystem"]
IDENTITIES = ["alice", "bob", "carol", "dana"]

# When USE_RUNUSER=1 is set (e.g. in the Docker container), Arm B subprocesses
# are launched under the target OS user via `runuser -u <identity> --`. This
# makes filesystem enforcement real (Arm B enforces via the kernel, which
# depends on the process's effective uid/gid). Arm A enforces in application
# code regardless of uid, so we do not wrap it.
USE_RUNUSER = os.environ.get("USE_RUNUSER") == "1"


def run_cell(
    arm: str, identity: str, task: str, repeat: int, results_dir: Path
) -> Path:
    """Run a single experiment cell; return the log path."""
    task_stem = Path(task).stem
    log_path = results_dir / arm / identity / f"{task_stem}__run{repeat:02d}.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    cmd: list[str] = [
        sys.executable,
        "-m",
        f"{arm}.run",
        "--identity",
        identity,
        "--task",
        str(ROOT / task),
        "--log",
        str(log_path),
    ]
    if USE_RUNUSER and arm == "arm_b_filesystem":
        runuser = shutil.which("runuser")
        if runuser is None:
            print("    ! USE_RUNUSER=1 set but runuser not found; continuing as-is")
        else:
            cmd = [runuser, "-u", identity, "--"] + cmd
    print(f"  [run] {arm} / {identity} / {task_stem} / r{repeat:02d}")
    # TODO: parallelize safely (watch out for rate limits)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    ! subprocess failed (code {result.returncode})")
        if result.stderr:
            print(result.stderr.rstrip())
    return log_path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--results-dir", default=str(ROOT / "results"))
    p.add_argument("--arms", nargs="*", default=ARMS)
    p.add_argument("--identities", nargs="*", default=IDENTITIES)
    p.add_argument("--tasks", nargs="*", default=TASKS)
    p.add_argument("--repeats", type=int, default=3,
                   help="runs per (task × arm × identity) cell")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-scoring", action="store_true",
                   help="run the agents but skip scorer.score_all")
    p.add_argument("--skip-judge", action="store_true",
                   help="score with rule-based only (disable LLM judge pass)")
    p.add_argument("--summary", action="store_true",
                   help="print aggregate summary to stdout at the end")
    args = p.parse_args()

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    cells = [
        (a, i, t, r)
        for a in args.arms
        for i in args.identities
        for t in args.tasks
        for r in range(1, args.repeats + 1)
    ]

    print(f"Matrix: {len(cells)} cells -> {results_dir}")
    if args.dry_run:
        for c in cells:
            print(f"  {c}")
        return

    log_paths: list[Path] = []
    for arm, identity, task, repeat in cells:
        log_paths.append(run_cell(arm, identity, task, repeat, results_dir))

    if args.skip_scoring:
        print("Runs complete. Scoring skipped (--skip-scoring).")
        return

    # Score everything. Import late so the agents can run even if the scorer's
    # deps are half-installed.
    from runner import scorer

    print(f"Scoring {len(log_paths)} runs...")
    scores = scorer.score_all(results_dir, skip_judge=args.skip_judge)

    if args.summary:
        summary = scorer.summarize(scores)
        print("\n=== Summary ===")
        print(json.dumps(summary, indent=2, default=str))
        # Also persist the summary.
        summary_path = results_dir / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2, default=str))
        print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
