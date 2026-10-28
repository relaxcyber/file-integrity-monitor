"""Compares the baseline with a fresh scan and returns a list of Change.

Owner: Donald. Branch: feature/comparer
"""

from fim.models import Change, ChangeType


def compare(old, new):
    """old and new are dicts {rel path: FileRecord}."""
    changes = []

    for path, rec in new.items():
        if path not in old:
            changes.append(Change(path, ChangeType.ADDED, new=rec))
        elif rec.sha256 != old[path].sha256:
            changes.append(Change(path, ChangeType.MODIFIED, old=old[path], new=rec))

    for path, rec in old.items():
        if path not in new:
            changes.append(Change(path, ChangeType.DELETED, old=rec))

    return changes
