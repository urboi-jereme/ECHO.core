import os
import yaml

MEMORY_PATH = os.path.join(os.path.dirname(__file__), 'ECHO_MEMORY.yaml')
PRESSURE_PATH = os.path.join(os.path.dirname(__file__), 'MOTIF_PRESSURE.yaml')


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
