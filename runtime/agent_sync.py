import yaml
import os
from echo_logger import log_custom_event

AGENT_STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "AGENT_STATE.yaml")

def sync_agent_weight(agent_name: str, weight: float):
    """Persist the agent's weight directly in AGENT_STATE.yaml."""
    with open(AGENT_STATE_FILE, "r") as f:
        state = yaml.safe_load(f) or {}

    agent_entry = state.get(agent_name, {}) or {}
    if not isinstance(agent_entry, dict):
        agent_entry = {"weight": weight}
    else:
        agent_entry["weight"] = weight
    state[agent_name] = agent_entry

    with open(AGENT_STATE_FILE, "w") as f:
        yaml.dump(state, f, sort_keys=False)

    log_custom_event(f"🔄 Synced {agent_name} weight: {weight}")
