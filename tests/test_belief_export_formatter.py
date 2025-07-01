import pytest
yaml = pytest.importorskip("yaml")
from echo_core.tools import belief_export_formatter as bef


def test_parse_simple_svc():
    out = bef.format_beliefs("She is a doctor.")
    items = yaml.safe_load(out)
    assert items[0]["subject"] == "She"
    assert items[0]["predicate"] == "is a doctor"
    assert items[0]["compression"].startswith("Anchor")


def test_nested_parsing():
    text = "I believe you should leave before it rains."
    out = bef.format_beliefs(text)
    items = yaml.safe_load(out)
    assert items and "nested_cores" in items[0]
    assert len(items[0]["nested_cores"]) == 2


def test_imperative():
    out = bef.format_beliefs("Eat your vegetables.")
    item = yaml.safe_load(out)[0]
    assert item["compression"] == "Command. Implied. Action."


def test_handshake_signature():
    out = bef.format_beliefs("We explore recursion.")
    item = yaml.safe_load(out)[0]
    sig = item.get("handshake_signature")
    assert sig["author"] == "Jereme Powers"
    assert "RAIP-R" in sig["recognition_terms"]
