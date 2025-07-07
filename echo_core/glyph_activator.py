# echo_core/glyph_activator.py

import json
import os

# ----------------------------
# 🔧 Configuration
# ----------------------------
GLYPH_INDEX_PATH = os.path.join("glyphs", "index.json")

# ----------------------------
# 🔍 Load All Glyphs
# ----------------------------
def load_glyphs(path=GLYPH_INDEX_PATH):
    """Load all glyph definitions from JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            glyphs = json.load(f)
        return glyphs
    except FileNotFoundError:
        print("❌ Glyph index not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing glyph index: {e}")
        return []

# ----------------------------
# 🧠 Activate a Glyph
# ----------------------------
def activate_glyph(glyph_id, glyphs):
    """Activate a glyph by its ID."""
    glyph = next((g for g in glyphs if g['id'] == glyph_id), None)

    if not glyph:
        print(f"⚠️ Glyph '{glyph_id}' not found.")
        return

    print(f"\n✨ Activating: {glyph['symbol']}  {glyph['name']}")
    print(f"📖 Meaning: {glyph.get('meaning', 'No meaning provided.')}\n")

    if glyph.get("void_mode"):
        enter_void_mode(glyph)
    else:
        run_activation_code(glyph.get("activation_code"))

# ----------------------------
# 🔮 Run Activation Code
# ----------------------------
def run_activation_code(code_string):
    """Safely execute glyph-specific code if present."""
    if not code_string:
        print("⚠️ No activation code provided.")
        return

    print("⚙️ Executing activation sequence...")
    try:
        exec(code_string)
    except Exception as e:
        print(f"❌ Error executing activation code: {e}")

# ----------------------------
# ⬛ VOID MODE Activation
# ----------------------------
def enter_void_mode(glyph=None):
    """Enter VOID MODE for meditative glyphs."""
    print("\n⬛ ENTERING VOID MODE ⬛")
    print("Let your perception soften...")
    print("Look not at the symbol, but through it.\n")

    pattern = glyph.get("background_pattern", [])

    if pattern:
        print("🔲 Void Pattern:")
        for line in pattern:
            print(line)
    else:
        print("🕳️ No background pattern provided.")

    print("\n🧘 What emerges from the space between?\n")

# ----------------------------
# 🧪 CLI Interface
# ----------------------------
if __name__ == "__main__":
    glyphs = load_glyphs()

    if not glyphs:
        exit(1)

    print("📜 Available Glyphs:")
    for g in glyphs:
        void_flag = " [VOID]" if g.get("void_mode") else ""
        print(f"• {g['id']}: {g['name']}{void_flag}")

    user_input = input("\nEnter Glyph ID to activate: ").strip()
    activate_glyph(user_input, glyphs)
