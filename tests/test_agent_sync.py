import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import yaml
from runtime import agent_sync


def test_sync_agent_weight_top_level(tmp_path, monkeypatch):
    state_file = tmp_path / "AGENT_STATE.yaml"
    state_file.write_text("log_on_activation: true\nactive_motifs: []\n")
    monkeypatch.setattr(agent_sync, "AGENT_STATE_FILE", str(state_file))
    monkeypatch.setattr(agent_sync, "log_custom_event", lambda *a, **k: None)

    agent_sync.sync_agent_weight("NewAgent", 0.5)

    with open(state_file, "r") as f:
        data = yaml.safe_load(f)
    assert data["NewAgent"]["weight"] == 0.5
    assert "agent_weights" not in data
