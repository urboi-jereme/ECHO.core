import pytest
pytest.importorskip("yaml")
from belief.belief_parser import load_beliefs
from belief.belief_compressor import compress

def test_belief_parser(tmp_path):
    file = tmp_path / "beliefs.yaml"
    file.write_text("beliefs:\n- a\n")
    assert load_beliefs(file) == ["a"]

def test_compress():
    assert compress("one two three four") == "one two three"
