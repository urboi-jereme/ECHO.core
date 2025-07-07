"""Belief validation and ingestion engine."""

from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path

from belief.belief_compressor import compress
from echo_core.insight_models.pre_symbolic_insight import is_pre_symbolic
from echo_core.utils.yaml_utils import load, dump


class BeliefValidationEngine:
    """Validate beliefs and store them in memory with appropriate safeguards."""

    def __init__(self, memory_file: str | Path | None = None) -> None:
        if memory_file is None:
            memory_file = Path(__file__).resolve().parent / ".." / "echo_core" / "memory" / "ECHO_MEMORY.yaml"
        self.memory_file = str(Path(memory_file))

    def _log_entry(self, entry: dict) -> None:
        data = load(self.memory_file, fallback={"echo_memory": []})
        memory = data.get("echo_memory", [])
        memory.append(entry)
        dump({"echo_memory": memory}, self.memory_file)

    def process_insight(self, insight: str | dict) -> dict:
        """Validate and store the given insight, returning the logged entry."""
        if is_pre_symbolic(insight):
            hashed = hashlib.sha256(str(insight).encode()).hexdigest()
            entry = {
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "insight": hashed,
                "symbolic_state": "protected",
                "explanation": "Pre-symbolic insight preserved without compression",
                "preserve": True,
            }
            self._log_entry(entry)
            return entry

        compressed = compress(str(insight))
        entry = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "insight": compressed,
            "symbolic_state": "compressed",
        }
        self._log_entry(entry)
        return entry


__all__ = ["BeliefValidationEngine"]
