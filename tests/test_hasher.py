"""Tests for fim.hasher"""

import hashlib

import pytest

from fim.hasher import hash_file


def test_known_value(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_bytes(b"hello")
    # sha256 of "hello", checked with an online calculator
    expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    assert hash_file(f) == expected


def test_same_content_same_hash(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"same text")
    b.write_bytes(b"same text")
    assert hash_file(a) == hash_file(b)


def test_one_byte_changes_hash(tmp_path):
    f = tmp_path / "x.txt"
    f.write_bytes(b"version 1")
    before = hash_file(f)
    f.write_bytes(b"version 2")
    assert hash_file(f) != before


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        hash_file(tmp_path / "nope.txt")
