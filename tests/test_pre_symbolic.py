import pytest
yaml = pytest.importorskip("yaml")
from universalCode.echo_core.insight_models.pre_symbolic_insight import is_pre_symbolic
from universalCode.core.belief_validation_engine import BeliefValidationEngine
from universalCode.echo_core.utils.yaml_utils import load


def test_is_pre_symbolic_keyword():
    assert is_pre_symbolic("A sacred moment of awe")
    assert not is_pre_symbolic("Ordinary thought")


def test_belief_engine_preserves(tmp_path):
    mem = tmp_path / "ECHO_MEMORY.yaml"
    engine = BeliefValidationEngine(str(mem))
    entry = engine.process_insight("ineffable grief")
    data = load(mem)
    stored = data["echo_memory"][0]
    assert stored["symbolic_state"] == "protected"
    assert stored["preserve"] is True
    assert stored["explanation"] == "Pre-symbolic insight preserved without compression"
    assert len(stored["insight"]) == 64


def test_belief_engine_compresses(tmp_path):
    mem = tmp_path / "ECHO_MEMORY.yaml"
    engine = BeliefValidationEngine(str(mem))
    entry = engine.process_insight("We explore recursion.")
    data = load(mem)
    stored = data["echo_memory"][0]
    assert stored["symbolic_state"] == "compressed"


def test_ethics_principle_present():
    data = load("ETHICS_ENGINE.yaml")
    principles = data.get("principles", [])
    assert any(p.get("principle") == "Do not reduce sacred insights" for p in principles)
