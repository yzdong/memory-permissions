# Linux container that mirrors the Arm B production shape:
# real OS users + groups with real filesystem perms. Arm A runs the same way
# here — its backend enforces in Python regardless of UID.
#
# Build (only when Python source / deps change):
#   docker build -t mem-perm .
#
# Run matrix with live corpus + config from host (no rebuild needed for
# corpus edits or perms.yaml edits):
#   docker run --rm \
#     -v /Users/zidong/personal/.env:/experiment/.env:ro \
#     -v $(pwd)/memory-store:/experiment/memory-store \
#     -v $(pwd)/config:/experiment/config \
#     -v $(pwd)/tasks:/experiment/tasks \
#     -v $(pwd)/results:/experiment/results \
#     mem-perm python -m runner.run_all --summary
#
# The entrypoint re-runs setup.sh whenever memory-store is bind-mounted,
# so chgrp/chmod from perms.yaml get re-applied to the host inodes.
#
# Without bind mounts, the image ships with a baked-in copy of memory-store
# and setup.sh has already been applied.

FROM python:3.11-slim

# util-linux gives us runuser; acl is there if we ever need POSIX ACLs.
RUN apt-get update && apt-get install -y --no-install-recommends \
        util-linux \
        acl \
    && rm -rf /var/lib/apt/lists/*

# Groups + users matching config/identities.yaml.
#   alice   — platform, ml (not finance)
#   bob     — platform only
#   carol   — finance only
#   dana    — ml only
# Every identity is implicitly in the `all` group (org-wide tier).
RUN groupadd -r platform && \
    groupadd -r ml && \
    groupadd -r finance && \
    groupadd -r all && \
    useradd -m -s /bin/bash -G platform,ml,all alice && \
    useradd -m -s /bin/bash -G platform,all       bob && \
    useradd -m -s /bin/bash -G finance,all        carol && \
    useradd -m -s /bin/bash -G ml,all             dana

WORKDIR /experiment

# Python deps first so source edits don't invalidate the dep layer.
COPY pyproject.toml /experiment/
RUN pip install --no-cache-dir "anthropic>=0.84.0" "pyyaml>=6.0"

# Project source.
COPY . /experiment/

# Editable install for `python -m ...` module imports.
RUN pip install --no-cache-dir -e .

# Source code must be readable/executable by all four identities.
# memory-store/ keeps its strict perms (applied next by setup.sh).
RUN find /experiment -mindepth 1 -maxdepth 1 ! -name memory-store -exec chmod -R a+rX {} +

# Apply perms to memory-store/ from config/perms.yaml. setup.sh no-ops the
# group-creation step because the groups already exist. These perms apply
# to the baked-in copy; if memory-store is bind-mounted at runtime, the
# entrypoint re-applies perms to the mounted tree.
RUN bash /experiment/arm_b_filesystem/setup.sh

# Results dir: owned by `all` with setgid so files written by any identity
# inherit group=all and are readable by the others + the host user.
RUN mkdir -p /experiment/results && \
    chgrp all /experiment/results && \
    chmod 2775 /experiment/results

# Tell run_all.py to wrap Arm B subprocesses with `runuser -u <identity> --`.
ENV USE_RUNUSER=1

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["bash"]
