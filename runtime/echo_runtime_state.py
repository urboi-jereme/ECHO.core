# runtime/echo_runtime_state.py

import json
import time
from pathlib import Path

STATE_PATH = Path("runtime/echo_state_log.json")

def log_event(agent: str, event_type: str, detail: str):
    event = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent,
        "type": event_type,
        "detail": detail
    }
    log = []
    if STATE_PATH.exists():
        try:
            log = json.loads(STATE_PATH.read_text())
        except Exception:
            log = []
    log.append(event)
    STATE_PATH.write_text(json.dumps(log[-100:], indent=2))  # keep last 100 events
