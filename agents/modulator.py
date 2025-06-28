
# File: agents/modulator.py

"""
ModulatorAgent is responsible for dynamically adjusting agent behavior based on symbolic motifs,
resonance trends, and meta-preference schemas.

It reads from META_PREFERENCES.yaml and modifies AGENT_STATE.yaml accordingly.
"""

import yaml
import os

class ModulatorAgent:
    def __init__(self, preferences_path="memory/META_PREFERENCES.yaml", agent_state_path="memory/AGENT_STATE.yaml"):
        self.preferences_path = preferences_path
        self.agent_state_path = agent_state_path
        self.meta_preferences = self.load_yaml(preferences_path)
        self.agent_state = self.load_yaml(agent_state_path)

    def load_yaml(self, path):
        if not os.path.exists(path):
            print(f"⚠️  Missing file: {path}. Initializing with empty dict.")
            return {}
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}

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
        with open(self.agent_state_path, "w") as f:
            yaml.dump(self.agent_state, f)
        print("✅ AGENT_STATE.yaml updated successfully.")

    def run(self):
        self.adjust_agent_weights()
        self.save_agent_state()

if __name__ == "__main__":
    modulator = ModulatorAgent()
    modulator.run()
