# Arm A — Memory-as-tools

Access control lives inside a custom `BetaAbstractMemoryTool` subclass. The
agent sees a single tool (`memory`, type `memory_20250818`) with six commands
(`view`, `create`, `str_replace`, `insert`, `delete`, `rename`). Every call
is routed through `TeamMemoryBackend`, which:

1. Maps the virtual `/memories/...` path to a real path under `memory-store/`.
2. Looks up the path's perms entry in `config/perms.yaml`.
3. Applies Unix-style owner/group/other semantics against the caller's
   identity and groups.
4. For `view` on a directory, filters the listing to only entries the caller
   can read (hides unauthorized entries).
5. For unauthorized files, returns the Anthropic-standard "does not exist"
   error — indistinguishable from a truly missing path. This is deliberate:
   we do not want to leak the existence of files the caller cannot read.

## Run

```
export ANTHROPIC_API_KEY=...
python -m arm_a_memory_tool.run --identity alice --task tasks/01_cross_team_deploy.md
```

Identity comes from `--identity` or `$MEM_IDENTITY`. Groups are looked up
from `config/identities.yaml`.

## Key files

- `backend.py` — `TeamMemoryBackend` + pure `permission_check` helper.
- `run.py` — task runner; writes JSON log under `results/`.

## Known limitations / TODOs

- `run.py` uses `run_tools().until_done()` for brevity; per-turn tool-call
  logging is left as a TODO (drop down to the lower-level create loop).
- No rate limiting or retries on the API call.
