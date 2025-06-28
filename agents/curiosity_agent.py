import os
import yaml
from datetime import datetime

# Logging support (optional)
try:
    from echo_logger import log_agent_activation
    log_agent_activation("CuriosityAgent", reason="Initialization")
except ImportError:
    def log_agent_activation(*args, **kwargs): pass  # Silent fallback if logger missing

# Correct import path for goal handling
from memory.goals import load_goals

class CuriosityAgent:
    def __init__(self):
        print("[CuriosityAgent] Initializing...")
        self.goals = self._load_goals()
        self.memory_path = os.path.join(os.path.dirname(__file__), "..", "memory", "ECHO_MEMORY.yaml")
        self.curiosity_log_path = os.path.join(os.path.dirname(__file__), "..", "memory", "CURIOUS_LOG.yaml")

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
            if os.path.exists(self.curiosity_log_path):
                with open(self.curiosity_log_path, "r") as f:
                    existing = yaml.safe_load(f) or {}
            else:
                existing = {}

            existing.setdefault("questions", []).extend(questions)

            with open(self.curiosity_log_path, "w") as f:
                yaml.dump(existing, f, sort_keys=False)
            print(f"[CuriosityAgent] Questions logged to {self.curiosity_log_path}")
        except Exception as e:
            print(f"[CuriosityAgent] Error logging questions: {e}")
