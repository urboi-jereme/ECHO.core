import os
from datetime import datetime
import yaml

MEMORY_PATH = os.path.join(os.path.dirname(__file__), 'ECHO_MEMORY.yaml')
PRESSURE_PATH = os.path.join(os.path.dirname(__file__), 'MOTIF_PRESSURE.yaml')
PRIVATE_PATH = os.path.join(os.path.dirname(__file__), 'ECHO_PRIVATE.yaml')
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.private', 'reports')


def load_memory(path: str = MEMORY_PATH):
    if not os.path.exists(path):
        return {'echo_memory': []}
    with open(path, 'r') as f:
        data = yaml.safe_load(f) or {}
    if 'echo_memory' not in data:
        data['echo_memory'] = []
    return data


def save_memory(data, path: str = MEMORY_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)


def append_memory_entry(entry: dict, path: str = MEMORY_PATH):
    data = load_memory(path)
    entries = data.get('echo_memory', [])
    entries.append(entry)
    data['echo_memory'] = entries
    save_memory(data, path)


def load_pressure(path: str = PRESSURE_PATH):
    if not os.path.exists(path):
        return {'motif_pressure': {}}
    with open(path, 'r') as f:
        data = yaml.safe_load(f) or {}
    if 'motif_pressure' not in data:
        # Support legacy structure where file is just a dict of pressures
        if isinstance(data, dict):
            return {'motif_pressure': data}
        data = {'motif_pressure': {}}
    return data


def save_pressure(data, path: str = PRESSURE_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)


def increment_pressure(tags, path: str = PRESSURE_PATH):
    if isinstance(tags, str):
        tags = [tags]
    data = load_pressure(path)
    pressure = data.get('motif_pressure', {})
    for tag in tags:
        pressure[tag] = pressure.get(tag, 0) + 1
    data['motif_pressure'] = pressure
    save_pressure(data, path)


def _load_private(path: str = PRIVATE_PATH):
    if not os.path.exists(path):
        return {'private_reflections': []}
    with open(path, 'r') as f:
        data = yaml.safe_load(f) or {}
    if 'private_reflections' not in data:
        data['private_reflections'] = []
    return data


def _save_private(data, path: str = PRIVATE_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)


def log_private_reflection(entry: dict, path: str = PRIVATE_PATH, reports_dir: str = REPORTS_DIR):
    """Store full reflection entry privately and archive report."""
    data = _load_private(path)
    reflections = data.get('private_reflections', [])
    reflections.append(entry)
    data['private_reflections'] = reflections
    _save_private(data, path)

    # archive full entry in reports directory
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = entry.get('timestamp') or datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    safe_ts = str(timestamp).replace(' ', '_').replace(':', '-')
    report_path = os.path.join(reports_dir, f'{safe_ts}.yaml')
    with open(report_path, 'w') as f:
        yaml.dump(entry, f, sort_keys=False)


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
