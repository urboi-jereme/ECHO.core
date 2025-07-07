# File: agents/emergence_scanner.py
"""Agent wrapper around runtime.emergence_tracker.check_emergence."""

from pathlib import Path

from echo_core.utils.yaml_utils import load
from echo_core.runtime.emergence_tracker import check_emergence, LOG_PATH


class EmergenceScanner:
    def __init__(self, log_path: str | None = None):
        self.log_path = log_path or LOG_PATH

    def scan(self):
        base = Path(__file__).resolve().parents[3] / "memory"
        memory = load(base / "ECHO_MEMORY.yaml", fallback={"echo_memory": []}).get("echo_memory", [])
        goals = load(base / "GOALS.yaml", fallback=[]) or []
        beliefs = load(base / "BELIEFS.yaml", fallback={"beliefs": []}).get("beliefs", [])
        original = LOG_PATH
        if self.log_path != LOG_PATH:
            from echo_core.runtime import emergence_tracker
            emergence_tracker.LOG_PATH = self.log_path
        try:
            return check_emergence(memory, goals, beliefs)
        finally:
            if self.log_path != original:
                from echo_core.runtime import emergence_tracker
                emergence_tracker.LOG_PATH = original
