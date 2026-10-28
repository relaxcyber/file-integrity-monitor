"""Tests for fim.comparer"""

from fim.comparer import compare
from fim.models import ChangeType, FileRecord


def rec(path, sha="h1", mode=0o644, mtime=1.0):
    return FileRecord(path=path, sha256=sha, size=1, mtime=mtime, mode=mode)


def as_pairs(changes):
    return [(ch.path, ch.type) for ch in changes]


def test_no_changes():
    state = {"a.txt": rec("a.txt")}
    assert compare(state, dict(state)) == []


def test_added_file():
    old = {}
    new = {"a.txt": rec("a.txt")}
    changes = compare(old, new)
    assert as_pairs(changes) == [("a.txt", ChangeType.ADDED)]
    assert changes[0].old is None
    assert changes[0].new == new["a.txt"]


def test_deleted_file():
    old = {"a.txt": rec("a.txt")}
    changes = compare(old, {})
    assert as_pairs(changes) == [("a.txt", ChangeType.DELETED)]
    assert changes[0].new is None


def test_modified_file():
    old = {"a.txt": rec("a.txt", sha="h1")}
    new = {"a.txt": rec("a.txt", sha="h2")}
    changes = compare(old, new)
    assert as_pairs(changes) == [("a.txt", ChangeType.MODIFIED)]
    assert changes[0].old.sha256 == "h1"
    assert changes[0].new.sha256 == "h2"
