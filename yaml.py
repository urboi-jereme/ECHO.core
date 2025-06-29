# yaml.py
import yaml

def load_yaml(path):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f) or []
    except Exception as e:
        print(f"⚠️ Error loading YAML from {path}: {e}")
        return []

def save_yaml(path, data):
    try:
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
    except Exception as e:
        print(f"⚠️ Error saving YAML to {path}: {e}")
