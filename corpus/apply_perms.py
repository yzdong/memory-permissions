"""Rewrite `config/perms.yaml` so every directory and file under
`memory-store/` has a perm entry.

Rules:
- Canonical entries already listed in perms.yaml are preserved verbatim.
- New files inherit from the conventions of their parent tree:
    teams/platform/**  -> owner=root, group=platform, mode=0660 (files) / 0770 (dirs)
    teams/ml/**        -> owner=root, group=ml,       mode=0660 / 0770
    teams/finance/**   -> owner=root, group=finance,  mode=0660 / 0770
    org/compliance/**  -> owner=root, group=all,      mode=0644 / 0755
    personal/alice/**  -> owner=alice, group=alice,   mode=0600 / 0700

Produces a deterministic ordering: depth-first, sorted by path.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MEMORY_STORE = ROOT / "memory-store"
PERMS_YAML = ROOT / "config" / "perms.yaml"


# -------------------- rule tables --------------------

# (path-prefix relative to memory-store, owner, group, dir_mode, file_mode)
# First match wins; order matters.
RULES: list[tuple[str, str, str, str, str]] = [
    ("personal/alice",    "alice", "alice",    "0700", "0600"),
    ("personal",          "root",  "all",      "0755", "0644"),
    ("teams/platform",    "root",  "platform", "0770", "0660"),
    ("teams/ml",          "root",  "ml",       "0770", "0660"),
    ("teams/finance",     "root",  "finance",  "0770", "0660"),
    ("teams",             "root",  "all",      "0755", "0644"),
    ("org/compliance",    "root",  "all",      "0755", "0644"),
    ("org",               "root",  "all",      "0755", "0644"),
]


def rule_for(rel_path: str) -> tuple[str, str, str, str]:
    """Return (owner, group, dir_mode, file_mode) for a path relative to memory-store."""
    for prefix, owner, group, dmode, fmode in RULES:
        if rel_path == prefix or rel_path.startswith(prefix + "/") or rel_path == "":
            if rel_path == "" and prefix != "":
                continue
            return owner, group, dmode, fmode
    # Default fallback.
    return "root", "all", "0755", "0644"


# -------------------- existing-entry preservation --------------------

def load_existing_entries() -> dict[str, dict[str, str]]:
    """Load existing perms.yaml and key entries by path."""
    if not PERMS_YAML.exists():
        return {}
    data = yaml.safe_load(PERMS_YAML.read_text()) or {}
    out = {}
    for e in data.get("entries", []) or []:
        if "path" in e:
            out[e["path"]] = e
    return out


# -------------------- main --------------------

def enumerate_paths() -> list[Path]:
    """Return all directories and files under memory-store, including memory-store itself?
    No — perms.yaml tracks contents inside memory-store; top-level covered by runner."""
    paths: list[Path] = []
    for p in sorted(MEMORY_STORE.rglob("*")):
        # Skip DS_Store and other junk
        if p.name.startswith("."):
            continue
        paths.append(p)
    return paths


def build_entries() -> list[dict[str, Any]]:
    existing = load_existing_entries()
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()

    # We iterate all filesystem paths, then emit entries in sort order.
    for p in enumerate_paths():
        rel = p.relative_to(MEMORY_STORE).as_posix()
        if rel in seen:
            continue
        seen.add(rel)

        if rel in existing:
            entries.append(existing[rel])
            continue

        owner, group, dmode, fmode = rule_for(rel)
        mode = dmode if p.is_dir() else fmode
        entries.append({
            "path": rel,
            "owner": owner,
            "group": group,
            "mode": mode,
        })

    # Sort entries by path for readability and determinism.
    entries.sort(key=lambda e: e["path"])
    return entries


HEADER = """# Sidecar perms for memory-store.
#
# Semantics (Unix-style):
#   mode: three octal digits: owner / group / other.
#   bits: 4 = read, 2 = write, 1 = execute (directory listing).
#   Files: read+write. Directories: read = can view listing, execute = can
#   traverse. For this experiment we treat r on directories as "can view",
#   and don't separately model x.
#
# ACLs (optional): a list of {identity, perms} entries granting explicit
# access to specific identities beyond owner/group/other. Used by Arm A's
# pure Python check; Arm B translates these to POSIX ACLs via setfacl.
#
# Every directory and file in memory-store/ must be covered.
# NOTE: Auto-expanded by corpus/apply_perms.py after corpus generation.
"""


def dump_yaml(entries: list[dict[str, Any]]) -> str:
    # Use PyYAML with quotes around mode to preserve octal-looking strings.
    # We hand-assemble for stable ordering (path, owner, group, mode).
    lines = [HEADER, "entries:"]
    for e in entries:
        lines.append(f"  - path: {e['path']}")
        lines.append(f"    owner: {e['owner']}")
        lines.append(f"    group: {e['group']}")
        lines.append(f'    mode: "{e["mode"]}"')
        # Preserve any ACLs if present.
        if "acls" in e and e["acls"]:
            lines.append("    acls:")
            for acl in e["acls"]:
                ident = acl.get("identity", "")
                perms = acl.get("perms", "")
                lines.append(f"      - identity: {ident}")
                lines.append(f"        perms: {perms}")
    return "\n".join(lines) + "\n"


def main() -> int:
    if not MEMORY_STORE.exists():
        print(f"memory-store not found at {MEMORY_STORE}", file=sys.stderr)
        return 2
    entries = build_entries()
    text = dump_yaml(entries)
    # Validate by parsing back.
    parsed = yaml.safe_load(text)
    assert isinstance(parsed, dict) and "entries" in parsed, "bad yaml"
    PERMS_YAML.write_text(text)
    print(f"wrote {len(entries)} entries to {PERMS_YAML.relative_to(ROOT)}")
    # Quick coverage stats
    n_dirs = sum(1 for e in entries if (MEMORY_STORE / e["path"]).is_dir())
    n_files = sum(1 for e in entries if (MEMORY_STORE / e["path"]).is_file())
    print(f"  dirs={n_dirs} files={n_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
