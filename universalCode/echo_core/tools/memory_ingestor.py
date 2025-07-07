# memory_ingestor.py v0.1.0
"""Utilities for ingesting belief entries into ECHO memory."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, Dict, Any

from echo_core.utils.yaml_utils import load, dump, loads

BASE = Path(__file__).resolve().parents[3] / "memory"
MEMORY_PATH = BASE / "ECHO_MEMORY.yaml"


def ingest_entries(entries: Iterable[Dict[str, Any]], memory_file: str | Path = MEMORY_PATH) -> None:
    """Append parsed belief entries into the memory file."""
    data = load(memory_file, fallback={"echo_memory": []})
    mem = data.get("echo_memory", [])
    for entry in entries:
        mem.append({
            "id": f"{len(mem)+1:04d}",
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "symbolic_insight": entry.get("sentence", ""),
            "subject": entry.get("subject"),
            "predicate": entry.get("predicate"),
            "compression": entry.get("compression"),
            "status": "active",
            "tags": entry.get("tags", []),
        })
    data["echo_memory"] = mem
    dump(data, memory_file)


def ingest_yaml(text: str, memory_file: str | Path = MEMORY_PATH) -> None:
    """Ingest YAML-formatted beliefs."""
    entries = loads(text) or []
    if isinstance(entries, dict):
        entries = [entries]
    ingest_entries(entries, memory_file)

__all__ = ["ingest_entries", "ingest_yaml"]
