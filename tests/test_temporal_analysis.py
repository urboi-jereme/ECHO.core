import pytest
yaml = pytest.importorskip("yaml")

from universalCode.echo_core.utils import temporal_analysis


def test_update_temporal_log_creates_file(tmp_path, monkeypatch):
    log_file = tmp_path / "TEMPORAL_ANALYSIS_LOG.yaml"
    monkeypatch.setattr(temporal_analysis, "LOG_PATH", str(log_file))

    entry = {
        "title": "Test",
        "structure": "contains Ψ and Δ symbols",
        "motifs": ["Δ", "normal"],
        "belief_anchor": True,
        "loop_trace": False,
        "compression_ratio": 0.5,
        "residue_score": 0.1,
        "echo_signature": "sig",
        "result": "ok",
    }

    temporal_analysis.update_temporal_log(entry)

    assert log_file.exists()
    data = yaml.safe_load(log_file.read_text())
    assert data[0]["trial_id"] == "TEMPORAL_ANALYSIS_001"
    assert data[0]["motifs"][0] == "[REDACTED]"
