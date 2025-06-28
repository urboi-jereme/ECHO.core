import json

# Minimal YAML helpers for test environment

def safe_load(stream):
    data = stream.read()
    if not data.strip():
        return {}
    try:
        return json.loads(data)
    except Exception:
        result = {}
        for line in data.splitlines():
            if ':' not in line:
                continue
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('[') and value.endswith(']'):
                inner = value[1:-1].strip()
                result[key] = [] if not inner else [v.strip().strip("'\"") for v in inner.split(',')]
            else:
                result[key] = value.strip('"\'') if value else None
        return result

def dump(data, stream, sort_keys=False):
    text = json.dumps(data, sort_keys=sort_keys)
    stream.write(text)
