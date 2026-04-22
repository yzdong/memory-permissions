#!/usr/bin/env bash
# ACL-based variant of setup.sh. Does NOT require creating real OS groups.
# Instead, it grants per-identity ACLs using setfacl (Linux) or `chmod +a`
# (macOS). Useful for running the experiment on a dev laptop without sudo.
#
# Usage:
#   ./setup-acls.sh [path-to-memory-store] [path-to-perms-yaml] [path-to-identities-yaml]

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
STORE="${1:-$(cd "$HERE/../memory-store" && pwd)}"
PERMS="${2:-$HERE/../config/perms.yaml}"
IDS="${3:-$HERE/../config/identities.yaml}"

OS="$(uname -s)"

echo "=== Applying ACLs per-identity ==="
python3 - "$STORE" "$PERMS" "$IDS" "$OS" <<'PY'
import os, subprocess, sys, yaml

store, perms_path, ids_path, os_name = sys.argv[1:5]

with open(perms_path) as f:
    perms = yaml.safe_load(f)
with open(ids_path) as f:
    ids = yaml.safe_load(f)

# Build: group -> list of identities in that group.
group_members: dict[str, list[str]] = {}
for ident, info in ids["identities"].items():
    for g in info["groups"]:
        group_members.setdefault(g, []).append(ident)

def mode_to_bits(mode_str: str) -> tuple[int, int, int]:
    m = int(mode_str, 8)
    return (m >> 6) & 7, (m >> 3) & 7, m & 7

def bits_to_rwx(b: int, is_dir: bool) -> str:
    r = "r" if b & 4 else "-"
    w = "w" if b & 2 else "-"
    # On directories we grant x together with r so traversal works.
    x = "x" if (b & 1) or (is_dir and (b & 4)) else "-"
    return r + w + x

def grant(path: str, ident: str, rwx: str) -> None:
    if rwx == "---":
        return
    is_dir = os.path.isdir(path)
    if os_name == "Linux":
        subprocess.run(["setfacl", "-m", f"u:{ident}:{rwx}", path], check=True)
    elif os_name == "Darwin":
        # macOS uses chmod +a with a verbose form. We approximate.
        perms = []
        if "r" in rwx: perms += ["read"]
        if "w" in rwx: perms += ["write", "delete", "append"]
        if "x" in rwx and is_dir: perms += ["search"]
        if not perms: return
        spec = f"user:{ident} allow {','.join(perms)}"
        subprocess.run(["chmod", "+a", spec, path], check=True)
    else:
        print(f"  unsupported OS: {os_name}", file=sys.stderr)
        sys.exit(1)

for e in perms["entries"]:
    full = os.path.join(store, e["path"])
    if not os.path.exists(full):
        print(f"  skip (missing): {full}")
        continue
    is_dir = os.path.isdir(full)
    o_bits, g_bits, w_bits = mode_to_bits(e["mode"])

    # Owner ACL.
    owner_rwx = bits_to_rwx(o_bits, is_dir)
    if e["owner"] != "root":
        grant(full, e["owner"], owner_rwx)

    # Group ACL -> each member of the group.
    grp_rwx = bits_to_rwx(g_bits, is_dir)
    for member in group_members.get(e["group"], []):
        if member == e["owner"]:
            continue
        grant(full, member, grp_rwx)

    # World (other) perms: apply to the file mode itself via chmod.
    # We clear write bit for group/other via 0-<group>=w etc. but the simple
    # approach is to chmod the file readable by all if other has read.
    subprocess.run(["chmod", e["mode"], full], check=False)
    print(f"  acl set for {e['path']}")
PY

echo ""
echo "=== Done ==="
echo "Verify with: ls -le (macOS) or getfacl (Linux) on memory-store/..."
