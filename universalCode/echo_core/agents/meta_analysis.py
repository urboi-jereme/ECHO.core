"""MetaAnalysisAgent evaluates symbolic integrity across sessions."""

from pathlib import Path
from echo_core.utils.yaml_utils import load

class MetaAnalysisAgent:
    """Analyze memory and assumptions for contradictions or drift."""

    def __init__(self, memory_file: str | Path | None = None,
                 assumptions_file: str | Path | None = None):
        base = Path(__file__).resolve().parent.parent / "memory"
        self.memory_file = Path(memory_file) if memory_file else base / "ECHO_MEMORY.yaml"
        self.assumptions_file = Path(assumptions_file) if assumptions_file else base / "ARRESTED_ASSUMPTIONS.yaml"

    def evaluate_integrity(self) -> dict:
        """Return simple diagnostics about symbolic integrity."""
        memory = load(self.memory_file, fallback={"echo_memory": []}).get("echo_memory", [])
        assumptions = load(self.assumptions_file, fallback={"arrested_assumptions": []}).get("arrested_assumptions", [])
        contradictions = []
        seen = {}
        for entry in memory:
            for tag in entry.get("tags", []):
                if tag in seen and seen[tag] != entry.get("status"):
                    contradictions.append({"tag": tag, "states": {seen[tag], entry.get("status")}})
                else:
                    seen[tag] = entry.get("status")
        assumption_notes = [a["assumption"] for a in assumptions if a.get("status") == "re-evaluated"]
        return {
            "contradictions": contradictions,
            "re_evaluated_assumptions": assumption_notes,
        }
