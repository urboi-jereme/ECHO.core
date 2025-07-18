import pytest
yaml = pytest.importorskip("yaml")

from universalCode.echo_core.agents.linguistic_divergence import LinguisticDivergenceAuditor


def test_amae_translation_divergence(tmp_path):
    pipeline = tmp_path / "CURIOSITY_PIPELINE.yaml"
    auditor = LinguisticDivergenceAuditor(str(pipeline), threshold=0.5)
    score = auditor.audit("甘え", "dependence", lang1="ja", lang2="en")
    assert score >= 0.5

    data = yaml.safe_load(pipeline.read_text())
    assert data["divergences"][0]["term1"] == "甘え"
    assert data["divergences"][0]["term2"] == "dependence"
