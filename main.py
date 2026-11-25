#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Entry for make.fun's "One Star for Monday" bounty.

The program writes one line to the output directory's entry.txt: a
one-star review of Monday written as if Monday were a restaurant.
It is built as a real diner's complaint -- seated before coffee,
served cold toast and a table full of meetings -- and lands on the
Monday-specific punch: the whole weekend charged as the bill.
"""

import os
from pathlib import Path

TEXT = (
    "One star: Monday seated me before coffee, served cold toast and a "
    "table full of meetings, then charged my whole weekend as the bill."
)


def main() -> None:
    # The bounty's gate: UTF-8 text of 1 to 180 characters, not only
    # white space; the task also caps the line at 25 words. Fail loudly
    # rather than hand in a text the gate would refuse.
    if not 1 <= len(TEXT) <= 180 or not TEXT.strip():
        raise SystemExit("entry text is outside the 1-180 character gate")
    if len(TEXT.split()) > 25:
        raise SystemExit("entry text exceeds the 25-word cap")
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output.mkdir(parents=True, exist_ok=True)
    (output / "entry.txt").write_text(TEXT, encoding="utf-8")


if __name__ == "__main__":
    main()
