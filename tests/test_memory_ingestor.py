import pytest
from echo_core.tools.memory_ingestor import ingest_yaml
from echo_core.memory.echo_memory import load_memory


pytest.importorskip("yaml")

def test_ingest_yaml(tmp_path):
    mem = tmp_path / "ECHO_MEMORY.yaml"
    yaml_text = "- sentence: Example insight\n  subject: Example\n  predicate: insight\n  compression: Anchor. Act. Close."
    ingest_yaml(yaml_text, mem)
    data = load_memory(mem)
    assert data["echo_memory"][0]["symbolic_insight"] == "Example insight"


