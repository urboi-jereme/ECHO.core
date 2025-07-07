import sqlite3
import types
from pathlib import Path
from universalCode.echo_core.symbolic import symbolic_daemon as sd


def test_init_and_store(tmp_path, monkeypatch):
    db = tmp_path / 'test.db'
    monkeypatch.setattr(sd, 'DB_NAME', str(db))
    sd.init_db()
    sd.store_statement('s', ['recursion'], 'recursive balance', 'ref', 1)
    with sqlite3.connect(db) as conn:
        cur = conn.execute('SELECT original FROM statements')
        rows = cur.fetchall()
        assert rows and rows[0][0] == 's'


def test_daemon_loop_iteration(monkeypatch, tmp_path):
    db = tmp_path / 'loop.db'
    monkeypatch.setattr(sd, 'DB_NAME', str(db))
    calls = []
    monkeypatch.setattr(sd, 'generate_seed_statement', lambda: 'seed')
    monkeypatch.setattr(sd, 'decompose', lambda s: ['recursion'])
    monkeypatch.setattr(sd, 'identify_motif', lambda b: 'recursive balance')
    monkeypatch.setattr(sd, 'refine', lambda s, b, m: ('ref', 1))
    def fake_sleep(t):
        calls.append(t)
        raise KeyboardInterrupt
    monkeypatch.setattr(sd.time, 'sleep', fake_sleep)
    sd.init_db()
    try:
        sd.daemon_loop()
    except KeyboardInterrupt:
        pass
    assert calls
