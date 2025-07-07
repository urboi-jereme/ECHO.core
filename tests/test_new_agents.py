import pytest
yaml = pytest.importorskip("yaml")

from universalCode.echo_core.agents.belief_input import BeliefInputAgent
from universalCode.echo_core.agents.emergence_scanner import EmergenceScanner


def test_belief_input_agent(tmp_path):
    mem = tmp_path / "ECHO_MEMORY.yaml"
    mem.write_text("echo_memory:\n- status: active\n  tags: [test]\n  resonance_score: 1.0\n")
    beliefs_file = tmp_path / "BELIEFS.yaml"
    beliefs_file.write_text("beliefs: []\n")

    agent = BeliefInputAgent(str(mem), str(beliefs_file))
    proposals = agent.propose_beliefs()
    assert proposals
    agent.add_belief("new belief")
    data = yaml.safe_load(beliefs_file.read_text())
    assert data["beliefs"] == ["new belief"]


def test_emergence_scanner_scan(tmp_path, monkeypatch):
    log_file = tmp_path / "log.yaml"

    mem = {"echo_memory": [{"tags": ["belief"], "resonance_score": 0.95, "symbolic_insight": "x"}]}
    goals = [{"goal": "g", "trigger_tags": ["belief"]}]
    beliefs = {"beliefs": ["belief"]}

    def fake_load(path, fallback=None):
        if path.endswith("ECHO_MEMORY.yaml"):
            return mem
        if path.endswith("GOALS.yaml"):
            return goals
        if path.endswith("BELIEFS.yaml"):
            return beliefs
        return fallback

    monkeypatch.setattr("agents.emergence_scanner.load", fake_load)

    scanner = EmergenceScanner(str(log_file))
    events = scanner.scan()
    assert log_file.exists()
    assert events
