# symbolic_daemon.py v0.3.1
"""Background loop persisting symbolic statements into SQLite."""

import os
import random
import sqlite3
import time
from datetime import datetime

from symbolic_utils import decompose, refine, identify_motif

DB_NAME = os.getenv("SYMBOLIC_DB", "symbolic_language.db")

# -------------------------------
# DB INIT
# -------------------------------
def init_db() -> None:
    """Create the ``statements`` table if it doesn't exist."""

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS statements (
                id INTEGER PRIMARY KEY,
                original TEXT,
                base_symbols TEXT,
                motif TEXT,
                refined TEXT,
                compression_level INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )"""
        )

# -------------------------------
# STORE FUNCTION
# -------------------------------
def store_statement(
    original: str, base_symbols: list[str], motif: str, refined: str, level: int
) -> None:
    """Insert a symbolic statement record into the database."""

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """INSERT INTO statements
                (original, base_symbols, motif, refined, compression_level)
                VALUES (?, ?, ?, ?, ?)""",
            (original, ",".join(base_symbols), motif, refined, level),
        )

# -------------------------------
# SEED GENERATOR (TEMPORARY)
# -------------------------------
def generate_seed_statement() -> str:
    """Return a pseudo-random seed statement."""

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
def daemon_loop() -> None:
    """Continuously generate and store refined symbolic statements."""

    while True:
        seed = generate_seed_statement()
        base = decompose(seed)
        motif = identify_motif(base)
        refined, level = refine(seed, base, motif)
        store_statement(seed, base, motif, refined, level)
        print(f"[{datetime.now()}] Stored: {refined} [Level: {level}]")
        time.sleep(10)  # adjustable cycle rate

# -------------------------------
if __name__ == "__main__":
    init_db()
    daemon_loop()
