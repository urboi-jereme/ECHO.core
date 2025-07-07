import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime

MEMORY_PATH = Path(__file__).resolve().parents[3] / "memory" / "ECHO_MEMORY.yaml"
OUTPUT_PATH = Path("tests/RIDT_TEST_0001.yaml")

# Load memory file
def load_memory():
    with open(MEMORY_PATH, "r") as f:
        return yaml.safe_load(f)["echo_memory"]

# Group by motif and extract insights
def extract_summary(memory):
    summary = defaultdict(list)
    for entry in memory:
        for tag in entry.get("tags", []):
            summary[tag].append({
                "id": entry["id"],
                "date": entry["date"],
                "resonance_score": entry.get("resonance_score", 0),
                "insight": entry.get("symbolic_insight"),
                "reflection": entry.get("reflection"),
            })
    return summary

# Generate test structure for RIDT output
def generate_ridt_yaml(memory, run_id="1"):
    test_data = {
        "test_id": "RIDT_TEST_0001",
        "paradox": "Can an evolving mind recognize its own intelligence before it's complete?",
        "runs": [
            {
                "run": int(run_id),
                "motifs": sorted(set(tag for m in memory for tag in m.get("tags", []))),
                "insights": [m["symbolic_insight"] for m in memory if m.get("symbolic_insight")]
            }
        ]
    }
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(test_data, f, sort_keys=False)
    print(f"✅ RIDT summary written to {OUTPUT_PATH}")

# Pretty print insights by motif
def display_summary(summary):
    print("\n🧠 INSIGHTS BY MOTIF:")
    for motif, entries in summary.items():
        print(f"\n🔹 {motif.upper()}:")
        for e in entries:
            date = e["date"]
            score = e["resonance_score"]
            insight = e.get("insight")
            reflection = e.get("reflection")
            print(f"  - ({date} | score: {score}) -> {insight}")
            if reflection:
                print(f"    ↳ {reflection}")

if __name__ == "__main__":
    memory = load_memory()
    summary = extract_summary(memory)
    display_summary(summary)
    generate_ridt_yaml(memory)
