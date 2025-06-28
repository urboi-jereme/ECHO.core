from agents.intuition import IntuitionAgent from agents.navigator import NavigatorAgent from memory import load_goals, update_goal_status import yaml import os

print("\U0001F9E0 Initializing ECHO.Core Cognitive Loop...\n")

Load active goals

goals = load_goals() print("🎯 Active Goals:") for g in goals: if g['status'] == 'active': print(f"• {g['goal']} (trigger tags: {', '.join(g['trigger_tags'])})") print()

Load motif pressure data

PRESSURE_PATH = os.path.join(os.path.dirname(file), 'memory/MOTIF_PRESSURE.yaml') if os.path.exists(PRESSURE_PATH): with open(PRESSURE_PATH, 'r') as f: motif_data = yaml.safe_load(f) motif_pressure = motif_data.get('motif_pressure', {}) else: motif_pressure = {} print("⚠️  MOTIF_PRESSURE.yaml not found. Run motif_pressure_tracker.py to generate it.")

Display motif pressure

print("\U0001F4A1 Motif Pressure Levels:") for tag, count in sorted(motif_pressure.items(), key=lambda x: -x[1]): print(f"• {tag}: {count}") print()

Initialize agents

intuition = IntuitionAgent() navigator = NavigatorAgent()

Run cognitive loop

prompts = navigator.get_next_prompt_targets() actions = navigator.get_next_architectural_actions()

print("\U0001F52E Top Symbolic Motifs:") for tag in intuition.get_resonant_tags(): print(f"• {tag['tag']} (resonance: {tag['avg_resonance']:.2f}, count: {tag['count']})") print()

print("\U0001F9E0 Proposed Prompts:") for p in prompts: print(f"• {p}") print()

print("\U0001F6E0️ Proposed Architectural Actions:") for a in actions: print(f"• {a}") print()

print("\U0001F501 Next step options:") print("1. Generate prompt from top motif") print("2. Scaffold ModulatorAgent") print("3. Exit") choice = input("Enter choice (1/2/3): ")

if choice == '1': print("\n⚙️ Generating prompt from top motif...") # Simulated prompt generation here elif choice == '2': print("\n🚧 Triggering ModulatorAgent scaffolding sequence (not yet implemented)") elif choice == '3': print("\n👋 Exiting ECHO.Core cognitive loop.") else: print("\n❓ Invalid choice.")

