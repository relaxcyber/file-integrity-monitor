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


def test_permissions_changed():
    old = {"run.sh": rec("run.sh", mode=0o644)}
    new = {"run.sh": rec("run.sh", mode=0o777)}
    assert as_pairs(compare(old, new)) == [("run.sh", ChangeType.PERMISSIONS)]


def test_only_mtime_changed_is_not_a_change():
    old = {"a.txt": rec("a.txt", mtime=1.0)}
    new = {"a.txt": rec("a.txt", mtime=999.0)}
    assert compare(old, new) == []


def test_content_and_permissions_give_two_changes():
    old = {"a.sh": rec("a.sh", sha="h1", mode=0o644)}
    new = {"a.sh": rec("a.sh", sha="h2", mode=0o755)}
    types = {ch.type for ch in compare(old, new)}
    assert types == {ChangeType.MODIFIED, ChangeType.PERMISSIONS}


def test_result_is_sorted_by_path():
    old = {"z.txt": rec("z.txt"), "m.txt": rec("m.txt")}
    new = {"b.txt": rec("b.txt"), "m.txt": rec("m.txt", sha="other")}
    paths = [ch.path for ch in compare(old, new)]
    assert paths == ["b.txt", "m.txt", "z.txt"]


def test_everything_at_once():
    old = {
        "keep.txt": rec("keep.txt"),
        "edit.txt": rec("edit.txt", sha="old"),
        "gone.txt": rec("gone.txt"),
    }
    new = {
        "keep.txt": rec("keep.txt"),
        "edit.txt": rec("edit.txt", sha="new"),
        "fresh.txt": rec("fresh.txt"),
    }
    assert as_pairs(compare(old, new)) == [
        ("edit.txt", ChangeType.MODIFIED),
        ("fresh.txt", ChangeType.ADDED),
        ("gone.txt", ChangeType.DELETED),
    ]
