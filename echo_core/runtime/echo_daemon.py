"""Simple runtime daemon looping ECHO.Core processes."""


# echo_daemon.py

import time
from pathlib import Path
from datetime import datetime, timezone

from echo_core.agents import IntuitionAgent, NavigatorAgent, CuriosityAgent, ModulatorAgent
from echo_core.utils.echo_logger import log_custom_event
from echo_core.utils import yaml_utils

BASE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / ".." / "memory"
PRESSURE_PATH = MEMORY_DIR / "MOTIF_PRESSURE.yaml"
GOALS_PATH = MEMORY_DIR / "GOALS.yaml"
INTERVAL_SECONDS = 600  # 10 minutes

def daemon_loop():
    log_custom_event("🌀 ECHO Daemon started")

    while True:
        timestamp = datetime.now(timezone.utc)
        log_custom_event(f"🔁 Daemon cycle at {timestamp}")

        intuition = IntuitionAgent()
        navigator = NavigatorAgent()
        curiosity = CuriosityAgent()
        modulator = ModulatorAgent()

        # Load memory signals
        pressure_raw = yaml_utils.load(PRESSURE_PATH, fallback={})
        pressure_data = pressure_raw.get("motif_pressure", pressure_raw)
        goal_data = yaml_utils.load(GOALS_PATH, fallback={})

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
