#!/bin/sh
# Entrypoint that re-applies setup.sh when memory-store is bind-mounted.
#
# When the caller mounts host memory-store/ and config/ over the baked-in
# copies, perms from the build-time setup.sh are gone (the mount replaces
# the inode tree). We detect that and reapply. If nothing is mounted, we
# no-op — the baked-in perms from image build are still in effect.

set -e

CANONICAL="/experiment/memory-store/teams/platform/runbooks/deploy.md"

if [ -f "$CANONICAL" ]; then
    current_group=$(stat -c '%G' "$CANONICAL" 2>/dev/null || echo "unknown")
    if [ "$current_group" != "platform" ]; then
        echo "[entrypoint] memory-store perms not applied (group=$current_group); running setup.sh"
        bash /experiment/arm_b_filesystem/setup.sh > /dev/null 2>&1 || \
            echo "[entrypoint] warning: setup.sh exited non-zero"
    fi
fi

exec "$@"
