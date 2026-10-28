"""Walks through a folder and builds a FileRecord for every file.

Owner: Donald. Branch: feature/scanner
"""

import os
import stat
from pathlib import Path

from fim.hasher import hash_file
from fim.models import FileRecord


def scan(root, ignore=None):
    """Scan a folder and return a dict {relative path: FileRecord}.

    ignore is an optional function that gets a relative path and returns
    True if that file or folder should be skipped. It is a function and not
    a list of patterns so this module does not depend on config.py.
    """
    root = Path(root)
    records = {}

    for folder, dirs, files in os.walk(root):
        folder = Path(folder)

        # sorting makes the order the same on every run
        dirs.sort()
        # removing items from dirs in place stops os.walk from entering them
        if ignore:
            dirs[:] = [d for d in dirs if not ignore(_rel(folder / d, root))]

        for name in sorted(files):
            full = folder / name
            rel = _rel(full, root)
            if ignore and ignore(rel):
                continue

            st = full.stat()
            records[rel] = FileRecord(
                path=rel,
                sha256=hash_file(full),
                size=st.st_size,
                mtime=st.st_mtime,
                mode=stat.S_IMODE(st.st_mode),  # only the permission bits
            )
    return records


def _rel(path, root):
    """Relative path with forward slashes, so a baseline made on Windows
    still matches on Linux."""
    return path.relative_to(root).as_posix()
