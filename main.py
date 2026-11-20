#!/usr/bin/env python3
"""news-image-20261119 entry (v3): deliver the front page to /output/entry.png.

The front page is bundled beside this script as entry.png: a newspaper
page drawn in-session for Thursday 19 November 2026, carrying twenty
verified stories from the full day (one lead, three illustrated
secondaries, eight in the grid, eight briefs) plus a source line.
This program never changes the image: it checks the bundled file is a
complete, well-formed PNG of the size the competition allows, copies it
byte-for-byte to the output path, and then proves the copy matches the
source by hash. It uses only the standard library, reads no network,
clock or random input, and writes the same bytes on every run.

Output directory: /output by default, or $MAKEFUN_OUTPUT_DIR when set
(the kit's local-run convention).

Checks, in order:
  1. The bundled file starts with the PNG signature.
  2. Its size is at most 1 MiB.
  3. Every chunk in the stream is well-formed (length, type, payload,
     CRC) and the stream ends with an IEND chunk as its last bytes.
  4. The first chunk is IHDR declaring 1024x1024.
After the copy, the destination's SHA-256 must equal the source's; on
any mismatch the destination is removed and the run fails.
"""
import hashlib
import os
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                    "entry.png")

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
SIZE = (1024, 1024)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def check_png(path):
    """Validate the whole PNG chunk stream; return (width, height)."""
    with open(path, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        raise ValueError("%s: %d bytes, over the 1 MiB limit"
                         % (path, len(data)))
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("%s: bad PNG signature" % path)
    pos = 8
    first = True
    width = height = None
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("%s: truncated chunk header at %d" % (path, pos))
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + length + 4
        if end > len(data):
            raise ValueError("%s: truncated %s chunk at %d"
                             % (path, ctype.decode("latin-1"), pos))
        if first:
            if ctype != b"IHDR" or length != 13:
                raise ValueError("%s: first chunk is not a 13-byte IHDR"
                                 % path)
            width, height = struct.unpack(">II", data[pos + 8:pos + 16])
            if (width, height) != SIZE:
                raise ValueError("%s: expected 1024x1024, got %dx%d"
                                 % (path, width, height))
            first = False
        stored_crc, = struct.unpack(">I", data[end - 4:end])
        actual_crc = zlib.crc32(ctype)
        actual_crc = zlib.crc32(data[pos + 8:pos + 8 + length], actual_crc)
        if stored_crc != (actual_crc & 0xFFFFFFFF):
            raise ValueError("%s: bad CRC in %s chunk at %d"
                             % (path, ctype.decode("latin-1"), pos))
        if ctype == b"IEND":
            if length != 0:
                raise ValueError("%s: IEND carries data" % path)
            if end != len(data):
                raise ValueError("%s: %d bytes after IEND"
                                 % (path, len(data) - end))
            return width, height
        pos = end
    raise ValueError("%s: no IEND chunk (truncated file)" % path)


def main():
    width, height = check_png(SOURCE)
    digest = sha256_of(SOURCE)
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    if sha256_of(DEST) != digest:
        os.unlink(DEST)
        raise RuntimeError("%s: copy failed its integrity check" % DEST)
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (DEST, os.path.getsize(DEST), width, height, digest))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        print("error: %s" % error, file=sys.stderr)
        raise SystemExit(1)
