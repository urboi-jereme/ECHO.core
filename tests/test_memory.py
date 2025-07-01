import pytest
yaml = pytest.importorskip("yaml")
from echo_core.memory import echo_memory as em


def test_append_and_pressure(tmp_path):
    mem = tmp_path / 'ECHO.yaml'
    pressure = tmp_path / 'PRESS.yaml'
    em.append_memory_entry({'status':'active', 'tags':['x'], 'resonance_score':1}, path=mem)
    em.increment_pressure('x', path=pressure)
    data = em.load_memory(mem)
    press = em.load_pressure(pressure)
    assert data['echo_memory']
    assert press['motif_pressure']['x'] == 1
