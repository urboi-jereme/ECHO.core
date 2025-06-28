# echo_daemon.py
import time
import os
import sys
import yaml
from datetime import datetime
from agents.intuition import IntuitionAgent
from agents.navigator import NavigatorAgent
from agents.curiosity_agent import CuriosityAgent
from agents.modulator import ModulatorAgent
from echo_logger import log_custom_event

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
PRESSURE_PATH = os.path.join(MEMORY_DIR, "MOTIF_PRESSURE.yaml")
GOALS_PATH = os.path.join(MEMORY_DIR, "GOALS.yaml")
INTERVAL_SECONDS = 600  # 10 minutes

def load_yaml(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

def daemon_loop():
    log_custom_event("🌀 ECHO Daemon started")

    while True:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        log_custom_event(f"🔁 Daemon cycle at {timestamp}")

        intuition = IntuitionAgent()
        navigator = NavigatorAgent()
        curiosity = CuriosityAgent()
        modulator = ModulatorAgent()

        # Load memory signals
        pressure_data = load_yaml(PRESSURE_PATH)
        goal_data = load_yaml(GOALS_PATH)

        # Run modulator to adapt agent weights
        modulator.run()
        log_custom_event("🔧 ModulatorAgent updated agent weights")

        top_motifs = intuition.get_resonant_tags()[:3]
        prompt_targets = navigator.get_next_prompt_targets()
        questions = curiosity.generate_questions()

        log_custom_event("🧠 Top Resonant Motifs:")
        for motif in top_motifs:
            log_custom_event(f"• {motif['tag']} (resonance: {motif['avg_resonance']:.2f})")

        log_custom_event("🎯 Prompt Suggestions:")
        for p in prompt_targets:
            log_custom_event(f"• {p}")

        log_custom_event("❓ Curiosity Questions:")
        for q in questions:
            log_custom_event(f"• {q}")

        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    daemon_loop()
