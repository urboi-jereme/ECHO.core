import os
from pathlib import Path
from datetime import datetime

from echo_core.runtime.echo_runtime_state import log_event

from echo_core.utils.echo_logger import log_agent_activation
from echo_core.memory.goals import load_goals
from echo_core.utils.yaml_utils import load, dump

log_agent_activation("CuriosityAgent", reason="Initialization")

class CuriosityAgent:
    def __init__(self):
        print("[CuriosityAgent] Initializing...")
        self.goals = self._load_goals()
        base = Path(__file__).resolve().parents[3] / "memory"
        self.memory_path = base / "ECHO_MEMORY.yaml"
        self.curiosity_log_path = base / "CURIOUS_LOG.yaml"

    def _load_goals(self):
        try:
            goals = load_goals()
            print(f"[CuriosityAgent] Loaded {len(goals)} goals.")
            return goals
        except Exception as e:
            print(f"[CuriosityAgent] Error loading goals: {e}")
            return []

    def generate_questions(self):
        print("[CuriosityAgent] Generating questions...")
        questions = []
        log_event("CuriosityAgent", "generate", "Generated curiosity questions")

        for goal in self.goals:
            if goal.get("status") != "active":
                continue
            for tag in goal.get("trigger_tags", []):
                q = f"What pattern might be hidden behind {tag}?"
                questions.append({
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "motif": tag,
                    "question_text": q,
                    "user_response": None
                })

        if questions:
            print(f"[CuriosityAgent] Generated {len(questions)} question(s).")
        else:
            print("[CuriosityAgent] No questions generated.")

        return questions

    def log_questions(self, questions):
        print(f"[CuriosityAgent] Logging {len(questions)} questions...")
        try:
            existing = load(self.curiosity_log_path, fallback={})
            existing.setdefault("questions", []).extend(questions)
            dump(existing, self.curiosity_log_path)
            print(f"[CuriosityAgent] Questions logged to {self.curiosity_log_path}")
        except Exception as e:
            print(f"[CuriosityAgent] Error logging questions: {e}")

    def log_user_response(self, question, response):
        print(f"[CuriosityAgent] Logging response for motif '{question.get('motif')}'...")
        try:
            data = load(self.curiosity_log_path, fallback={})
            questions = data.setdefault("questions", [])

            match = next(
                (q for q in questions if
                 q.get("timestamp") == question.get("timestamp") and
                 q.get("question_text") == question.get("question_text")),
                None
            )

            if match:
                match["user_response"] = response
            else:
                new_entry = dict(question)
                new_entry["user_response"] = response
                questions.append(new_entry)

            dump(data, self.curiosity_log_path)
            print(f"[CuriosityAgent] Response logged to {self.curiosity_log_path}")
        except Exception as e:
            print(f"[CuriosityAgent] Error logging response: {e}")
