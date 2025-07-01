from __future__ import annotations

"""Triadic symbol validator."""

from pathlib import Path
from typing import List

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

SEMANTIC_ROLES = {
    "🔥": "Leader",
    "🪞": "Mirror",
    "🗿": "Foundation",
    "🌊": "Flow",
    "⭐": "Inspiration",
    "⚖️": "Balance",
    "🔗": "Connection",
}

TRIAD_PATTERNS = [
    {"Leader", "Mirror", "Foundation"},
    {"Inspiration", "Reflection", "Action"},
    {"Energy", "Flow", "Balance"},
]

RECURSIVE_MAP = {
    "Leader": ["guide", "ignite"],
    "Mirror": ["reflect", "adapt"],
    "Foundation": ["ground", "support"],
    "Flow": ["cycle", "movement"],
    "Inspiration": ["spark", "vision"],
    "Balance": ["equilibrium", "justice"],
    "Connection": ["link", "bridge"],
}


def validate_triad(symbols: List[str]) -> float:
    """Return validation score for a triad of symbols."""
    if len(symbols) != 3:
        return 0.0

    roles = [SEMANTIC_ROLES.get(s) for s in symbols]
    coverage = sum(role is not None for role in roles) / 3.0
    roles = [r for r in roles if r]

    if set(roles) in [set(p) for p in TRIAD_PATTERNS]:
        coherence = 1.0
    elif len(set(roles)) == 3:
        coherence = 0.7
    else:
        coherence = 0.0

    recursion = 1.0 if all(r in RECURSIVE_MAP for r in roles) else 0.0
    score = round((coverage + coherence + recursion) / 3.0, 3)
    return score


def _load_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load SYMBOL_MAP.yaml")
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def _dump_yaml(path: Path, data: dict) -> None:
    if yaml is None:
        return
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def main() -> None:
    path = Path("SYMBOL_MAP.yaml")
    data = _load_yaml(path)
    updated = False
    for key, entry in data.items():
        score = validate_triad(entry.get("symbols", []))
        if entry.get("validation_score") != score:
            entry["validation_score"] = score
            updated = True
    if updated:
        _dump_yaml(path, data)
    if yaml is not None:
        print(yaml.safe_dump(data, sort_keys=False))


if __name__ == "__main__":  # pragma: no cover
    main()
