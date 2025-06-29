print("✅ echo_main.py is running...")

from agents.intuition import IntuitionAgent
from agents.navigator import NavigatorAgent
from agents.curiosity import CuriosityAgent
from memory.goals import load_goals
import yaml
import os

# echo_main.py
from memory.echo_memory import load_yaml

print("✅ echo_main.py is running...")

# Load active goals
goals = load_yaml("memory/GOALS.yaml") or []
print("🎯 Active Goals:")
for g in goals:
    print(f" - {g}")

# Load motif pressure
PRESSURE_PATH = os.path.join(os.path.dirname(__file__), 'memory/MOTIF_PRESSURE.yaml')
if os.path.exists(PRESSURE_PATH):
    with open(PRESSURE_PATH, 'r') as f:
        motif_data = yaml.safe_load(f)
        motif_pressure = motif_data.get('motif_pressure', {})
else:
    motif_pressure = {}
    print("⚠️  MOTIF_PRESSURE.yaml not found. Run motif_pressure_tracker.py first.")

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
