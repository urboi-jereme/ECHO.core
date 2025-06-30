print("✅ echo_main.py is running...")

import os
import sys
import yaml
from runtime.emergence_tracker import check_emergence
from agents.intuition import IntuitionAgent
from agents.navigator import NavigatorAgent
from agents.curiosity import CuriosityAgent
from memory.goals import load_goals
from yaml_utils import load  # ✅ This is our YAML loader now

# Load memory and beliefs
memory_data = load("memory/ECHO_MEMORY.yaml", fallback={"echo_memory": []})
memory_entries = memory_data.get("echo_memory", [])
beliefs = load("memory/BELIEFS.yaml", fallback=[])

# Load active goals
goals = load("memory/GOALS.yaml", fallback=[])
print("🎯 Active Goals:")
for g in goals:
    print(f" - {g}")

# Load motif pressure
motif_pressure = load("memory/MOTIF_PRESSURE.yaml", fallback={}).get("motif_pressure", {})

print("\n💡 Motif Pressure Levels:")
for tag, count in sorted(motif_pressure.items(), key=lambda x: -x[1]):
    print(f"• {tag}: {count}")
print()

# Initialize agents
intuition = IntuitionAgent()
navigator = NavigatorAgent()
curiosity = CuriosityAgent()

# Check for symbolic emergence events
emergence_events = check_emergence(memory_entries, goals, beliefs)
if emergence_events:
    print("\n🌟 Emergence Milestones:")
    for ev in emergence_events:
        print(f"• {ev['motif']} ({ev['source']})")
    print()

# Generate outputs
print("🔮 Resonant Tags:")
for tag in intuition.get_resonant_tags():
    print(f"• {tag['tag']} (resonance: {tag['avg_resonance']:.2f}, count: {tag['count']})")
print()

print("🧭 Proposed Prompts:")
for p in navigator.get_next_prompt_targets():
    print(f"• {p}")
print()

print("🏗️  Architectural Suggestions:")
for a in navigator.get_next_architectural_actions():
    print(f"• {a}")
print()

print("🤔 Curiosity Questions:")
for q in curiosity.generate_questions():
    print(f"• {q}")
print()
