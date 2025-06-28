def build_prompt(motif: str, mode: str = "default") -> str:
    if mode == "default":
        return f"Generate a new insight about the symbolic field: {motif}"
    elif mode == "friction":
        return f"Explore tension or contradiction in the motif: {motif}"
    elif mode == "goal":
        return f"What would it mean to achieve coherence in: {motif}?"
    else:
        return f"[Unknown mode] {motif}"
