#!/usr/bin/env bash
# Apply Unix group+mode perms to memory-store/ based on config/perms.yaml.
#
# Usage:
#   ./setup.sh [path-to-memory-store] [path-to-perms-yaml]
#
# This script uses chgrp + chmod. Creating groups and adding your user to
# them requires root (sudo). On macOS, group management uses `dseditgroup`;
# on Linux, `groupadd` + `usermod`.
#
# For a non-root alternative, see setup-acls.sh, which uses POSIX ACLs and
# does not require real system groups.

set -euo pipefail

STORE="${1:-$(cd "$(dirname "$0")/../memory-store" && pwd)}"
PERMS="${2:-$(cd "$(dirname "$0")/../config" && pwd)/perms.yaml}"

if [[ ! -d "$STORE" ]]; then
  echo "error: memory-store not found at $STORE" >&2
  exit 1
fi
if [[ ! -f "$PERMS" ]]; then
  echo "error: perms.yaml not found at $PERMS" >&2
  exit 1
fi

OS="$(uname -s)"
GROUPS_NEEDED=(platform ml finance all)

echo "=== Step 1: ensure groups exist ==="
for g in "${GROUPS_NEEDED[@]}"; do
  case "$OS" in
    Darwin)
      if dseditgroup -o read "$g" >/dev/null 2>&1; then
        echo "  group $g exists"
      else
        echo "  creating group $g (requires sudo)"
        sudo dseditgroup -o create "$g"
      fi
      ;;
    Linux)
      if getent group "$g" >/dev/null; then
        echo "  group $g exists"
      else
        echo "  creating group $g (requires sudo)"
        sudo groupadd "$g"
      fi
      ;;
    *)
      echo "  unsupported OS: $OS" >&2
      exit 1
      ;;
  esac
done

echo ""
echo "=== Step 2: apply chgrp + chmod per perms.yaml ==="
# Tiny YAML reader: we only need entries[*].{path,group,mode}.
python3 - "$STORE" "$PERMS" <<'PY'
import sys, os, subprocess, yaml
store, perms = sys.argv[1], sys.argv[2]
with open(perms) as f:
    data = yaml.safe_load(f)
for e in data["entries"]:
    p = os.path.join(store, e["path"])
    if not os.path.exists(p):
        print(f"  skip (missing): {p}")
        continue
    subprocess.run(["chgrp", e["group"], p], check=True)
    subprocess.run(["chmod", e["mode"], p], check=True)
    print(f"  {e['mode']} {e['group']:<10} {p}")
PY

echo ""
echo "=== Manual follow-ups ==="
cat <<'NOTE'
  * Add yourself to the groups you intend to act as:
      macOS:  sudo dseditgroup -o edit -a <you> -t user <group>
      Linux:  sudo usermod -aG <group> <you>
  * Log out and back in (or `exec su - <you>`) for group membership to
    take effect. `id` should list the new groups.
  * Run Arm B's runner AS that user. The OS filesystem enforces access —
    unauthorized reads raise PermissionError, which the runner surfaces to
    the agent as a tool error.
NOTE
