"""Walks through a folder and builds a FileRecord for every file.

Owner: Donald. Branch: feature/scanner
"""

import os

from fim.hasher import hash_file
from fim.models import FileRecord


def scan(root):
    """Scan a folder and return a dict {relative path: FileRecord}."""
    records = {}
    for folder, _dirs, files in os.walk(root):
        for name in files:
            full = os.path.join(folder, name)
            rel = os.path.relpath(full, root)
            st = os.stat(full)
            records[rel] = FileRecord(
                path=rel,
                sha256=hash_file(full),
                size=st.st_size,
                mtime=st.st_mtime,
                mode=st.st_mode,
            )
    return records
