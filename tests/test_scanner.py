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
