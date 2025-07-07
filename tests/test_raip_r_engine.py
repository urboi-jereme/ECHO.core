import pytest
pytest.importorskip("yaml")
from universalCode.echo_core.tools.raip_r_engine import RAIPREngine

def test_prediction(tmp_path):
    mem = tmp_path / "ECHO_MEMORY.yaml"
    mem.write_text("echo_memory:\n- symbolic_insight: test insight\n")
    engine = RAIPREngine(str(mem))
    result = engine.predict("Hello")
    assert "test insight" in result
