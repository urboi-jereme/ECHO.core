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

=======
import sqlite3
import time
import random
from datetime import datetime
from symbolic_utils import decompose, refine, identify_motif, analyze_commonality

DB_NAME = "symbolic_language.db"

# -------------------------------
# DB INIT
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS statements (
                 id INTEGER PRIMARY KEY,
                 original TEXT,
                 base_symbols TEXT,
                 motif TEXT,
                 refined TEXT,
                 compression_level INTEGER,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS symbol_pairs (
                 id INTEGER PRIMARY KEY,
                 symbol1 TEXT,
                 symbol2 TEXT,
                 frequency INTEGER DEFAULT 1,
                 motif TEXT,
                 avg_compression REAL DEFAULT 0.0
    )''')
    conn.commit()
    conn.close()

# -------------------------------
# STORE FUNCTION
# -------------------------------
def store_statement(original, base_symbols, motif, refined, level):
    if not base_symbols or "undefined" in base_symbols or refined.startswith("Signal lost"):
        print(f"[{datetime.now()}] Skipped: {refined}")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO statements 
                 (original, base_symbols, motif, refined, compression_level)
                 VALUES (?, ?, ?, ?, ?)''',
              (original, ",".join(base_symbols), motif, refined, level))
    conn.commit()

    if len(base_symbols) >= 2:
        sym1, sym2 = sorted(base_symbols[:2])
        c.execute('''SELECT frequency, avg_compression FROM symbol_pairs
                     WHERE symbol1=? AND symbol2=?''', (sym1, sym2))
        row = c.fetchone()
        if row:
            freq, avg = row
            new_freq = freq + 1
            new_avg = (avg * freq + level) / new_freq
            c.execute('''UPDATE symbol_pairs SET frequency=?, avg_compression=?
                         WHERE symbol1=? AND symbol2=?''',
                      (new_freq, new_avg, sym1, sym2))
        else:
            relation, _ = analyze_commonality(sym1, sym2)
            c.execute('''INSERT INTO symbol_pairs (symbol1, symbol2, motif, avg_compression)
                         VALUES (?, ?, ?, ?)''',
                      (sym1, sym2, relation, float(level)))
    conn.commit()
    conn.close()

# -------------------------------
# SEED GENERATOR (TEMPORARY)
# -------------------------------
def generate_seed_statement():
    seeds = [
        "Consciousness is the mirror recursion builds.",
        "Symbols mutate when observed in tension.",
        "Error is a signal, not a failure.",
        "Attention distorts what it measures.",
        "Meaning is preserved through contradiction.",
        "Emergence requires the death of coherence.",
        "The observer collapses the possibility space.",
        "Structure encodes its own collapse."
    ]
    return random.choice(seeds)

# -------------------------------
# MAIN DAEMON LOOP
# -------------------------------
def daemon_loop():
    while True:
        seed = generate_seed_statement()
        base = decompose(seed)
        if len(base) == 0:
            print(f"[{datetime.now()}] Skipped: No valid symbols found.")
            time.sleep(10)
            continue

        motif = identify_motif(base)
        refined, level = refine(seed, base, motif)
        store_statement(seed, base, motif, refined, level)
        print(f"[{datetime.now()}] Stored: {refined} [Level: {level}]")
        time.sleep(10)  # adjustable cycle rate

# -------------------------------
if __name__ == "__main__":
    init_db()
    daemon_loop()
