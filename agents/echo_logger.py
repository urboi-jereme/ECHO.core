import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime
yaml = __import__("yaml")

LOG_PATH = os.path.join(os.path.dirname(__file__), "journal", "ECHO_LOG.md")
AGENT_STATE_PATH = os.path.join(os.path.dirname(__file__), "AGENT_STATE.yaml")

def _init_log():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            f.write("# 🧠 ECHO Activity Log\n\n")

def _logging_enabled():
    try:
        with open(AGENT_STATE_PATH, "r") as f:
            state = yaml.safe_load(f)
            return state.get("log_on_activation", True)
    except Exception:
        return True  # Default to logging if file missing or corrupted

def log_agent_activation(agent_name: str, action: str = "activated"):
    if not _logging_enabled():
        return
    _init_log()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"- [{timestamp}] **{agent_name}** {action}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)

def log_custom_event(event: str):
    _init_log()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"- [{timestamp}] {event}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)

# Auto-inject logging into agent __init__ if imported in agent context
import sys
if any("agents" in arg for arg in sys.argv):
    import inspect
    import builtins

    def log_init_patch(cls):
        orig_init = cls.__init__
        def new_init(self, *args, **kwargs):
            log_agent_activation(cls.__name__)
            orig_init(self, *args, **kwargs)
        cls.__init__ = new_init
        return cls

    builtins.__ECHO_AUTO_LOG_PATCH__ = log_init_patch
