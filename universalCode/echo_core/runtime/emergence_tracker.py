# runtime/emergence_tracker.py
"""Utility for tracking symbolic emergence events during runtime."""

import os
from datetime import datetime, timezone
from typing import Any, Iterable

from echo_core.utils.yaml_utils import load, dump

# Log file lives at project root
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "emergence_log.yaml"


_MOTIFS = {"intuition", "belief", "paradox", "resonance"}


def _contains_motif(text: str) -> str | None:
    """Return first motif present in text, if any."""
    text_lower = text.lower()
    for motif in _MOTIFS:
        if motif in text_lower:
            return motif
    return None


def check_emergence(memory: Iterable[dict], goals: Iterable[dict], beliefs: Iterable[Any] | None = None):
    """Scan inputs for high-resonance motifs and log any emergence events."""
    events: list[dict] = []

    for entry in memory:
        motif = None
        tags = [str(t).lower() for t in entry.get("tags", [])]
        for m in _MOTIFS:
            if m in tags:
                motif = m
                break
        if not motif:
            motif = _contains_motif(str(entry))
        if motif and entry.get("resonance_score", 0) >= 0.9:
            events.append({
                "motif": motif,
                "source": "memory",
                "evidence": entry.get("symbolic_insight") or entry.get("reflection"),
            })

    for goal in goals:
        if not isinstance(goal, dict):
            continue  # skip malformed goal
        motif = None
        tags = [str(t).lower() for t in goal.get("trigger_tags", [])]
        for m in _MOTIFS:
            if m in tags:
                motif = m
                break
        if not motif:
            motif = _contains_motif(str(goal.get("goal", "")))
        if motif:
            events.append({
                "motif": motif,
                "source": "goal",
                "evidence": goal.get("goal"),
            })

    if beliefs:
        for belief in beliefs:
            motif = _contains_motif(str(belief))
            if motif:
                events.append({
                    "motif": motif,
                    "source": "belief",
                    "evidence": str(belief),
                })

    if events:
        log = load(LOG_PATH, fallback={"events": []})
        log_events = log.get("events", [])
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        for ev in events:
            ev_entry = {
                "timestamp": timestamp,
                "motif": ev["motif"],
                "source": ev["source"],
                "evidence": ev.get("evidence"),
            }
            log_events.append(ev_entry)
        dump({"events": log_events}, LOG_PATH)

    return events

