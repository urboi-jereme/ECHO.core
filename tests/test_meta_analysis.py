import pytest
pytest.importorskip("yaml")

from universalCode.echo_core.agents.meta_analysis import MetaAnalysisAgent


def test_meta_analysis_detects_contradictions(tmp_path):
    mem = tmp_path / "ECHO_MEMORY.yaml"
    mem.write_text("echo_memory:\n- tags: [a]\n  status: active\n- tags: [a]\n  status: archived\n")
    assump = tmp_path / "ARRESTED_ASSUMPTIONS.yaml"
    assump.write_text("arrested_assumptions: []\n")

    agent = MetaAnalysisAgent(memory_file=mem, assumptions_file=assump)
    result = agent.evaluate_integrity()
    assert result["contradictions"]
