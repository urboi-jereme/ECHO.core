# File: agents/motif_pressure_tracker.py

from agents.intuition import IntuitionAgent
from agents.navigator import NavigatorAgent
from memory.goals import load_goals, update_goal_status

import yaml
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from echo_logger import log_agent_activation


MEMORY_FILE = "memory/ECHO_MEMORY.yaml"
PRESSURE_FILE = "memory/MOTIF_PRESSURE.yaml"

def compute_motif_pressure():
    if not os.path.exists(MEMORY_FILE):
        print("❌ ECHO_MEMORY.yaml not found.")
        return {}

    with open(MEMORY_FILE, "r") as f:
        memory = yaml.safe_load(f) or []

    pressure = {}

    for entry in memory:
        for tag in entry.get("tags", []):
            if tag not in pressure:
                pressure[tag] = 0
            pressure[tag] += 1

    return dict(sorted(pressure.items(), key=lambda x: x[1], reverse=True))

def save_pressure(pressure):
    with open(PRESSURE_FILE, "w") as f:
        yaml.dump(pressure, f, sort_keys=False)
    print(f"✅ Motif pressure written to {PRESSURE_FILE}")

if __name__ == "__main__":
    print("🔍 Computing motif pressure from memory...")
    pressure = compute_motif_pressure()
    if pressure:
        save_pressure(pressure)
    else:
        print("⚠️ No motifs found in memory.")
