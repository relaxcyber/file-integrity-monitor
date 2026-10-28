"""Tests for fim.scanner"""

import os

import pytest

from fim import scanner
from fim.hasher import hash_file
from fim.scanner import scan


def make_tree(base):
    """Small folder structure used in several tests."""
    (base / "a.txt").write_text("aaa")
    (base / "sub").mkdir()
    (base / "sub" / "b.txt").write_text("bbb")
    (base / "sub" / "deep").mkdir()
    (base / "sub" / "deep" / "c.txt").write_text("ccc")


def test_finds_all_files(tmp_path):
    make_tree(tmp_path)
    result = scan(tmp_path)
    assert sorted(result) == ["a.txt", "sub/b.txt", "sub/deep/c.txt"]


def test_record_has_correct_values(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("hello")
    rec = scan(tmp_path)["a.txt"]
    assert rec.size == 5
    assert rec.sha256 == hash_file(f)
    assert rec.path == "a.txt"


def test_empty_folder(tmp_path):
    assert scan(tmp_path) == {}


def test_not_a_folder_raises(tmp_path):
    with pytest.raises(NotADirectoryError):
        scan(tmp_path / "does_not_exist")


def test_ignore_file(tmp_path):
    make_tree(tmp_path)
    result = scan(tmp_path, ignore=lambda rel: rel.endswith("b.txt"))
    assert "sub/b.txt" not in result
    assert "a.txt" in result


def test_ignore_folder_skips_everything_inside(tmp_path):
    make_tree(tmp_path)
    result = scan(tmp_path, ignore=lambda rel: rel == "sub")
    assert list(result) == ["a.txt"]


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="no symlink support")
def test_symlink_is_skipped(tmp_path):
    (tmp_path / "real.txt").write_text("data")
    try:
        os.symlink(tmp_path / "real.txt", tmp_path / "link.txt")
    except OSError:
        pytest.skip("not allowed to create symlinks here")
    assert list(scan(tmp_path)) == ["real.txt"]


def test_unreadable_file_is_skipped(tmp_path, monkeypatch):
    (tmp_path / "good.txt").write_text("ok")
    (tmp_path / "bad.txt").write_text("secret")

    real_hash = scanner.hash_file

    def fake_hash(path, *args, **kwargs):
        # pretend one file has no read permission
        # (chmod does not work for root, so we fake it)
        if path.name == "bad.txt":
            raise PermissionError("denied")
        return real_hash(path, *args, **kwargs)

    monkeypatch.setattr(scanner, "hash_file", fake_hash)
    assert list(scan(tmp_path)) == ["good.txt"]
