import pytest
yaml = pytest.importorskip("yaml")

from universalCode.echo_core.memory import echo_memory


def test_sync_reflection_private_and_public(tmp_path, monkeypatch):
    private_file = tmp_path / "ECHO_PRIVATE.yaml"
    public_file = tmp_path / "ECHO_MEMORY.yaml"
    reports_dir = tmp_path / ".private" / "reports"

    monkeypatch.setattr(echo_memory, "PRIVATE_PATH", str(private_file))
    monkeypatch.setattr(echo_memory, "MEMORY_PATH", str(public_file))
    monkeypatch.setattr(echo_memory, "REPORTS_DIR", str(reports_dir))

    entry = {
        "timestamp": "2025-01-01 00:00:00",
        "tags": ["t1"],
        "summary": "test summary",
        "content": "secret details",
    }

    echo_memory.sync_reflection(entry, private_mode=True)

    with open(private_file) as f:
        private_data = yaml.safe_load(f)
    assert private_data["private_reflections"][0]["content"] == "secret details"

    with open(public_file) as f:
        public_data = yaml.safe_load(f)
    assert public_data["echo_memory"][0]["summary"] == "test summary"

    report_files = list(reports_dir.iterdir())
    assert len(report_files) == 1
    report = yaml.safe_load(report_files[0].read_text())
    assert report["content"] == "secret details"


def test_sync_reflection_public_only(tmp_path, monkeypatch):
    private_file = tmp_path / "ECHO_PRIVATE.yaml"
    public_file = tmp_path / "ECHO_MEMORY.yaml"
    reports_dir = tmp_path / ".private" / "reports"

    monkeypatch.setattr(echo_memory, "PRIVATE_PATH", str(private_file))
    monkeypatch.setattr(echo_memory, "MEMORY_PATH", str(public_file))
    monkeypatch.setattr(echo_memory, "REPORTS_DIR", str(reports_dir))

    entry = {
        "timestamp": "2025-01-02 00:00:00",
        "tags": ["t2"],
        "summary": "only public",
        "content": "private text",
    }

    echo_memory.sync_reflection(entry, private_mode=False)

    assert not private_file.exists()
    with open(public_file) as f:
        public_data = yaml.safe_load(f)
    assert public_data["echo_memory"][0]["summary"] == "only public"
    assert not reports_dir.exists()
