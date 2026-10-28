"""Calculates the SHA-256 hash of a file.

Owner: Donald. Branch: feature/hasher
"""

import hashlib

# 64 KB per read is a good balance between speed and memory
CHUNK_SIZE = 64 * 1024


def hash_file(path, chunk_size=CHUNK_SIZE):
    """Return the sha256 of a file as a hex string.

    The file is read piece by piece, so a huge file does not have to
    fit into memory. OSError (missing file, no permission) is not caught
    here on purpose, the scanner decides what to do with it.
    """
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:  # empty bytes means end of file
                break
            sha.update(chunk)
    return sha.hexdigest()
