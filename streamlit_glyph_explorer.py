# streamlit_glyph_explorer.py

import streamlit as st
import json

GLYPH_PATH = "glyphs/index.json"

def load_glyphs():
    try:
        with open(GLYPH_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

glyphs = load_glyphs()

st.title("🔮 Glyph Explorer")

for glyph in glyphs:
    with st.expander(f"{glyph['symbol']} {glyph['name']}"):
        st.markdown(f"**Meaning:** {glyph['meaning']}")
        if glyph.get("void_mode"):
            st.markdown("⬛ *Void Mode Enabled*")
            st.code("\n".join(glyph.get("background_pattern", [])))
        if glyph.get("activation_code"):
            if st.button(f"Activate {glyph['symbol']}"):
                st.write("⚙️ Executing code:")
                st.code(glyph["activation_code"])
                exec(glyph["activation_code"])
