# belief_parser.py v0.1.0
"""Parse belief files into internal structures."""

import yaml
from pathlib import Path


def load_beliefs(path: str | Path) -> list[dict]:
    data = yaml.safe_load(Path(path).read_text())
    return data.get("beliefs", []) if isinstance(data, dict) else data


__all__ = ["load_beliefs"]
