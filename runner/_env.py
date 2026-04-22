"""Tiny .env loader. No python-dotenv dependency.

Called at the top of each runner so ANTHROPIC_API_KEY is available even when
the user hasn't exported it. Looks for .env at ~/personal/.env first, then
at the repo parent, and stops at the first hit.
"""

from __future__ import annotations

import os
from pathlib import Path


_ENV_CANDIDATES = [
    # Project root (e.g. /experiment/.env when mounted into the container).
    Path(__file__).resolve().parent.parent / ".env",
    # Host default: ~/personal/.env
    Path.home() / "personal" / ".env",
    # Sibling of the project dir (original host layout).
    Path(__file__).resolve().parent.parent.parent / ".env",
]


def load_env_if_needed(*, required_key: str = "ANTHROPIC_API_KEY") -> None:
    """If `required_key` isn't already in os.environ, look for a .env file and
    populate os.environ from it. Silently does nothing if no .env is found."""
    if os.environ.get(required_key):
        return
    for env_path in _ENV_CANDIDATES:
        if not env_path.exists():
            continue
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value
        if os.environ.get(required_key):
            return
