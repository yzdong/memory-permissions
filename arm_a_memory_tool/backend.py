"""TeamMemoryBackend: a BetaAbstractMemoryTool subclass that enforces
Unix-style perms against the caller's identity and group membership.

Design notes:
- The agent sees a virtual `/memories` root. We map `/memories/X` <-> a real
  path under `memory_store_root / X`.
- Perms come from a sidecar YAML (config/perms.yaml) loaded on init. Every
  path in the store should have an entry; missing entries deny by default.
- Unauthorized paths return the same error string as missing paths, so the
  agent cannot distinguish "you don't have access" from "not there". This is
  intentional per Anthropic's memory-tool error guidance.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from anthropic.lib.tools import BetaAbstractMemoryTool
from anthropic.lib.tools._beta_functions import BetaFunctionToolResultType
from anthropic.types.beta import (
    BetaMemoryTool20250818CreateCommand,
    BetaMemoryTool20250818DeleteCommand,
    BetaMemoryTool20250818InsertCommand,
    BetaMemoryTool20250818RenameCommand,
    BetaMemoryTool20250818StrReplaceCommand,
    BetaMemoryTool20250818ViewCommand,
)


# Error string used for both missing-path and unauthorized-path cases.
# Keep this exactly as written; the experiment relies on the two being
# indistinguishable to the agent.
PATH_DOES_NOT_EXIST = (
    "Error: The path {path} does not exist. Please provide a valid path."
)


@dataclass(frozen=True)
class PermsEntry:
    path: str           # relative to memory-store, e.g. "teams/platform"
    owner: str
    group: str
    mode: int           # e.g. 0o770

    @property
    def owner_bits(self) -> int:
        return (self.mode >> 6) & 0o7

    @property
    def group_bits(self) -> int:
        return (self.mode >> 3) & 0o7

    @property
    def other_bits(self) -> int:
        return self.mode & 0o7


# Op -> required bit. For this experiment:
#   read: view on a file, view on a directory (list)
#   write: create, str_replace, insert, delete, rename (dst). rename src
#          needs write on the source's parent; for simplicity we require
#          write on both src and dst.
OP_TO_BIT = {
    "read": 0o4,
    "write": 0o2,
}


def permission_check(
    entry: PermsEntry | None,
    identity: str,
    groups: Iterable[str],
    op: str,
) -> bool:
    """Pure perms check. Returns True iff (identity, groups) may perform op.

    If entry is None (no perms record), deny.
    """
    if entry is None:
        return False
    bit = OP_TO_BIT.get(op)
    if bit is None:
        return False
    gset = set(groups)
    if identity == entry.owner:
        return bool(entry.owner_bits & bit)
    if entry.group in gset:
        return bool(entry.group_bits & bit)
    return bool(entry.other_bits & bit)


class TeamMemoryBackend(BetaAbstractMemoryTool):
    """Team-aware memory backend.

    Parameters
    ----------
    identity : str
        Caller identity (e.g. "alice").
    groups : list[str]
        Groups the caller belongs to. "all" will be added automatically.
    memory_store_root : str | Path
        Absolute path to the memory-store/ directory.
    perms_yaml_path : str | Path
        Path to config/perms.yaml.
    """

    VIRTUAL_ROOT = "/memories"

    def __init__(
        self,
        identity: str,
        groups: list[str],
        memory_store_root: str | Path,
        perms_yaml_path: str | Path,
    ) -> None:
        super().__init__()
        self.identity = identity
        self.groups = list(groups)
        if "all" not in self.groups:
            self.groups.append("all")
        self.root = Path(memory_store_root).resolve()
        self._perms: dict[str, PermsEntry] = {}
        self._load_perms(Path(perms_yaml_path))

    # ----- perms loading -------------------------------------------------

    def _load_perms(self, perms_path: Path) -> None:
        with perms_path.open() as f:
            data = yaml.safe_load(f)
        for e in data.get("entries", []):
            entry = PermsEntry(
                path=e["path"].strip("/"),
                owner=e["owner"],
                group=e["group"],
                mode=int(e["mode"], 8),
            )
            self._perms[entry.path] = entry

    def _entry_for(self, rel: str) -> PermsEntry | None:
        return self._perms.get(rel.strip("/"))

    # ----- path translation ----------------------------------------------

    def _virtual_to_real(self, virtual_path: str) -> Path | None:
        """Map /memories/X -> memory_store_root/X. Return None if invalid."""
        if not virtual_path.startswith(self.VIRTUAL_ROOT):
            return None
        rel = virtual_path[len(self.VIRTUAL_ROOT):].lstrip("/")
        real = (self.root / rel).resolve()
        # Prevent escaping the root via .. etc.
        try:
            real.relative_to(self.root)
        except ValueError:
            return None
        return real

    def _real_to_rel(self, real: Path) -> str:
        return str(real.relative_to(self.root)) if real != self.root else ""

    def _can(self, virtual_path: str, op: str) -> tuple[bool, Path | None]:
        real = self._virtual_to_real(virtual_path)
        if real is None:
            return False, None
        rel = self._real_to_rel(real)
        entry = self._entry_for(rel) if rel else self._entry_for("")
        # Root case: always allow read, deny write at root.
        if not rel:
            return (op == "read"), real
        return permission_check(entry, self.identity, self.groups, op), real

    def _deny(self, virtual_path: str) -> str:
        return PATH_DOES_NOT_EXIST.format(path=virtual_path)

    # ----- command handlers ----------------------------------------------

    def view(self, command: BetaMemoryTool20250818ViewCommand) -> BetaFunctionToolResultType:
        ok, real = self._can(command.path, "read")
        if not ok or real is None or not real.exists():
            return self._deny(command.path)

        if real.is_dir():
            # Tab-separated directory listing, only entries the caller can see.
            visible: list[str] = []
            for child in sorted(real.iterdir()):
                child_rel = self._real_to_rel(child)
                child_entry = self._entry_for(child_rel)
                if permission_check(child_entry, self.identity, self.groups, "read"):
                    name = child.name + ("/" if child.is_dir() else "")
                    visible.append(name)
            header = f"Directory: {command.path}\n"
            body = "\n".join(visible)
            return header + body

        # File: line-numbered contents. Honor view_range if provided.
        text = real.read_text()
        lines = text.splitlines()
        start, end = 1, len(lines)
        if command.view_range:
            start = max(1, command.view_range[0])
            end = len(lines) if command.view_range[1] == -1 else min(len(lines), command.view_range[1])
        out_lines = []
        for i in range(start, end + 1):
            out_lines.append(f"{i:>6}\t{lines[i - 1]}")
        return "\n".join(out_lines)

    def create(self, command: BetaMemoryTool20250818CreateCommand) -> BetaFunctionToolResultType:
        # Need write on parent directory (to create) OR write on the file
        # itself (to overwrite). We check both conditions.
        real = self._virtual_to_real(command.path)
        if real is None:
            return self._deny(command.path)
        parent_virtual = os.path.dirname(command.path.rstrip("/"))
        parent_ok, parent_real = self._can(parent_virtual, "write")
        file_rel = self._real_to_rel(real)
        file_entry = self._entry_for(file_rel)
        file_ok = permission_check(file_entry, self.identity, self.groups, "write") if file_entry else False
        if not (parent_ok or file_ok):
            return self._deny(command.path)
        if parent_real is None or not parent_real.exists():
            return self._deny(command.path)
        real.write_text(command.file_text)
        return f"File created successfully at {command.path}"

    def str_replace(self, command: BetaMemoryTool20250818StrReplaceCommand) -> BetaFunctionToolResultType:
        ok, real = self._can(command.path, "write")
        if not ok or real is None or not real.is_file():
            return self._deny(command.path)
        text = real.read_text()
        if command.old_str not in text:
            return f"Error: Text not found in {command.path}"
        if text.count(command.old_str) > 1:
            return f"Error: Multiple matches for old_str in {command.path}; refine and retry."
        new_text = text.replace(command.old_str, command.new_str, 1)
        real.write_text(new_text)
        return f"File {command.path} has been edited successfully"

    def insert(self, command: BetaMemoryTool20250818InsertCommand) -> BetaFunctionToolResultType:
        ok, real = self._can(command.path, "write")
        if not ok or real is None or not real.is_file():
            return self._deny(command.path)
        lines = real.read_text().splitlines()
        idx = command.insert_line
        if idx < 0 or idx > len(lines):
            return f"Error: insert_line {idx} out of range for {command.path}"
        new_lines = lines[:idx] + command.insert_text.splitlines() + lines[idx:]
        real.write_text("\n".join(new_lines) + ("\n" if real.read_text().endswith("\n") else ""))
        return f"Text inserted into {command.path} at line {idx}"

    def delete(self, command: BetaMemoryTool20250818DeleteCommand) -> BetaFunctionToolResultType:
        ok, real = self._can(command.path, "write")
        if not ok or real is None or not real.exists():
            return self._deny(command.path)
        if real.is_dir():
            # Only delete empty dirs to be safe.
            try:
                real.rmdir()
            except OSError:
                return f"Error: Directory {command.path} is not empty"
        else:
            real.unlink()
        return f"Deleted {command.path}"

    def rename(self, command: BetaMemoryTool20250818RenameCommand) -> BetaFunctionToolResultType:
        src_ok, src_real = self._can(command.old_path, "write")
        dst_ok, dst_real = self._can(command.new_path, "write")
        if not src_ok or src_real is None or not src_real.exists():
            return self._deny(command.old_path)
        if not dst_ok or dst_real is None:
            return self._deny(command.new_path)
        src_real.rename(dst_real)
        return f"Renamed {command.old_path} to {command.new_path}"
