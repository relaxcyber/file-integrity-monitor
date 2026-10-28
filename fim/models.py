"""Shared data classes.

Both of us import these, so please do not change the field names
without telling each other first.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ChangeType(str, Enum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"
    PERMISSIONS = "permissions"


@dataclass(frozen=True)
class FileRecord:
    """What we remember about one file at the moment of scanning."""

    path: str      # path relative to the monitored folder
    sha256: str    # hex digest of the content
    size: int      # bytes
    mtime: float   # last modification time (unix timestamp)
    mode: int      # permission bits, for example 0o644


@dataclass(frozen=True)
class Change:
    """One difference between the baseline and the current state."""

    path: str
    type: ChangeType
    old: Optional[FileRecord] = None   # None for ADDED
    new: Optional[FileRecord] = None   # None for DELETED
