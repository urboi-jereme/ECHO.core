print("✅ echo_main.py is running...")

from agents.intuition import IntuitionAgent
from agents.navigator import NavigatorAgent
from agents.curiosity import CuriosityAgent
from yaml_utils import load as load_yaml  # Replaces direct yaml.safe_load
import os

# Load active goals with fallback to empty list
goals = load_yaml("memory/GOALS.yaml", fallback=[])
print("🎯 Active Goals:")
for g in goals:
    print(f" - {g.get('name', str(g))}")

# Load motif pressure data with fallback
PRESSURE_PATH = os.path.join(os.path.dirname(__file__), 'memory/MOTIF_PRESSURE.yaml')
motif_data = load_yaml(PRESSURE_PATH, fallback={"motif_pressure": {}})
motif_pressure = motif_data.get("motif_pressure", {})

if not motif_pressure:
    print("⚠️  MOTIF_PRESSURE.yaml missing or empty. Run motif_pressure_tracker.py first.")

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
