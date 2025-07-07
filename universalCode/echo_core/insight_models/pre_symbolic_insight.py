"""Pre-symbolic insight detection utilities."""

from __future__ import annotations

from typing import Any

PRE_SYMBOLIC_KEYWORDS = {
    "sacred",
    "pre-symbolic",
    "pre_symbolic",
    "presymbolic",
    "ineffable",
    "awe",
    "grief",
    "unity",
    "nameless",
}


def is_pre_symbolic(insight: str | Any) -> bool:
    """Return True if the insight should be preserved without symbolic mutation."""
    text = ""
    tags: list[str] = []

    if isinstance(insight, dict):
        text = str(insight.get("insight") or insight.get("text") or "")
        raw_tags = insight.get("tags", [])
        if isinstance(raw_tags, (list, tuple)):
            tags = [str(t).lower() for t in raw_tags]
        if insight.get("preserve") is True:
            return True
    else:
        text = str(insight)

    lower_text = text.lower()
    if any(k in lower_text for k in PRE_SYMBOLIC_KEYWORDS):
        return True
    if any(k in tags for k in PRE_SYMBOLIC_KEYWORDS):
        return True
    if (
        isinstance(insight, str)
        and len(insight.split()) == 1
        and len(insight) >= 32
        and all(ch in "0123456789abcdef" for ch in insight.lower())
    ):
        return True
    return False


__all__ = ["is_pre_symbolic"]
