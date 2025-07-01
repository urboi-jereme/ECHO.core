# belief_compressor.py v0.1.0
"""Compress belief statements using simple triad mapping."""

from __future__ import annotations


def compress(belief: str) -> str:
    words = belief.split()
    triad = words[:3] if len(words) >= 3 else words + ["."] * (3 - len(words))
    return " ".join(triad)


__all__ = ["compress"]
