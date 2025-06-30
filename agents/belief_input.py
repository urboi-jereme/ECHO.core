# File: agents/belief_input.py
"""BeliefInputAgent proposes new belief candidates based on motif resonance."""

import os
import sys
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.intuition import IntuitionAgent
from yaml_utils import load, dump


class BeliefInputAgent:
    def __init__(self, memory_file: str = "memory/ECHO_MEMORY.yaml", beliefs_file: str = "memory/BELIEFS.yaml"):
        self.intuition = IntuitionAgent(memory_file)
        self.beliefs_file = beliefs_file
        data = load(beliefs_file, fallback={"beliefs": []})
        self.beliefs: List[str] = data.get("beliefs", [])

    def propose_beliefs(self, top_n: int = 3) -> List[str]:
        tags = self.intuition.get_resonant_tags(top_n=top_n)
        return [f"Belief candidate: {tag['tag']} influences outcomes." for tag in tags]

    def add_belief(self, text: str) -> None:
        self.beliefs.append(text)
        dump({"beliefs": self.beliefs}, self.beliefs_file)
