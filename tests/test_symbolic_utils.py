import pytest
from universalCode.echo_core.symbolic import symbolic_utils as su


def test_decompose_and_identify():
    base = su.decompose("Recursion meets paradox")
    assert "recursion" in base
    motif = su.identify_motif(base)
    assert motif in su.MOTIF_MAP.values()


def test_analyze_commonality():
    relation, confidence = su.analyze_commonality("recursion", "loop")
    assert relation in {"coherent", "tensional", "discordant"}
    assert 0.0 <= confidence <= 1.0


def test_refine_levels():
    refined, level = su.refine("recursion paradox", ["recursion", "paradox"], "tension")
    assert level >= 2
    assert refined
