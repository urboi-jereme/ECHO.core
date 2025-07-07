# File: agents/intuition.py

"""
IntuitionAgent is a symbolic resonance detector for ECHO.Core.

Its purpose is to analyze ECHO_MEMORY.yaml and identify:
1. The most resonant symbolic motifs (based on tag frequency + resonance score)
2. Unresolved insights that still carry active symbolic weight
3. Suggested next directions based on internal harmonic alignment
"""

import os
from pathlib import Path
from collections import defaultdict
from operator import itemgetter

from echo_core.utils.echo_logger import log_agent_activation
from echo_core.utils.yaml_utils import load

class IntuitionAgent:
    def __init__(self, memory_file: str | Path | None = None):
        if memory_file is None:
            memory_file = Path(__file__).resolve().parents[3] / "memory" / "ECHO_MEMORY.yaml"
        memory_file = Path(memory_file)
        loaded = load(memory_file, fallback={})
        if not loaded or 'echo_memory' not in loaded:
            print("⚠️  Warning: ECHO_MEMORY.yaml is empty or malformed. Initializing with empty memory.")
            self.memory = []
        else:
            self.memory = loaded['echo_memory']

        if not self.memory:
            print("🧪 Tip: You can seed the memory by adding symbolic insights into ECHO_MEMORY.yaml.")

    def get_resonant_tags(self, top_n=5):
        tag_scores = defaultdict(float)
        tag_counts = defaultdict(int)

        for entry in self.memory:
            if entry['status'] == 'active':
                for tag in entry.get('tags', []):
                    tag_scores[tag] += entry.get('resonance_score', 0)
                    tag_counts[tag] += 1

        tag_rankings = [
            {
                'tag': tag,
                'avg_resonance': tag_scores[tag] / tag_counts[tag],
                'count': tag_counts[tag]
            }
            for tag in tag_scores
        ]

        return sorted(tag_rankings, key=itemgetter('avg_resonance', 'count'), reverse=True)[:top_n]

    def get_unresolved_insights(self, top_n=5):
        return sorted(
            [e for e in self.memory if e['status'] == 'active'],
            key=lambda x: x['resonance_score'],
            reverse=True
        )[:top_n]

    def suggest_inquiry_paths(self):
        tags = self.get_resonant_tags()
        return [
            f"Explore symbolic motif: {tag['tag']} (avg resonance: {tag['avg_resonance']:.2f})"
            for tag in tags
        ]
