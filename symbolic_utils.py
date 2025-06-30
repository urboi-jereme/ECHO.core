import re import random

Symbol registry for symbolic decomposition

BASE_SYMBOLS = [ "recursion", "error", "attention", "memory", "symbol", "paradox", "coherence", "perturbation", "emergence", "loop", "collapse", "mirror" ]

Motif heuristics

MOTIF_MAP = { "recursion": "recursive balance", "loop": "recursive balance", "paradox": "tension", "error": "disruption", "attention": "observer effect", "mirror": "self-reference", "collapse": "failure mode", "coherence": "stability", "perturbation": "novelty", "emergence": "complexity" }

-------------------------------

Symbolic Decomposition

-------------------------------

def decompose(statement): tokens = re.findall(r"\b\w+\b", statement.lower()) found = [symbol for symbol in BASE_SYMBOLS if symbol in tokens] return found if found else ["undefined"]

-------------------------------

Motif Identification

-------------------------------

def identify_motif(base_symbols): motif_counts = {} for symbol in base_symbols: motif = MOTIF_MAP.get(symbol, "unclassified") motif_counts[motif] = motif_counts.get(motif, 0) + 1

# Return most common motif, break ties randomly
max_count = max(motif_counts.values())
top_motifs = [k for k, v in motif_counts.items() if v == max_count]
return random.choice(top_motifs)

-------------------------------

Recursive Refinement

-------------------------------

def refine(original, base_symbols, motif): compression_level = 0 refined = original

if "recursion" in base_symbols and "paradox" in base_symbols:
    refined = f"{motif.capitalize()} encodes conflict that sustains itself."
    compression_level = 3
elif len(base_symbols) >= 2:
    refined = f"{base_symbols[0].capitalize()} mutates through {base_symbols[1]}."
    compression_level = 2
elif len(base_symbols) == 1:
    refined = f"{base_symbols[0].capitalize()} contains its own negation."
    compression_level = 1
else:
    refined = "Pattern not yet symbolized."
    compression_level = 0

return refined, compression_level

