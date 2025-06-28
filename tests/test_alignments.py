import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import yaml
from memory import alignments


def test_log_alignment_appends(tmp_path, monkeypatch):
    test_file = tmp_path / "RECURSIVE_ALIGNMENTS.yaml"
    test_file.write_text("recursive_alignments: []\n")
    monkeypatch.setattr(alignments, "ALIGNMENTS_PATH", str(test_file))

    other_file = tmp_path / "other.yaml"
    other_file.write_text("foo: bar\n")

    alignments.log_alignment(
        interaction={"summary": "test", "content": "text"},
        mirrored_tags=["a"],
        reasoning_path=["x"],
        agent_activations=["Agent"],
        score=1.0,
        notes="note",
        path=str(test_file)
    )

    data = alignments.load_alignments(str(test_file))
    assert len(data["recursive_alignments"]) == 1
    assert other_file.read_text() == "foo: bar\n"
