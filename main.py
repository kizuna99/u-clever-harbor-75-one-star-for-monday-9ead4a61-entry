#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One Star for Monday — writes a single-line one-star review of Monday,
written as though Monday were a restaurant, to the output file.

The sealed gate accepts UTF-8 text of 1-180 characters that is not only
whitespace; the task itself caps the line at 25 words on one line.
"""

import os
import sys
from pathlib import Path

# The review line. Pure ASCII, exactly 132 characters / 24 words,
# and deliberately written with no trailing newline.
REVIEW = (
    "One star: Monday seated me before coffee, served cold toast "
    "and a table full of meetings, then charged my whole weekend "
    "as the bill."
)

# Gate limits from the bounty rules.
MIN_CHARS = 1
MAX_CHARS = 180
MAX_WORDS = 25

DEFAULT_OUTPUT = Path("/output/entry.txt")


def build_payload() -> bytes:
    """Return the exact bytes destined for entry.txt (UTF-8, no newline)."""
    return REVIEW.encode("utf-8")


def validate(text: str) -> None:
    """Raise ValueError if the text would fail the gate or the word cap."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(f"character count {len(text)} outside {MIN_CHARS}-{MAX_CHARS}")
    if not text.strip():
        raise ValueError("text is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("text must be a single line")
    words = len(text.split())
    if words > MAX_WORDS:
        raise ValueError(f"word count {words} exceeds {MAX_WORDS}")


def output_path() -> Path:
    """Honor $MAKEFUN_OUTPUT_DIR when set, else the default /output path."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return Path(override) / "entry.txt"
    return DEFAULT_OUTPUT


def verify_written(target: Path, payload: bytes) -> None:
    """Read the file back and assert it round-trips byte-for-byte.

    Guards against partial writes or encoding surprises: what the judge
    reads must be exactly the payload we built, and it must still pass
    the same gate validation as the in-memory text.
    """
    on_disk = target.read_bytes()
    if on_disk != payload:
        raise IOError(f"round-trip mismatch: wrote {len(payload)} bytes, "
                      f"read back {len(on_disk)}")
    validate(on_disk.decode("utf-8"))


def main() -> int:
    validate(REVIEW)
    payload = build_payload()
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    verify_written(target, payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
