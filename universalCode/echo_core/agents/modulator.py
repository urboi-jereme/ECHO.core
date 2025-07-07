
# File: agents/modulator.py

"""
ModulatorAgent is responsible for dynamically adjusting agent behavior based on symbolic motifs,
resonance trends, and meta-preference schemas.

It reads from META_PREFERENCES.yaml and modifies AGENT_STATE.yaml accordingly.
"""

import os
from pathlib import Path

from echo_core.utils.echo_logger import log_agent_activation
from echo_core.utils.yaml_utils import load, dump


class ModulatorAgent:
    def __init__(self, preferences_path: str | Path = None, agent_state_path: str | Path = None):
        base = Path(__file__).resolve().parent.parent
        if preferences_path is None:
            preferences_path = base / "memory" / "META_PREFERENCES.yaml"
        if agent_state_path is None:
            agent_state_path = base.parent.parent / "memory" / "AGENT_STATE.yaml"
        self.preferences_path = Path(preferences_path)
        self.agent_state_path = Path(agent_state_path)
        self.meta_preferences = load(self.preferences_path, fallback={})
        self.agent_state = load(self.agent_state_path, fallback={})

    def adjust_agent_weights(self):
        if not self.meta_preferences or "modulation_rules" not in self.meta_preferences:
            print("⚠️  No modulation rules found. No adjustments made.")
            return self.agent_state

        for rule in self.meta_preferences["modulation_rules"]:
            agent = rule.get("agent")
            weight = rule.get("weight")
            if agent and weight is not None:
                if agent not in self.agent_state:
                    self.agent_state[agent] = {}
                self.agent_state[agent]["weight"] = weight
                print(f"🛠️  Adjusted weight of '{agent}' to {weight}")

        return self.agent_state

    def save_agent_state(self):
        dump(self.agent_state, self.agent_state_path)
        print("✅ AGENT_STATE.yaml updated successfully.")

    def run(self):
        self.adjust_agent_weights()
        self.save_agent_state()

if __name__ == "__main__":
    modulator = ModulatorAgent()
    modulator.run()
