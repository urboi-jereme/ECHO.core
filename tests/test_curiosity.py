import os
import sys
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.curiosity_agent import CuriosityAgent


def test_log_user_response_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr('agents.curiosity_agent.load_goals', lambda: [])
    agent = CuriosityAgent()
    agent.curiosity_log_path = str(tmp_path / "CURIOUS_LOG.yaml")

    question = {
        "timestamp": "2025-01-01 00:00:00",
        "motif": "test",
        "question_text": "What?",
        "user_response": None,
    }
    agent.log_user_response(question, "answer")
    data = yaml.safe_load(open(agent.curiosity_log_path))
    assert data["questions"][0]["user_response"] == "answer"


def test_log_user_response_updates_existing(tmp_path, monkeypatch):
    monkeypatch.setattr('agents.curiosity_agent.load_goals', lambda: [])
    agent = CuriosityAgent()
    agent.curiosity_log_path = str(tmp_path / "CURIOUS_LOG.yaml")

    existing = {
        "questions": [
            {
                "timestamp": "2025-01-01 00:00:00",
                "motif": "test",
                "question_text": "What?",
                "user_response": None,
            }
        ]
    }
    with open(agent.curiosity_log_path, "w") as f:
        yaml.dump(existing, f)

    question = existing["questions"][0]
    agent.log_user_response(question, "new answer")
    data = yaml.safe_load(open(agent.curiosity_log_path))
    assert data["questions"][0]["user_response"] == "new answer"

