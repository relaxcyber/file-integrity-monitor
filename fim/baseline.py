"""Saves the baseline to a JSON file and loads it back.

Owner: Donald. Branch: feature/baseline

File format:
{
  "version": 1,
  "created": "2026-10-28T12:00:00",
  "files": { "a.txt": {"path": ..., "sha256": ..., "size": ..., ...} }
}
"""

import json
import os
from dataclasses import asdict
from datetime import datetime

from fim.models import FileRecord

FORMAT_VERSION = 1


class BaselineError(Exception):
    """The baseline file is missing, broken or has an unknown format."""


def save_baseline(records, path):
    """Write a dict {rel path: FileRecord} to a json file."""
    data = {
        "version": FORMAT_VERSION,
        "created": datetime.now().isoformat(timespec="seconds"),
        "files": {rel: asdict(rec) for rel, rec in records.items()},
    }
    # write to a temp file first and then rename, so a crash in the middle
    # of writing can not leave us with a half written baseline
    tmp_path = str(path) + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)


def load_baseline(path):
    """Read the json file and return a dict {rel path: FileRecord}.

    Raises BaselineError with a readable message if anything is wrong.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise BaselineError(f"baseline not found: {path} (run 'init' first)")
    except json.JSONDecodeError as err:
        raise BaselineError(f"baseline is not valid json: {err}")

    if not isinstance(data, dict) or data.get("version") != FORMAT_VERSION:
        raise BaselineError("unknown baseline format or version")

    try:
        return {rel: FileRecord(**fields) for rel, fields in data["files"].items()}
    except (KeyError, TypeError) as err:
        raise BaselineError(f"baseline has wrong structure: {err}")
