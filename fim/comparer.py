"""Compares the baseline with a fresh scan and returns a list of Change.

Owner: Donald. Branch: feature/comparer

The idea is simple: both sides are dicts keyed by path, so we only need to
look at three groups. Paths only in new, paths only in old, and paths in both.
"""

from fim.models import Change, ChangeType


def compare(old, new):
    """old and new are dicts {rel path: FileRecord}.

    Returns a list of Change sorted by path. A file whose content and
    permissions both changed gives two entries (MODIFIED and PERMISSIONS).
    """
    changes = []

    for path, rec in new.items():
        if path not in old:
            changes.append(Change(path, ChangeType.ADDED, new=rec))
            continue

        before = old[path]

        # the hash is the real proof that the content changed
        if rec.sha256 != before.sha256:
            changes.append(Change(path, ChangeType.MODIFIED, old=before, new=rec))

        if rec.mode != before.mode:
            changes.append(Change(path, ChangeType.PERMISSIONS, old=before, new=rec))

        # a different mtime alone is ignored on purpose: "touch file" does not
        # change anything that matters for integrity

    for path, rec in old.items():
        if path not in new:
            changes.append(Change(path, ChangeType.DELETED, old=rec))

    # same input gives the same output order, easier to read and to test
    changes.sort(key=lambda ch: (ch.path, ch.type.value))
    return changes
