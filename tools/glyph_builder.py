# tools/glyph_builder.py

import json
import os

GLYPH_PATH = os.path.join("glyphs", "index.json")

def load_glyphs():
    try:
        with open(GLYPH_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_glyphs(glyphs):
    with open(GLYPH_PATH, "w", encoding="utf-8") as f:
        json.dump(glyphs, f, indent=2, ensure_ascii=False)

def add_glyph():
    glyph = {}
    glyph["id"] = input("🆔 ID: ")
    glyph["symbol"] = input("🔣 Symbol (glyph): ")
    glyph["name"] = input("📛 Name: ")
    glyph["meaning"] = input("📖 Meaning: ")
    glyph["activation_code"] = input("⚙️ Activation code (optional): ")

    void = input("⬛ Void mode? (y/n): ").lower()
    if void == "y":
        glyph["void_mode"] = True
        pattern = []
        print("🔲 Enter background pattern lines (blank line to finish):")
        while True:
            line = input()
            if line.strip() == "":
                break
            pattern.append(line)
        glyph["background_pattern"] = pattern

    glyphs = load_glyphs()
    glyphs.append(glyph)
    save_glyphs(glyphs)
    print(f"\n✅ Glyph '{glyph['id']}' added.")

if __name__ == "__main__":
    add_glyph()
