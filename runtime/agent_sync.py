import yaml
import os
from echo_logger import log_custom_event

AGENT_STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "AGENT_STATE.yaml")

def sync_agent_weight(agent_name: str, weight: float):
    with open(AGENT_STATE_FILE, "r") as f:
        state = yaml.safe_load(f) or {}

    state.setdefault("agent_weights", {})[agent_name] = weight

    with open(AGENT_STATE_FILE, "w") as f:
        yaml.dump(state, f)

    log_custom_event(f"🔄 Synced {agent_name} weight: {weight}")
