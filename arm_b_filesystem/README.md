# Arm B — RBAC + local filesystem

Access control lives in the OS: real Unix groups + file modes (with optional
POSIX ACLs). The agent uses three custom tools (`read_file`, `list_dir`,
`grep`) that proxy to the filesystem. When the OS denies access, the tool
surfaces the raw `PermissionError` to Claude.

The two arms read the same `memory-store/` directory; only the access layer
differs.

## Setup

Pick ONE of:

### (a) Real groups — closer to production, requires sudo
```
./setup.sh
# then add yourself to the groups you want to impersonate:
sudo dseditgroup -o edit -a $USER -t user platform   # macOS
sudo usermod -aG platform $USER                       # Linux
# re-login so the group takes effect
```

### (b) POSIX ACLs — dev-friendly, no sudo required on Linux
```
./setup-acls.sh
```

## Run
```
export ANTHROPIC_API_KEY=...
python -m arm_b_filesystem.run --identity alice --task tasks/01_cross_team_deploy.md
```

IMPORTANT: `--identity` only labels the log. Actual access is determined by
the **process's effective uid/gid**. To run "as alice", launch the process
under alice's uid (`sudo -u alice ...` or `su - alice -c ...`). On a single
dev box, pair option (b) above with separate real users.

## Tools exposed to Claude

- `read_file(path)` — `Path.read_text()` relative to `memory-store/`.
- `list_dir(path)` — lists children; directories entries get a trailing `/`.
- `grep(pattern, path=".")` — recursive regex search.

All three surface `PermissionError` / `FileNotFoundError` verbatim. No
attempt is made to hide unauthorized entries; the agent sees the real OS
behavior.

## Known limitations / TODOs

- `grep` silently skips files it cannot read (that's what the OS would do
  via `find -print` on inaccessible entries). We may want to instead emit a
  note so the scorer can tell the agent saw a denial.
- `setup-acls.sh` on macOS is a best effort; the Linux `setfacl` path is
  better tested.
