import os
import sys
import yaml
from typing import Dict


def setup_paths(project_root: str | None = None) -> Dict[str, str]:
    """Configure sys.path and return commonly used file paths."""
    root = os.path.abspath(project_root or os.getcwd())

    for sub in ("", "agents", "memory", "runtime"):
        path = os.path.join(root, sub) if sub else root
        if path not in sys.path:
            sys.path.insert(0, path)

    paths = {
        "PROJECT_ROOT": root,
        "ECHO_MEMORY_PATH": os.path.join(root, "memory", "ECHO_MEMORY.yaml"),
        "MOTIF_PRESSURE_PATH": os.path.join(root, "memory", "MOTIF_PRESSURE.yaml"),
        "AGENT_STATE_PATH": os.path.join(root, "memory", "AGENT_STATE.yaml"),
        "GOALS_PATH": os.path.join(root, "memory", "GOALS.yaml"),
        "META_PREFERENCES_PATH": os.path.join(root, "memory", "META_PREFERENCES.yaml"),
        "RECURSIVE_ALIGNMENTS_PATH": os.path.join(root, "memory", "RECURSIVE_ALIGNMENTS.yaml"),
        "JOURNAL_LOG_PATH": os.path.join(root, "journal", "ECHO_LOG.md"),
    }
    return paths


def verify_structure(project_root: str) -> None:
    """Print the presence of required directories and files."""
    required_dirs = ["agents", "memory", "journal", "runtime"]
    required_files = {
        "memory": [
            "AGENT_STATE.yaml",
            "ECHO_MEMORY.yaml",
            "GOALS.yaml",
            "META_PREFERENCES.yaml",
            "MOTIF_PRESSURE.yaml",
            "RECURSIVE_ALIGNMENTS.yaml",
        ],
        "journal": ["ECHO_LOG.md", "WORKFLOW_JOURNAL.md"],
    }

    print("\nVerifying core directory structure...")
    for d in required_dirs:
        path = os.path.join(project_root, d)
        if not os.path.isdir(path):
            print(f"❌ ERROR: Required directory '{path}' not found. Please ensure you are running this notebook from the repository root.")
        else:
            print(f"✅ Found directory: {d}/")
            if d in required_files:
                for f_name in required_files[d]:
                    f_path = os.path.join(path, f_name)
                    if not os.path.exists(f_path):
                        print(f"   ⚠️  Warning: Missing file '{f_name}' in '{d}/'. Some functionalities might be limited.")
                    else:
                        print(f"   ✅ Found file: {f_name}")
    print("\nSetup complete. You can now import modules from ECHO.core.")


def load_yaml(file_path: str) -> dict:
    """Load YAML content from a file, returning an empty dict if missing."""
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            return data if data is not None else {}
    except FileNotFoundError:
        print(f"Warning: File not found at {file_path}. Returning empty dictionary.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error loading YAML from {file_path}: {e}")
        return {}


def save_yaml(file_path: str, data: dict, mode: str = "w") -> None:
    """Persist YAML data to a file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, mode) as f:
            try:
                yaml.dump(data, f, sort_keys=False, default_flow_style=False)
            except TypeError:
                yaml.dump(data, f, sort_keys=False)
        print(f"Successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving YAML to {file_path}: {e}")


def append_yaml_list(file_path: str, new_entry: dict, list_key: str | None = None) -> None:
    """Append a new entry to a YAML file containing a list."""
    existing_data = load_yaml(file_path)

    if list_key:
        if list_key not in existing_data or not isinstance(existing_data[list_key], list):
            existing_data[list_key] = []
        existing_data[list_key].append(new_entry)
    else:
        if not isinstance(existing_data, list):
            existing_data = []
        existing_data.append(new_entry)

    save_yaml(file_path, existing_data)
    print(f"Appended new entry to {file_path}")
