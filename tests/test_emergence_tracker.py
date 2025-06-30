import os
import sys
import pytest

# Prefer using your robust utils
try:
    from yaml_utils import loads as safe_load_yaml
except ImportError:
    try:
        import yaml
        safe_load_yaml = lambda s: yaml.safe_load(s)
    except ImportError:
        pytest.skip("❌ Skipping test: PyYAML not available in this Codex sandbox.")

# Setup path and import the module under test
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

    # Read and parse YAML safely
    data = safe_load_yaml(log_file.read_text())
    assert len(data["events"]) == len(events) == 1
    assert data["events"][0]["motif"] == "intuition"
