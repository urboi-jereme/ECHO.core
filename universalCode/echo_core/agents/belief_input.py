# File: agents/belief_input.py
"""BeliefInputAgent proposes new belief candidates based on motif resonance."""

import os
from pathlib import Path
from typing import List

from echo_core.agents.intuition import IntuitionAgent
from echo_core.utils.yaml_utils import load, dump


class BeliefInputAgent:
    def __init__(self, memory_file: str | Path = None, beliefs_file: str | Path = None):
        if memory_file is None:
            memory_file = Path(__file__).resolve().parents[3] / "memory" / "ECHO_MEMORY.yaml"
        if beliefs_file is None:
            beliefs_file = Path(__file__).resolve().parents[3] / "memory" / "BELIEFS.yaml"
        self.intuition = IntuitionAgent(memory_file)
        self.beliefs_file = str(beliefs_file)
        data = load(beliefs_file, fallback={"beliefs": []})
        self.beliefs: List[str] = data.get("beliefs", [])

    def propose_beliefs(self, top_n: int = 3) -> List[str]:
        tags = self.intuition.get_resonant_tags(top_n=top_n)
        return [f"Belief candidate: {tag['tag']} influences outcomes." for tag in tags]

    def add_belief(self, text: str) -> None:
        self.beliefs.append(text)
        dump({"beliefs": self.beliefs}, self.beliefs_file)
