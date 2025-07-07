# echo_core/glyph_engine.py

from typing import List, Dict
import os
import json

# Optional: Enrich with full glyph definitions from glyphs/index.json
GLYPH_INDEX_PATH = os.path.join("glyphs", "index.json")

# --- Primary Soft Glyph Map (Keyword triggers) ---
GLYPH_MAP = {
    "collapse": "Δ",
    "insight": "Δ",
    "paradox": "🌀",
    "loop": "⟲",
    "belief": "𝕍",
    "symbol became real": "🝊",
    "containment": "Ω",
    "limit": "Ω",
    "multiplicity": "✴︎",
    "motif": "⧉",
    "compression": "∇",
    "audit": "⟲",
    "boundary": "Ω"
}

# ------------------------------------------
# 🔍 Soft Parse: Detect Glyphs from Keywords
# ------------------------------------------
def parse_glyphs(text: str) -> List[str]:
    """Detects glyphs from user input using keyword mapping."""
    detected = []
    lowered = text.lower()
    for keyword, glyph in GLYPH_MAP.items():
        if keyword in lowered and glyph not in detected:
            detected.append(glyph)
    return detected


# ------------------------------------------
# 🔮 Load Full Glyph Definitions (Optional)
# ------------------------------------------
def load_glyphs(path: str = GLYPH_INDEX_PATH) -> List[Dict]:
    """Loads full glyph definitions from JSON index."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Glyph index not found at {path}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in {path}")
        return []


# ------------------------------------------
# 🧬 Enrich: Add Metadata from index.json
# ------------------------------------------
def enrich_glyph(glyph_char: str) -> Dict[str, str]:
    """Returns enriched glyph data from index.json"""
    glyphs = load_glyphs()
    match = next((g for g in glyphs if g.get("symbol") == glyph_char), None)
    return match or {
        "symbol": glyph_char,
        "name": "Unknown",
        "meaning": "No description available.",
        "id": None
    }


# ------------------------------------------
# 🧾 Describe Glyphs (for UI or logs)
# ------------------------------------------
def describe_glyphs(glyphs: List[str]) -> Dict[str, str]:
    """Returns minimal glyph meanings for given glyph list."""
    return {g: enrich_glyph(g)["meaning"] for g in glyphs}
