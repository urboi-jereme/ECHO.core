"""Linguistic Divergence Auditor

Compares motif translations across languages and logs high divergences
into CURIOSITY_PIPELINE.yaml.
"""

import difflib
from pathlib import Path
from typing import Dict

from echo_core.utils.yaml_utils import load, dump
from echo_core.utils.echo_logger import log_agent_activation


class LinguisticDivergenceAuditor:
    def __init__(self, pipeline_file: str | Path = None, threshold: float = 0.5):
        if pipeline_file is None:
            pipeline_file = Path(__file__).resolve().parents[3] / "memory" / "CURIOSITY_PIPELINE.yaml"
        self.pipeline_file = Path(pipeline_file)
        self.threshold = threshold
        log_agent_activation("LinguisticDivergenceAuditor", reason="Initialization")

    def _load_pipeline(self) -> Dict:
        return load(self.pipeline_file, fallback={"divergences": []})

    def _save_pipeline(self, data: Dict) -> None:
        dump(data, self.pipeline_file)

    def score_divergence(self, term1: str, term2: str) -> float:
        """Return heuristic divergence score between two terms."""
        if not term1 or not term2:
            return 0.0
        score = 0.0
        if term1.lower() == term2.lower():
            score += 0.5
        if len(term2.split()) > 1:
            score += 0.2
        ratio = difflib.SequenceMatcher(None, term1.lower(), term2.lower()).ratio()
        score += (1 - ratio) * 0.3
        return min(score, 1.0)

    def audit(self, term1: str, term2: str, lang1: str = "", lang2: str = "") -> float:
        """Compare terms and log divergence if above threshold."""
        score = self.score_divergence(term1, term2)
        if score >= self.threshold:
            data = self._load_pipeline()
            entry = {
                "term1": term1,
                "term2": term2,
                "lang1": lang1,
                "lang2": lang2,
                "score": round(score, 3),
            }
            data.setdefault("divergences", []).append(entry)
            self._save_pipeline(data)
        return score
