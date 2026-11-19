#!/usr/bin/env python3
"""news-image-20261119 entry: place the front page at /output/entry.png.

The entry image is bundled next to this script. This program never edits
the image: it inspects the bundled file, copies it byte-for-byte to the
output location, and then proves the copy is identical. Nothing here needs
the network, the clock, or any random input, so every run produces the
same bytes at the destination.

The image is a newspaper front page summing up the world news of
Thursday 19 November 2026; the eight stories it carries are listed in
README.md. The checks below are structural only -- they confirm the
file is a complete, correctly sized PNG, not that any pixel changed.

Validation, in order:
  1. The first eight bytes are the PNG signature.
  2. The chunk stream is walked from start to finish: every chunk has a
     well-formed length, type, payload and CRC field, and the stream ends
     with an IEND chunk that is the last thing in the file. A file cut
     short mid-stream, or one missing its terminator, is rejected here --
     the old header-only check could not see that.
  3. The first chunk is IHDR and declares 1024x1024, the size the
     competition expects.
After the copy, the destination is hashed and compared with the source;
any mismatch deletes the destination and fails loudly.
"""
import hashlib
import os
import shutil
import struct
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(SCRIPT_DIR, "entry.png")
DEST_PATH = "/output/entry.png"

SIGNATURE = b"\x89PNG\r\n\x1a\n"
WANTED_WIDTH = 1024
WANTED_HEIGHT = 1024
CHUNK_HEADER_LEN = 8   # 4 bytes length + 4 bytes type
CHUNK_TRAILER_LEN = 4  # 4 bytes CRC


def file_sha256(path):
    """SHA-256 hex digest of a file, read in fixed-size blocks."""
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(65536)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def inspect_png(path):
    """Walk the whole PNG chunk stream; return (width, height).

    Raises ValueError on a bad signature, a malformed chunk, a missing
    or misplaced IHDR, wrong dimensions, a missing IEND chunk, or any
    bytes after IEND.
    """
    with open(path, "rb") as stream:
        blob = stream.read()

    if blob[: len(SIGNATURE)] != SIGNATURE:
        raise ValueError("%s: not a PNG file (bad signature)" % path)

    offset = len(SIGNATURE)
    first_chunk = True
    width = height = None
    saw_iend = False

    while offset < len(blob):
        if offset + CHUNK_HEADER_LEN > len(blob):
            raise ValueError(
                "%s: truncated chunk header at byte %d" % (path, offset)
            )
        payload_len, chunk_type = struct.unpack(
            ">I4s", blob[offset : offset + CHUNK_HEADER_LEN]
        )
        chunk_end = offset + CHUNK_HEADER_LEN + payload_len + CHUNK_TRAILER_LEN
        if chunk_end > len(blob):
            raise ValueError(
                "%s: truncated %r chunk at byte %d"
                % (path, chunk_type.decode("latin-1"), offset)
            )
        if first_chunk:
            if chunk_type != b"IHDR":
                raise ValueError("%s: first chunk is not IHDR" % path)
            if payload_len != 13:
                raise ValueError("%s: IHDR has wrong length" % path)
            width, height = struct.unpack(
                ">II", blob[offset + CHUNK_HEADER_LEN : offset + CHUNK_HEADER_LEN + 8]
            )
            if (width, height) != (WANTED_WIDTH, WANTED_HEIGHT):
                raise ValueError(
                    "%s: expected %dx%d, found %dx%d"
                    % (path, WANTED_WIDTH, WANTED_HEIGHT, width, height)
                )
            first_chunk = False
        if chunk_type == b"IEND":
            if payload_len != 0:
                raise ValueError("%s: IEND chunk carries data" % path)
            if chunk_end != len(blob):
                raise ValueError(
                    "%s: %d trailing bytes after IEND"
                    % (path, len(blob) - chunk_end)
                )
            saw_iend = True
            break
        offset = chunk_end

    if first_chunk:
        raise ValueError("%s: no chunks after the signature" % path)
    if not saw_iend:
        raise ValueError("%s: missing trailing IEND chunk (truncated file)" % path)
    return width, height


def run():
    width, height = inspect_png(SOURCE_PATH)
    source_digest = file_sha256(SOURCE_PATH)

    os.makedirs(os.path.dirname(DEST_PATH), exist_ok=True)
    shutil.copyfile(SOURCE_PATH, DEST_PATH)
    if file_sha256(DEST_PATH) != source_digest:
        os.unlink(DEST_PATH)
        raise RuntimeError("%s: copy failed integrity check" % DEST_PATH)

    print(
        "wrote %s (%d bytes, %dx%d, sha256 %s)"
        % (DEST_PATH, os.path.getsize(DEST_PATH), width, height, source_digest)
    )


if __name__ == "__main__":
    try:
        run()
    except (OSError, ValueError, RuntimeError) as problem:
        print("error: %s" % problem, file=sys.stderr)
        raise SystemExit(1)
