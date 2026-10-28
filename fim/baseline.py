"""Saves the baseline to a JSON file and loads it back.

Owner: Donald. Branch: feature/baseline
"""

import json
from dataclasses import asdict

from fim.models import FileRecord


def save_baseline(records, path):
    """Write a dict {rel path: FileRecord} to a json file."""
    data = {rel: asdict(rec) for rel, rec in records.items()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_baseline(path):
    """Read the json file and return a dict {rel path: FileRecord}."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {rel: FileRecord(**fields) for rel, fields in data.items()}
