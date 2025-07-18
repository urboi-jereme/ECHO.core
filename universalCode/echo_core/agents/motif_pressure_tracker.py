"""Calculate motif pressure based on occurrences in memory."""

from pathlib import Path
from collections import defaultdict

from echo_core.utils.echo_logger import log_agent_activation
from echo_core.utils.yaml_utils import load, dump

BASE_PATH = Path(__file__).resolve().parents[3]
MEMORY_PATH = BASE_PATH / "memory"
PRESSURE_FILE = MEMORY_PATH / "MOTIF_PRESSURE.yaml"

def load_yaml(file_name: str) -> dict:
    """Load a YAML file from ``MEMORY_PATH`` with fallback to empty dict."""
    return load(MEMORY_PATH / file_name, fallback={})

import sys
import os

# Add the root ECHO.core path to sys.path so echo_logger can be imported
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".."))
sys.path.insert(0, BASE_PATH)

from echo_logger import log_agent_activation
import yaml
from collections import defaultdict

log_agent_activation("MotifPressureTracker", reason="Recalculate motif pressure from ECHO_MEMORY")

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".."))
MEMORY_PATH = os.path.join(BASE_PATH, "memory")
OUTPUT_PATH = os.path.join(MEMORY_PATH, "MOTIF_PRESSURE.yaml")
PRESSURE_FILE = OUTPUT_PATH

def load_yaml(file_name):
    try:
        with open(os.path.join(MEMORY_PATH, file_name), "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


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


def save_pressure(pressure):
    with open(PRESSURE_FILE, "w") as f:
        yaml.dump({"motif_pressure": pressure}, f, sort_keys=False)
    print(f"✅ Motif pressure written to {PRESSURE_FILE}")

if __name__ == "__main__":


    print("🔍 Computing motif pressure from memory...")
    pressure = compute_motif_pressure()
    save_pressure(pressure)
    for motif, count in pressure.items():
        print(f"• {motif}: {count}")
