import pytest
from datetime import timezone, datetime as dt
from echo_core.runtime import echo_daemon


def test_daemon_timestamp_utc(monkeypatch):
    captured = {}

    class DummyDateTime:
        @staticmethod
        def now(tz=None):
            captured['tz'] = tz
            return dt(2000, 1, 1, tzinfo=tz)

    monkeypatch.setattr(echo_daemon, 'datetime', DummyDateTime)

    class DummyIntuition:
        def get_resonant_tags(self):
            return []

    class DummyNavigator:
        def get_next_prompt_targets(self):
            return []

    class DummyCuriosity:
        def generate_questions(self):
            return []

    class DummyModulator:
        def run(self):
            pass

    monkeypatch.setattr(echo_daemon, 'IntuitionAgent', DummyIntuition)
    monkeypatch.setattr(echo_daemon, 'NavigatorAgent', DummyNavigator)
    monkeypatch.setattr(echo_daemon, 'CuriosityAgent', DummyCuriosity)
    monkeypatch.setattr(echo_daemon, 'ModulatorAgent', DummyModulator)

    def fake_sleep(_):
        raise SystemExit()

    monkeypatch.setattr(echo_daemon.time, 'sleep', fake_sleep)

    with pytest.raises(SystemExit):
        echo_daemon.daemon_loop()

    assert captured['tz'] == timezone.utc
