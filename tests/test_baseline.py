"""Tests for fim.baseline"""

import json

import pytest

from fim.baseline import BaselineError, load_baseline, save_baseline
from fim.models import FileRecord


def sample_records():
    return {
        "a.txt": FileRecord("a.txt", "aa11", 3, 100.5, 0o644),
        "sub/b.txt": FileRecord("sub/b.txt", "bb22", 7, 200.0, 0o600),
    }


def test_save_then_load_gives_same_data(tmp_path):
    path = tmp_path / "baseline.json"
    records = sample_records()
    save_baseline(records, path)
    assert load_baseline(path) == records


def test_empty_baseline(tmp_path):
    path = tmp_path / "baseline.json"
    save_baseline({}, path)
    assert load_baseline(path) == {}


def test_file_contains_version(tmp_path):
    path = tmp_path / "baseline.json"
    save_baseline(sample_records(), path)
    data = json.loads(path.read_text())
    assert data["version"] == 1
    assert "created" in data


def test_overwrite_old_baseline(tmp_path):
    path = tmp_path / "baseline.json"
    save_baseline(sample_records(), path)
    save_baseline({}, path)
    assert load_baseline(path) == {}
    # no temp file should stay behind
    assert not (tmp_path / "baseline.json.tmp").exists()
