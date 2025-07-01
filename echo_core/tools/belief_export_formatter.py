"""Belief export formatter.

This module converts raw sentences into YAML-formatted belief entries for
ingestion by ECHO.Core. Each entry contains a sentence, subject, predicate,
and a three-word compression that summarizes the structure. Nested clauses are
recursively parsed as ``nested_cores``.
"""

from __future__ import annotations

import re
from typing import Iterable

from echo_core.utils.yaml_utils import dumps


def _parse_sentence(sentence: str) -> dict:
    """Parse a sentence into a belief entry dictionary."""

    text = sentence.strip()
    nested: list[dict] = []

    # Extract subordinate clauses first
    connectors = [" before ", " after ", " because ", " if ", " when ", " that "]
    for conn in connectors:
        if conn in text:
            main, sub = text.split(conn, 1)
            nested.append(_parse_sentence(sub.strip().rstrip(".")))
            text = main.strip()
            break

    # Handle "should" phrases as nested suggestions
    should_match = re.search(r"(\b\w+\b should[^.!?]+)", text)
    if should_match:
        phrase = should_match.group(1).strip()
        nested.append(_parse_sentence(phrase))
        text = text.replace(phrase, phrase.split()[0], 1).strip()

    core = text.rstrip(".!?")
    words = core.split()
    subject = words[0] if words else ""
    predicate = " ".join(words[1:]) if len(words) > 1 else ""

    if sentence.endswith("!") or words[0].lower() in {"eat", "fire", "run", "stop", "go"}:
        compression = "Command. Implied. Action."
    elif any(tok in {"is", "are", "am", "was", "were"} for tok in words[1:2]):
        compression = "Anchor. Is. Define."
    elif len(words) >= 3:
        compression = "Anchor. Flow. Impact."
    else:
        compression = "Anchor. Act. Close."

    entry = {
        "sentence": sentence.strip(),
        "subject": subject,
        "predicate": predicate,
        "compression": compression,
    }
    if nested:
        entry["nested_cores"] = nested
    return entry


def format_beliefs(text: str | Iterable[str]) -> str:
    """Return YAML representing parsed belief entries from text."""

    if isinstance(text, str):
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    else:
        sentences = [s.strip() for s in text if s.strip()]
    entries = [_parse_sentence(s) for s in sentences]
    return dumps(entries)


__all__ = ["format_beliefs"]

