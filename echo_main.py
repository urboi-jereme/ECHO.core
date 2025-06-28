from agents.intuition import IntuitionAgent
from agents.navigator import NavigatorAgent
from agents.curiosity_agent import CuriosityAgent
from memory import load_goals, update_goal_status
import yaml
import os

print("🧠 Initializing ECHO.Core Cognitive Loop...\n")

# Load active goals
goals = load_goals()
print("🎯 Active Goals:")
for g in goals:
    if g["status"] == "active":
        print(f"• {g['goal']} (trigger tags: {', '.join(g['trigger_tags'])})")
print()

# Load motif pressure data
PRESSURE_PATH = os.path.join(os.path.dirname(__file__), 'memory/MOTIF_PRESSURE.yaml')
if os.path.exists(PRESSURE_PATH):
    with open(PRESSURE_PATH, 'r') as f:
        motif_data = yaml.safe_load(f)
        motif_pressure = motif_data.get('motif_pressure', {})
else:
    motif_pressure = {}
    print("⚠️  MOTIF_PRESSURE.yaml not found. Run motif_pressure_tracker.py to generate it.")

# Display motif pressure
print("💡 Motif Pressure Levels:")
for tag, count in sorted(motif_pressure.items(), key=lambda x: -x[1]):
    print(f"• {tag}: {count}")
print()

# Initialize agents
intuition = IntuitionAgent()
navigator = NavigatorAgent()
curiosity = CuriosityAgent()

# Run cognitive loop
prompts = navigator.get_next_prompt_targets()
actions = navigator.get_next_architectural_actions()

print("🔮 Top Symbolic Motifs:")
for tag in intuition.get_resonant_tags():
    print(f"• {tag['tag']} (resonance: {tag['avg_resonance']:.2f}, count: {tag['count']})")
print()

print("🧠 Proposed Prompts:")
for p in prompts:
    print(f"• {p}")
print()

print("🛠️ Proposed Architectural Actions:")
for a in actions:
    print(f"• {a}")
print()

# Curiosity loop
curious_questions = curiosity.generate_questions()
if curious_questions:
    print("🤔 CuriosityAgent Questions:")
    for q in curious_questions:
        print(f"• {q}")
    print()
    
    response = input("✍️  Would you like to log a response to one? (y/n): ")
    if response.lower() == 'y':
        chosen = input("Enter motif tag you're responding to: ").strip()
        insight = input("Enter your symbolic insight or reflection: ").strip()

        memory_entry = {
            "tags": [chosen],
            "content": insight,
            "resonance": 10.0
        }

        memory_path = os.path.join(os.path.dirname(__file__), 'memory/ECHO_MEMORY.yaml')
        if os.path.exists(memory_path):
            with open(memory_path, 'r') as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}

        data.setdefault("echo_memory", []).append(memory_entry)

        with open(memory_path, 'w') as f:
            yaml.dump(data, f, sort_keys=False)

        print("✅ Response logged to ECHO_MEMORY.yaml")
        print()

# Prompt user for next step
print("🔁 Next step options:")
print("1. Generate prompt from top motif")
print("2. Scaffold ModulatorAgent")
print("3. Exit")

choice = input("Enter choice (1/2/3): ")

if choice == '1':
    print("\n⚙️ Generating prompt from top motif...")
    # Simulated prompt generation
elif choice == '2':
    print("\n🚧 Triggering ModulatorAgent scaffolding sequence (not yet implemented)")
elif choice == '3':
    print("\n👋 Exiting ECHO.Core cognitive loop.")
else:
    print("\n❓ Invalid choice.")
