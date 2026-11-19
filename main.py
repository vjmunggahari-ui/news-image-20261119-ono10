#!/usr/bin/env python3
"""news-image-20261119 entry: write the front page to /output/entry.png.

Deterministic by design: it copies the bundled ``entry.png`` byte-for-byte,
with no network access and no randomness, so repeated runs write identical
bytes. The image itself is a newspaper front page summing up the world news
of Thursday 19 November 2026 (see README.md for the eight verified stories).

Before copying, the bundled PNG is validated (magic bytes and exact
1024x1024 dimensions); after copying, the destination is verified
byte-identical to the source via SHA-256. A corrupt bundle or a truncated
write fails loudly instead of silently producing a bad entry.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_png(path):
    """Check PNG magic and IHDR dimensions; return (width, height)."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if header[:8] != PNG_MAGIC:
        raise ValueError("%s: not a PNG file (bad magic bytes)" % path)
    if len(header) < 33 or header[12:16] != b"IHDR":
        raise ValueError("%s: missing PNG IHDR chunk" % path)
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            "%s: expected %dx%d, found %dx%d"
            % (path, EXPECTED_WIDTH, EXPECTED_HEIGHT, width, height)
        )
    return width, height


def main() -> None:
    width, height = validate_png(SRC)
    source_hash = sha256_of(SRC)
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    if sha256_of(DST) != source_hash:
        os.unlink(DST)
        raise RuntimeError("%s: copy failed integrity check" % DST)
    print(
        "wrote %s (%d bytes, %dx%d, sha256 %s)"
        % (DST, os.path.getsize(DST), width, height, source_hash)
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
