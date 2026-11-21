#!/usr/bin/env python3
"""make.fun entry: news-image-20261121 (Manja lane).

One page that sums up Saturday 21 November 2026's world news in a
single image.

The picture is baked into this repo at assets/entry.png — it was drawn
in advance by render.py from the stories in data/news.json. This script
does nothing creative: it copies that exact file to /output/entry.png
and, before exiting, proves the copy is a well-formed PNG inside the
bounty's limits (no more than 1024x1024 pixels, no more than 1 MiB)
and byte-for-byte identical to the baked original.

Standard library only. No network, no clock, no randomness: run it
twice and /output/entry.png comes out identical both times.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "assets" / "entry.png"
DEST = Path("/output/entry.png")

SIDE_LIMIT = 1024
BYTES_LIMIT = 1024 * 1024  # 1 MiB
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def sha256_file(path: Path) -> str:
    """Hex SHA-256 of a file, read in 64 KiB slices."""
    summer = hashlib.sha256()
    with path.open("rb") as stream:
        while (chunk := stream.read(65536)):
            summer.update(chunk)
    return summer.hexdigest()


def next_chunk(stream) -> tuple[int, bytes] | None:
    """Read one PNG chunk header: (payload length, 4-byte type).

    Returns None at end of file instead of raising, so the caller can
    report a missing IHDR in its own words.
    """
    header = stream.read(8)
    if len(header) < 8:
        return None
    return int.from_bytes(header[:4], "big"), header[4:]


def read_png_size(path: Path) -> tuple[int, int]:
    """Return (width, height) of a PNG by walking its chunk headers.

    The 8-byte signature is checked first, then each chunk is stepped
    over (length, type, payload, CRC) until the IHDR chunk turns up, so
    a coincidental IHDR-looking byte run elsewhere cannot be mistaken
    for the header.
    """
    with path.open("rb") as stream:
        if stream.read(8) != SIGNATURE:
            raise ValueError("not a PNG: bad signature")
        while True:
            header = next_chunk(stream)
            if header is None:
                raise ValueError("IHDR chunk not found before end of file")
            length, kind = header
            if kind == b"IHDR":
                body = stream.read(13)
                if len(body) < 13:
                    raise ValueError("truncated IHDR chunk")
                width = int.from_bytes(body[:4], "big")
                height = int.from_bytes(body[4:8], "big")
                return width, height
            stream.seek(length + 4, os.SEEK_CUR)


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def run() -> int:
    if not SOURCE.is_file():
        return fail(f"baked image missing: {SOURCE}")

    try:
        width, height = read_png_size(SOURCE)
    except ValueError as exc:
        return fail(str(exc))

    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        return fail(
            f"image is {width}x{height}, over the "
            f"{SIDE_LIMIT}x{SIDE_LIMIT} limit"
        )

    size = SOURCE.stat().st_size
    if size > BYTES_LIMIT:
        return fail(f"image is {size} bytes, over the 1 MiB limit")

    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(SOURCE.read_bytes())

    if sha256_file(SOURCE) != sha256_file(DEST):
        return fail("output differs from the baked image")

    out_width, out_height = read_png_size(DEST)
    if (out_width, out_height) != (width, height):
        return fail("output dimensions differ from the baked image")

    print(
        f"wrote {DEST} — {width}x{height}, {size} bytes, "
        f"sha256 {sha256_file(DEST)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
