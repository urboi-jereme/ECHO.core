# File: agents/emergence_scanner.py
"""Agent wrapper around runtime.emergence_tracker.check_emergence."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from yaml_utils import load
from runtime.emergence_tracker import check_emergence, LOG_PATH


class EmergenceScanner:
    def __init__(self, log_path: str | None = None):
        self.log_path = log_path or LOG_PATH

    def scan(self):
        memory = load("memory/ECHO_MEMORY.yaml", fallback={"echo_memory": []}).get("echo_memory", [])
        goals = load("memory/GOALS.yaml", fallback=[]) or []
        beliefs = load("memory/BELIEFS.yaml", fallback={"beliefs": []}).get("beliefs", [])
        original = LOG_PATH
        if self.log_path != LOG_PATH:
            from runtime import emergence_tracker
            emergence_tracker.LOG_PATH = self.log_path
        try:
            return check_emergence(memory, goals, beliefs)
        finally:
            if self.log_path != original:
                from runtime import emergence_tracker
                emergence_tracker.LOG_PATH = original
