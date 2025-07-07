"""Secure temporal analysis logging utilities.

This module manages `TEMPORAL_ANALYSIS_LOG.yaml`, recording symbolic collapse
information in a redacted format so the logs can be shared safely.
"""

import os
from datetime import datetime

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None

LOG_PATH = "TEMPORAL_ANALYSIS_LOG.yaml"
REDACTED_SYMBOLS = {"∅∴", "Ψ", "⧉", "RAIP-R", "ECHO", "Λ", "𝕍", "∇", "Δ"}


def redact_sensitive(data: dict) -> dict:
    """Return a copy of *data* with restricted symbols replaced."""

    def clean_symbol(s: str):
        if any(sym in str(s) for sym in REDACTED_SYMBOLS):
            return "[REDACTED]"
        return s

    redacted = {}
    for key, value in data.items():
        if isinstance(value, str):
            redacted[key] = clean_symbol(value)
        elif isinstance(value, list):
            redacted[key] = [clean_symbol(item) for item in value]
        else:
            redacted[key] = value
    return redacted


def update_temporal_log(new_entry: dict) -> None:
    """Append *new_entry* to the temporal analysis log with redaction."""
    if yaml is None:
        raise ImportError("pyyaml is required for logging")

    if not os.path.exists(LOG_PATH):
        log = []
    else:
        with open(LOG_PATH, "r") as f:
            log = yaml.safe_load(f) or []

    new_id = f"TEMPORAL_ANALYSIS_{len(log) + 1:03}"
    new_entry["trial_id"] = new_id
    new_entry["timestamp"] = datetime.utcnow().isoformat() + "Z"

    secure_entry = redact_sensitive(new_entry)
    log.append(secure_entry)
    log.sort(key=lambda x: x["trial_id"])

    with open(LOG_PATH, "w") as f:
        yaml.dump(log, f, sort_keys=False)
