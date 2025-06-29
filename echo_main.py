# echo_main.py

print("✅ echo_main.py is running...")

from agents.intuition import IntuitionAgent
from agents.navigator import NavigatorAgent
from agents.curiosity import CuriosityAgent
from memory.echo_memory import load_yaml
from yaml_utils import load  # Replaces direct PyYAML calls
import os

# Load active goals
goals = load("memory/GOALS.yaml", fallback=[])
print("🎯 Active Goals:")
for g in goals:
    print(f" - {g}")

# Load motif pressure
motif_pressure = load("memory/MOTIF_PRESSURE.yaml", fallback={})
if isinstance(motif_pressure, dict) and "motif_pressure" in motif_pressure:
    motif_pressure = motif_pressure["motif_pressure"]

print("\n💡 Motif Pressure Levels:")
for tag, count in sorted(motif_pressure.items(), key=lambda x: -x[1]):
    print(f"• {tag}: {count}")
print()

# Initialize agents
intuition = IntuitionAgent()
navigator = NavigatorAgent()
curiosity = CuriosityAgent()

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
