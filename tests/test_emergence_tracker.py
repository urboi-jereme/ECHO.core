import os
import sys
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime import emergence_tracker


def test_check_emergence_logs(tmp_path, monkeypatch):
    log_file = tmp_path / "emergence_log.yaml"
    monkeypatch.setattr(emergence_tracker, "LOG_PATH", str(log_file))

    memory = [
        {
            "tags": ["intuition"],
            "symbolic_insight": "test insight",
            "resonance_score": 0.95,
        }
    ]
    goals = []

    events = emergence_tracker.check_emergence(memory, goals, beliefs=[])
    assert log_file.exists()
    data = yaml.safe_load(log_file.read_text())
    assert len(data["events"]) == len(events) == 1
    assert data["events"][0]["motif"] == "intuition"
