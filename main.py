#!/usr/bin/env python3
"""news-image-20261119 entry: write the front page to /output/entry.png.

Deterministic by design: it copies the bundled ``entry.png`` byte-for-byte,
with no network access and no randomness, so repeated runs write identical
bytes. The image itself is a newspaper front page summing up the world news
of Thursday 19 November 2026 (see README.md for the eight verified stories).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main() -> None:
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("wrote %s (%d bytes)" % (DST, os.path.getsize(DST)))


if __name__ == "__main__":
    main()
