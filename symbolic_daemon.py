import sqlite3
import time
import random
from datetime import datetime
from symbolic_utils import decompose, refine, identify_motif

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
    conn.commit()
    conn.close()

# -------------------------------
# STORE FUNCTION
# -------------------------------
def store_statement(original, base_symbols, motif, refined, level):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO statements 
                 (original, base_symbols, motif, refined, compression_level)
                 VALUES (?, ?, ?, ?, ?)''',
              (original, ",".join(base_symbols), motif, refined, level))
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
        motif = identify_motif(base)
        refined, level = refine(seed, base, motif)
        store_statement(seed, base, motif, refined, level)
        print(f"[{datetime.now()}] Stored: {refined} [Level: {level}]")
        time.sleep(10)  # adjustable cycle rate

# -------------------------------
if __name__ == "__main__":
    init_db()
    daemon_loop()
