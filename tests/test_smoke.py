"""Very first tests, just to check the package imports and the models work.

More tests are added together with every module.
"""

import fim
from fim.models import Change, ChangeType, FileRecord


def test_package_has_version():
    assert fim.__version__ == "0.1.0"


def test_file_record_stores_values():
    rec = FileRecord(path="a.txt", sha256="abc", size=3, mtime=1.0, mode=0o644)
    assert rec.path == "a.txt"
    assert rec.size == 3


def test_added_change_has_no_old_record():
    rec = FileRecord(path="a.txt", sha256="abc", size=3, mtime=1.0, mode=0o644)
    change = Change(path="a.txt", type=ChangeType.ADDED, new=rec)
    assert change.old is None
    assert change.type == ChangeType.ADDED
