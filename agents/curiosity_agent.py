import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from memory import load_goals

from typing import List, Dict
from echo_logger import log_agent_activation

class CuriosityAgent:
    def __init__(self):
        log_agent_activation("CuriosityAgent", reason="ECHO converse initiated")
        self.relevant_motifs = self._extract_motifs_from_goals()

        if not self.relevant_motifs:
            print("[⚠️ warning] No motifs found in goals. Falling back to default motifs.")
            self.relevant_motifs = ["emergence", "recursion", "coherence", "symbolic friction"]

        print(f"[debug] CuriosityAgent initialized with motifs: {self.relevant_motifs}")

    def _extract_motifs_from_goals(self) -> List[str]:
        try:
            goals = load_goals()
            motifs = [tag for g in goals for tag in g.get("trigger_tags", [])]
            return list(set(motifs))  # De-duplicate
        except Exception as e:
            print(f"[error] Failed to load goals: {e}")
            return []

    def generate_questions(self) -> List[Dict[str, str]]:
        print(f"[debug] Generating questions from motifs: {self.relevant_motifs}")
        questions = []

        for motif in self.relevant_motifs:
            q = {
                "motif": motif,
                "question_text": f"What deeper symbolic pattern might be emerging in relation to '{motif}'?"
            }
            questions.append(q)

        if not questions:
            print("[❌] No curiosity questions could be generated.")
        else:
            print(f"[✅] Generated {len(questions)} curiosity question(s).")

        return questions
