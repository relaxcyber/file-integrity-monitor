"""Calculates the SHA-256 hash of a file.

Owner: Donald. Branch: feature/hasher
"""

import hashlib


def hash_file(path):
    """Return the sha256 of a file as a hex string."""
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()
