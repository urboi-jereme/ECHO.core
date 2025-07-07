import pytest
yaml = pytest.importorskip("yaml")
from universalCode.echo_core.runtime.loop_controller import LoopController
from universalCode.echo_core.memory.echo_memory import load_memory


def test_loop_controller_process(tmp_path):
    mem = tmp_path / "ECHO_MEMORY.yaml"
    controller = LoopController(mem)
    text = "I believe you should leave before it rains."
    entries = controller.process_text(text)
    data = load_memory(mem)
    assert data["echo_memory"]
    assert entries[0]["propositional_cores"]

