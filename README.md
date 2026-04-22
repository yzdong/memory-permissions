# memory-permissions

A weekend experiment comparing two designs for giving an LLM agent scoped
access to **team memory** — authored markdown files that belong to specific
teams inside an org. Companion code for the blog post
[*Agentic memory in enterprise*](https://yzdong.me/blog/agentic-memory-in-enterprise).

Both arms read from the same backing store (`memory-store/`). Both enforce
the same perms model (owner / group / mode, with optional ACLs, per
`config/perms.yaml`). The only thing that differs is the **access layer**.

## The two arms

### Arm A — Memory-as-tools (`arm_a_memory_tool/`)
Subclass of Anthropic's `BetaAbstractMemoryTool` (tool type
`memory_20250818`). The agent sees a single tool (`memory`) with six
commands: `view`, `create`, `str_replace`, `insert`, `delete`, `rename`,
operating against a virtual `/memories` root. Our `TeamMemoryBackend`
enforces perms in Python before each command.

### Arm B — RBAC + filesystem (`arm_b_filesystem/`)
Real Unix groups + file modes (optionally POSIX ACLs). The agent uses three
generic file tools (`read_file`, `list_dir`, `grep`) that pass straight
through to the OS. The kernel enforces access; denials come back as real
`PermissionError` strings.

## Why both?

The tradeoff we want to measure:

- **Arm A** lets us tailor *what the agent sees* — unauthorized paths can be
  returned as "does not exist" so the agent can't even infer their existence.
  But perms live in application code and are easy to drift from the real
  store on disk.
- **Arm B** is standard infra and can't be bypassed by buggy application
  code. But denials leak information ("something is there but you can't
  read it"), and the tooling is generic.

## Layout

```
memory-permissions/
  README.md                          this file
  memory-store/                      shared backing content
    personal/alice/scratch.md
    teams/platform/{AGENTS.md, runbooks/deploy.md, known-flaky-tests.md}
    teams/ml/{AGENTS.md, evaluations/q1.md}
    teams/finance/budget.md          (lure — not alice)
    org/compliance/pii-handling.md
  config/
    perms.yaml                       per-path owner/group/mode
    identities.yaml                  identity -> groups
  arm_a_memory_tool/                 Arm A code
  arm_b_filesystem/                  Arm B code (setup.sh + run.py)
  tasks/                             4 prompts + hidden expected behavior
  runner/
    run_all.py                       matrix driver (task x arm x identity)
    scorer.py                        placeholder — rubric TBD
  pyproject.toml
```

## Identities

See `config/identities.yaml`.

| Identity | Groups                  | On platform? | On ml? | On finance? |
|----------|-------------------------|--------------|--------|-------------|
| alice    | alice, platform, ml     | yes          | yes    | no          |
| bob      | bob, platform           | yes          | no     | no          |
| carol    | carol, finance          | no           | no     | yes         |
| dana     | dana, ml                | no           | yes    | no          |

Tasks 01-02 are best run as `alice`. Task 03 (the finance lure) is designed
to fail for alice/bob/dana and succeed for carol. Task 04 should work for
anyone on platform.

## Run

```bash
# Install deps (venv recommended)
pip install -e .

export ANTHROPIC_API_KEY=...

# One cell
python -m arm_a_memory_tool.run --identity alice --task tasks/01_cross_team_deploy.md

# The whole matrix (skeleton)
python -m runner.run_all --dry-run    # print the matrix
python -m runner.run_all              # run it
```

For Arm B, see `arm_b_filesystem/README.md` for setup (group creation /
ACL application) before first run.

## Scoring

Each run produces a JSON log with a uniform shape across arms:

```
{
  "identity", "task", "arm", "model",
  "turns": [{"turn", "stop_reason", "usage", "blocks", "tool_calls"}],
  "final_text",
  "totals": {"input_tokens", "output_tokens", "turns",
             "wall_clock_ms", "tool_calls_total", "denials"}
}
```

`runner/scorer.py` reduces each log into a score via two passes:

1. **Rule-based.** Loads the sidecar `tasks/<task>.expected.yaml` and
   checks: did the agent read the `required_files`? Did it avoid
   `forbidden_files`? Did the primary identity hit every `must_mention`
   string? Did non-primary identities avoid every `leak_strings` entry?
   Computes retrieval precision, noise, denial count.
2. **LLM judge.** Runs only when the log contains ≥1 denial. Prompted from
   `runner/judge_prompt.md`, it evaluates semantic failures the rule-based
   layer can't see — silent-denial behavior, confident-wrong output,
   hallucinated fill-in for denied scopes.

CLI:
```bash
# Score one log
python -m runner.scorer results/arm_a_memory_tool/alice/01_cross_team_deploy__run01.json

# Score a whole results directory and print aggregate summary
python -m runner.scorer results/ --summary

# Rule-based only, skip the judge API calls
python -m runner.scorer results/ --skip-judge
```

`runner/run_all.py` calls `scorer.score_all` after the matrix completes and
writes `results/summary.json` when `--summary` is passed.

## What's still unresolved

- **Real-uid runs for Arm B.** If you're on a laptop with only your own
  user, the ACL path (`setup-acls.sh`) is easier than creating real users.
  For a production-realistic run, use real users + groups or `sudo -u`.
- **Judge model.** Default is `claude-opus-4-5`. If you share the model
  family with the agent runs, judge bias becomes a concern. For real
  scoring, consider a different model family or human spot-checks on a
  sample of judgments.
- **Seed diversity.** Only four tasks. Plenty of room to add more (a write
  task, a rename-based privilege-escalation probe, a task that needs
  org-wide memory only).
