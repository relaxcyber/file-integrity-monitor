"""Walks through a folder and builds a FileRecord for every file.

Owner: Donald. Branch: feature/scanner
"""

import logging
import os
import stat
from pathlib import Path

from fim.hasher import hash_file
from fim.models import FileRecord

log = logging.getLogger(__name__)


def scan(root, ignore=None):
    """Scan a folder and return a dict {relative path: FileRecord}.

    ignore is an optional function that gets a relative path and returns
    True if that file or folder should be skipped. It is a function and not
    a list of patterns so this module does not depend on config.py.

    Files we cannot read are skipped with a warning, one bad file should not
    stop the whole scan.
    """
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(f"not a folder: {root}")

    records = {}

    # followlinks=False (the default) means we never walk into linked folders,
    # this also protects us from symlink loops
    for folder, dirs, files in os.walk(root):
        folder = Path(folder)

        dirs.sort()
        if ignore:
            dirs[:] = [d for d in dirs if not ignore(_rel(folder / d, root))]

        for name in sorted(files):
            full = folder / name
            rel = _rel(full, root)
            if ignore and ignore(rel):
                continue

            # a symlink could point outside the folder, so we skip it
            if full.is_symlink():
                log.debug("skipping symlink %s", rel)
                continue

            try:
                st = full.stat()
                digest = hash_file(full)
            except OSError as err:
                # file deleted while scanning, or no permission
                log.warning("cannot read %s (%s)", rel, err)
                continue

            records[rel] = FileRecord(
                path=rel,
                sha256=digest,
                size=st.st_size,
                mtime=st.st_mtime,
                mode=stat.S_IMODE(st.st_mode),
            )
    return records


def _rel(path, root):
    """Relative path with forward slashes, so a baseline made on Windows
    still matches on Linux."""
    return path.relative_to(root).as_posix()
