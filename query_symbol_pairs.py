# query_symbol_pairs.py v0.3.1
"""Query statement pairs sharing a motif in ``symbolic_language.db``."""

from __future__ import annotations

import argparse
import sqlite3
from typing import Iterator, Tuple

DB_NAME = "symbolic_language.db"


def iter_pairs(motif: str) -> Iterator[Tuple[str, str]]:
    """Yield pairs of original statements with the given motif."""
    query = (
        "SELECT s1.original, s2.original FROM statements s1 "
        "JOIN statements s2 ON s1.motif = s2.motif "
        "WHERE s1.motif = ? AND s1.id < s2.id"
    )
    with sqlite3.connect(DB_NAME) as conn:
        for row in conn.execute(query, (motif,)):
            yield row[0], row[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Query symbolic statement pairs")
    parser.add_argument("motif", help="Motif to search for")
    args = parser.parse_args()
    for a, b in iter_pairs(args.motif):
        print(f"{a} <-> {b}")


if __name__ == "__main__":
    main()

