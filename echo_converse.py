from agents.curiosity_agent import CuriosityAgent
from datetime import datetime
import yaml
import os

MEMORY_PATH = os.path.join("memory", "ECHO_MEMORY.yaml")

def log_response(motif, response, resonance):
    entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "tags": [motif],
        "content": response,
        "resonance": float(resonance)
    }
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            data = yaml.safe_load(f) or {"echo_memory": []}
    else:
        data = {"echo_memory": []}
    data["echo_memory"].append(entry)
    with open(MEMORY_PATH, "w") as f:
        yaml.dump(data, f, sort_keys=False)

# Start conversation
curiosity = CuriosityAgent()
questions = curiosity.generate_questions()

if not questions:
    print("❌ No questions generated.")
else:
    for q in questions:
        print(f"🤖 ECHO asks about motif: {q['motif']}")
        print(f"❓ {q['question_text']}")
        response = input("✍️  Your insight: ").strip()
        resonance = input("🔢 How resonant was that insight (1-10)? ").strip()
        log_response(q["motif"], response, resonance)
        print("✅ Logged.\n")
