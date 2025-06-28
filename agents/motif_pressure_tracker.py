import yaml import os from collections import Counter

MEMORY_PATH = os.path.join(os.path.dirname(file), '../memory/ECHO_MEMORY.yaml') PRESSURE_PATH = os.path.join(os.path.dirname(file), '../memory/MOTIF_PRESSURE.yaml')

def load_memory(): if not os.path.exists(MEMORY_PATH): print("⚠️  ECHO_MEMORY.yaml not found.") return [] with open(MEMORY_PATH, 'r') as f: data = yaml.safe_load(f) return data.get('echo_memory', [])

def compute_pressure(memory_entries): tag_counts = Counter() for entry in memory_entries: for tag in entry.get('tags', []): tag_counts[tag] += 1 return dict(tag_counts)

def save_pressure(pressure_dict): with open(PRESSURE_PATH, 'w') as f: yaml.dump({'motif_pressure': pressure_dict}, f, sort_keys=False) print("✅ MOTIF_PRESSURE.yaml updated.")

def run_tracker(): memory = load_memory() pressure = compute_pressure(memory) save_pressure(pressure) print("\n🔍 Motif Pressure:") for tag, count in sorted(pressure.items(), key=lambda x: -x[1]): print(f"• {tag}: {count}")

if name == 'main': run_tracker()

