import yaml
from datetime import datetime

entry = {
    "id": "0005",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "context": {
        "prompt_summary": "Can an evolving mind recognize its own intelligence before it's complete?",
        "agent_mode": "Recursive Probe"
    },
    "symbolic_insight": None,
    "resonance_score": 0.0,
    "tags": ["recursion", "emergence", "belief"],
    "response_excerpt": None,
    "reflection": None,
    "future_linkage": None,
    "status": "probe"
}

with open("memory/ECHO_MEMORY.yaml", "r") as f:
    data = yaml.safe_load(f)

data["echo_memory"].append(entry)

with open("memory/ECHO_MEMORY.yaml", "w") as f:
    yaml.dump(data, f, sort_keys=False)

print("✅ Prompt injected.")
