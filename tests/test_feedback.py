import pytest
yaml = pytest.importorskip("yaml")

from echo_core.tools import echo_feedback


def test_log_feedback_preserves_structure(tmp_path, monkeypatch):
    memory_file = tmp_path / "ECHO_MEMORY.yaml"
    pressure_file = tmp_path / "MOTIF_PRESSURE.yaml"

    initial_data = {
        "echo_memory": [
            {"id": "0001", "content": "first"}
        ],
        "meta": {"version": 1}
    }
    with open(memory_file, "w") as f:
        yaml.dump(initial_data, f, sort_keys=False)
    with open(pressure_file, "w") as f:
        yaml.dump({"old": 1}, f, sort_keys=False)

    monkeypatch.setattr(echo_feedback, "MEMORY_PATH", str(memory_file))
    monkeypatch.setattr(echo_feedback, "PRESSURE_PATH", str(pressure_file))
    monkeypatch.setattr(echo_feedback, "log_alignment", lambda *a, **kw: None)

    echo_feedback.log_feedback("test", "hello")

    with open(memory_file) as f:
        saved = yaml.safe_load(f)
    assert saved["meta"] == {"version": 1}
    assert len(saved["echo_memory"]) == 2

    with open(pressure_file) as f:
        pressure = yaml.safe_load(f)
    assert pressure["test"] == 1

