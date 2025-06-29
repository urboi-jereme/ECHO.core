# yaml_utils.py

from __future__ import annotations
from pathlib import Path, PurePath
from typing import Any
from yaml import dump as ydump, load as yload

try:
    from yaml import CSafeDumper as SafeDumper
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper, SafeLoader


def loads(stream: Any) -> Any:
    try:
        return yload(stream, Loader=SafeLoader) or {}
    except Exception as e:
        print(f"⚠️ YAML parse error: {e}")
        return {}


def dumps(data: Any) -> str:
    try:
        return ydump(data, Dumper=SafeDumper)
    except Exception as e:
        print(f"⚠️ YAML dump error: {e}")
        return ""


def load(fpath: str | PurePath, fallback: Any = None) -> Any:
    """Load YAML from file, inject fallback if file is empty or invalid."""
    fpath = Path(str(fpath))
    try:
        raw = fpath.read_text(encoding="utf-8").strip()
        if not raw:
            print(f"⚠️ {fpath.name} was empty. Injecting fallback...")
            dump(fallback, fpath)
            return fallback
        parsed = yload(raw, Loader=SafeLoader)
        if parsed is None:
            print(f"⚠️ {fpath.name} was null. Injecting fallback...")
            dump(fallback, fpath)
            return fallback
        return parsed
    except FileNotFoundError:
        print(f"❌ YAML file not found: {fpath}")
        return fallback
    except Exception as e:
        print(f"⚠️ Error reading YAML from {fpath}: {e}")
        return fallback


def dump(data: Any, outpath: str | PurePath) -> None:
    try:
        Path(outpath).write_text(dumps(data), encoding="utf-8")
    except Exception as e:
        print(f"⚠️ Error writing YAML to {outpath}: {e}")
