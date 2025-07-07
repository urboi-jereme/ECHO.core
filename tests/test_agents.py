from pathlib import Path
import pytest

yaml = pytest.importorskip("yaml")
from universalCode.echo_core.agents import IntuitionAgent, NavigatorAgent, ModulatorAgent, CuriosityAgent
from universalCode.echo_core.memory.echo_memory import append_memory_entry, increment_pressure


def test_intuition_basic(tmp_path):
    mem = tmp_path / 'ECHO_MEMORY.yaml'
    append_memory_entry({'status': 'active', 'tags': ['test'], 'resonance_score': 1.0}, path=mem)
    agent = IntuitionAgent(mem)
    tags = agent.get_resonant_tags()
    assert tags and tags[0]['tag'] == 'test'


def test_navigator_prompts(tmp_path):
    mem = tmp_path / 'ECHO_MEMORY.yaml'
    append_memory_entry({'status': 'active', 'tags': ['x'], 'resonance_score': 1.0}, path=mem)
    agent = NavigatorAgent(mem)
    prompts = agent.get_next_prompt_targets()
    assert prompts


def test_modulator_updates(tmp_path, monkeypatch):
    pref = tmp_path / 'pref.yaml'
    pref.write_text('modulation_rules:\n- agent: Test\n  weight: 0.3\n')
    state = tmp_path / 'state.yaml'
    monkeypatch.setattr(ModulatorAgent, 'agent_state_path', state)
    mod = ModulatorAgent(pref, state)
    mod.run()
    assert state.exists()


def test_curiosity_question_logging(tmp_path, monkeypatch):
    log = tmp_path / 'CURIOSITY.yaml'
    monkeypatch.setattr(CuriosityAgent, '_load_goals', lambda self: [{'trigger_tags':['a'], 'status':'active'}])
    c = CuriosityAgent()
    c.curiosity_log_path = log
    qs = c.generate_questions()
    c.log_questions(qs)
    assert log.exists()
