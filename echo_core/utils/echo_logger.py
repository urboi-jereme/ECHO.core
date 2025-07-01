"""Logging helpers for agent activations and custom events."""

from pathlib import Path
from datetime import datetime
import os

import sys
import os
from datetime import datetime


try:
    yaml = __import__("yaml")
except Exception:  # pragma: no cover - optional dependency
    yaml = None

# Paths relative to repository root
ROOT_DIR = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT_DIR / "journal" / "ECHO_LOG.md"
AGENT_STATE_PATH = ROOT_DIR / "AGENT_STATE.yaml"

# Root dir setup
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

LOG_PATH = os.path.join(ROOT_DIR, "journal", "ECHO_LOG.md")
AGENT_STATE_PATH = os.path.join(ROOT_DIR, "AGENT_STATE.yaml")

# Optional .env loading for toggles
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT_DIR, ".env"))
except ImportError:
    pass  # .env optional

def _init_log():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            f.write("# 🧠 ECHO Activity Log\n\n")

def _logging_enabled():
    if yaml is None:
        return True
    try:
        with open(AGENT_STATE_PATH, "r") as f:
            state = yaml.safe_load(f) or {}
        return state.get("log_on_activation", True)
    except Exception:
        return True

def log_agent_activation(agent_name: str, action: str = "activated", reason: str = None, tag: str = None, motif: str = None):
    if not _logging_enabled():
        return
    _init_log()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    metadata = []
    if reason: metadata.append(f"Reason: {reason}")
    if tag: metadata.append(f"Tag: {tag}")
    if motif: metadata.append(f"Motif: {motif}")
    meta_str = f" ({' | '.join(metadata)})" if metadata else ""
    entry = f"- [{timestamp}] **{agent_name}** {action}{meta_str}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)

def log_custom_event(event: str):
    _init_log()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"- [{timestamp}] {event}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)

# 🧠 Optional patch injection
