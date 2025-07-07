# loop_controller.py v0.1.0
"""Recursive execution controller for the ECHO cognitive loop."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Dict, Any

from echo_core.tools import belief_export_formatter as bef
from echo_core.tools import triad_translator as tt
from echo_core.tools import memory_ingestor as mi
from echo_core.utils.yaml_utils import loads

BASE = Path(__file__).resolve().parents[3] / "memory"
MEMORY_PATH = BASE / "ECHO_MEMORY.yaml"


class LoopController:
    """High-level orchestrator for one reasoning cycle."""

    def __init__(self, memory_file: str | Path | None = None) -> None:
        self.memory_file = Path(memory_file) if memory_file else MEMORY_PATH

    def process_text(self, text: str) -> Iterable[Dict[str, Any]]:
        """Translate raw text into beliefs and store them in memory."""
        yaml_text = bef.format_beliefs(text)
        entries = loads(yaml_text) or []
        if isinstance(entries, dict):
            entries = [entries]
        for entry in entries:
            entry["propositional_cores"] = tt.extract_propositional_cores(entry["sentence"])
        mi.ingest_entries(entries, self.memory_file)
        return entries

    def run_interactive(self) -> None:
        """Simple interactive loop for manual testing."""
        try:
            while True:
                text = input("Enter reflection (blank to exit): ").strip()
                if not text:
                    break
                entries = self.process_text(text)
                print("Stored entries:")
                for e in entries:
                    print(f"- {e['symbolic_insight']}")
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    LoopController().run_interactive()
