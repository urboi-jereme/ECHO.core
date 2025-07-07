from pathlib import Path
from datetime import datetime

from echo_core.utils.yaml_utils import load, dump

ROOT_DIR = Path(__file__).resolve().parents[3]
MEMORY_PATH = ROOT_DIR / 'memory' / 'ECHO_MEMORY.yaml'
PRESSURE_PATH = ROOT_DIR / 'memory' / 'MOTIF_PRESSURE.yaml'
PRIVATE_PATH = ROOT_DIR / 'memory' / 'ECHO_PRIVATE.yaml'
REPORTS_DIR = ROOT_DIR / '.private' / 'reports'


def load_memory(path: str | Path = MEMORY_PATH):
    path = Path(path)
    if not path.exists():
        return {'echo_memory': []}
    data = load(path, fallback={})
    if 'echo_memory' not in data:
        data['echo_memory'] = []
    return data


def save_memory(data, path: str | Path = MEMORY_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dump(data, path)


def append_memory_entry(entry: dict, path: str = MEMORY_PATH):
    data = load_memory(path)
    entries = data.get('echo_memory', [])
    entries.append(entry)
    data['echo_memory'] = entries
    save_memory(data, path)


def load_pressure(path: str | Path = PRESSURE_PATH):
    path = Path(path)
    if not path.exists():
        return {'motif_pressure': {}}
    data = load(path, fallback={})
    if 'motif_pressure' not in data:
        # Support legacy structure where file is just a dict of pressures
        if isinstance(data, dict):
            return {'motif_pressure': data}
        data = {'motif_pressure': {}}
    return data


def save_pressure(data, path: str | Path = PRESSURE_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dump(data, path)


def increment_pressure(tags, path: str = PRESSURE_PATH):
    if isinstance(tags, str):
        tags = [tags]
    data = load_pressure(path)
    pressure = data.get('motif_pressure', {})
    for tag in tags:
        pressure[tag] = pressure.get(tag, 0) + 1
    data['motif_pressure'] = pressure
    save_pressure(data, path)


def _load_private(path: str | Path = PRIVATE_PATH):
    path = Path(path)
    if not path.exists():
        return {'private_reflections': []}
    data = load(path, fallback={})
    if 'private_reflections' not in data:
        data['private_reflections'] = []
    return data


def _save_private(data, path: str | Path = PRIVATE_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dump(data, path)


def log_private_reflection(entry: dict, path: str = PRIVATE_PATH, reports_dir: str = REPORTS_DIR):
    """Store full reflection entry privately and archive report."""
    data = _load_private(path)
    reflections = data.get('private_reflections', [])
    reflections.append(entry)
    data['private_reflections'] = reflections
    _save_private(data, path)

    # archive full entry in reports directory
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = entry.get('timestamp') or datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    safe_ts = str(timestamp).replace(' ', '_').replace(':', '-')
    report_path = reports_dir / f'{safe_ts}.yaml'
    dump(entry, report_path)


def log_public_summary(entry: dict, path: str = MEMORY_PATH):
    """Store only symbolic summary of reflection in public memory."""
    public_fields = ['timestamp', 'tags', 'summary', 'motif', 'type', 'source']
    summary = {k: entry[k] for k in public_fields if k in entry}
    append_memory_entry(summary, path=path)


def sync_reflection(entry: dict, private_mode: bool = True):
    """Log reflection to private and public stores based on mode."""
    if private_mode:
        log_private_reflection(entry)
    log_public_summary(entry)
