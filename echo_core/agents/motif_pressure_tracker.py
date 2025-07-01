"""Calculate motif pressure based on occurrences in memory."""

from pathlib import Path
from collections import defaultdict

from echo_core.utils.echo_logger import log_agent_activation
from echo_core.utils.yaml_utils import load, dump

BASE_PATH = Path(__file__).resolve().parent.parent
MEMORY_PATH = BASE_PATH / "memory"
PRESSURE_FILE = MEMORY_PATH / "MOTIF_PRESSURE.yaml"

def load_yaml(file_name: str) -> dict:
    """Load a YAML file from ``MEMORY_PATH`` with fallback to empty dict."""
    return load(MEMORY_PATH / file_name, fallback={})

def compute_motif_pressure():
    memory = load_yaml("ECHO_MEMORY.yaml")
    motif_counter = defaultdict(int)

    for entry in memory.get("echo_memory", []):
        if isinstance(entry, dict):
            for tag in entry.get("tags", []):
                motif_counter[tag] += 1
        else:
            print(f"[WARN] Skipping malformed memory entry: {entry}")
    return dict(sorted(motif_counter.items(), key=lambda x: -x[1]))

def save_pressure(pressure: dict) -> None:
    """Persist pressure values to ``PRESSURE_FILE``."""
    dump({"motif_pressure": pressure}, PRESSURE_FILE)
    print(f"✅ Motif pressure written to {PRESSURE_FILE}")

if __name__ == "__main__":
    log_agent_activation("MotifPressureTracker", reason="recalculate motif pressure")
    print("🔍 Computing motif pressure from memory...")
    pressure = compute_motif_pressure()
    save_pressure(pressure)
    for motif, count in pressure.items():
        print(f"• {motif}: {count}")
