"""YAML utilities with safe fallback behavior."""

from __future__ import annotations
from pathlib import Path, PurePath
from typing import Any

from yaml import dump as ydump
from yaml import load as yload

try:
    from yaml import CSafeDumper as SafeDumper
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper, SafeLoader  # type: ignore


def loads(stream: Any) -> Any:
    """Load YAML from a stream."""
    try:
        return yload(stream, Loader=SafeLoader) or {}
    except Exception as e:
        print(f"⚠️ YAML parse error: {e}")
        return {}


def dumps(data: Any) -> str:
    """Convert Python object to YAML string."""
    try:
        return ydump(data, Dumper=SafeDumper)
    except Exception as e:
        print(f"⚠️ YAML dump error: {e}")
        return ""


def load(fpath: str | PurePath) -> Any:
    """Load YAML from a file path."""
    try:
        return loads(Path(str(fpath)).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"❌ YAML file not found: {fpath}")
        return {}
    except Exception as e:
        print(f"⚠️ Error reading YAML from {fpath}: {e}")
        return {}


def dump(data: Any, outpath: str | PurePath) -> None:
    """Write YAML data to file."""
    try:
        Path(outpath).write_text(dumps(data), encoding="utf-8")
    except Exception as e:
        print(f"⚠️ Error writing YAML to {outpath}: {e}")
