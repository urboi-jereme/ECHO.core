import os
import yaml
from datetime import datetime
from collections import defaultdict
from memory.alignments import log_alignment

MEMORY_PATH = "memory/ECHO_MEMORY.yaml"
PRESSURE_PATH = "memory/MOTIF_PRESSURE.yaml"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, 'r') as f:
        data = yaml.safe_load(f)
        return data if isinstance(data, list) else []

def save_memory(entries):
    with open(MEMORY_PATH, 'w') as f:
        yaml.dump(entries, f, sort_keys=False)

def update_pressure(tag):
    if os.path.exists(PRESSURE_PATH):
        with open(PRESSURE_PATH, 'r') as f:
            pressure = yaml.safe_load(f) or {}
    else:
        pressure = {}
    pressure[tag] = pressure.get(tag, 0) + 1
    with open(PRESSURE_PATH, 'w') as f:
        yaml.dump(pressure, f, sort_keys=False)

def log_feedback(motif, response_text):
    memory = load_memory()
    entry = {
        'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'tags': [motif],
        'content': response_text,
        'resonance': 7.0  # Default resonance for feedback
    }
    memory.append(entry)
    save_memory(memory)
    update_pressure(motif)
    # record alignment when user feedback mirrors existing motifs
    log_alignment(
        interaction={
            'summary': f"Feedback for {motif}",
            'content': response_text,
        },
        mirrored_tags=[motif],
        reasoning_path=['feedback', 'motif coherence'],
        agent_activations=['CuriosityAgent'],
        score=7.0,
        notes='Logged from echo_feedback'
    )
    print(f"✅ Feedback on '{motif}' logged successfully. Motif pressure updated.")

if __name__ == "__main__":
    print("✍️  Provide your reflection on a motif.")
    motif = input("Motif tag: ").strip()
    if not motif:
        print("❌ Motif is required.")
        exit(1)
    response = input("Your reflection: ").strip()
    if not response:
        print("❌ Response text is required.")
        exit(1)
    log_feedback(motif, response)
