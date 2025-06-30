import re import sys

Define symbolic archetypes and keyword mappings

symbolic_archetypes = { "Division": ["cut", "split", "fracture", "break", "lose", "separate", "exile", "loss"], "Integration": ["weave", "stitch", "connect", "rebuild", "repair", "unify", "return"], "Memory": ["recall", "inherit", "remember", "hold", "archive", "carry"], "Naming": ["name", "label", "mark", "assign", "define"], "Emergence": ["open", "birth", "emerge", "start", "begin", "rise"], "Redemption": ["hope", "redeem", "resolve", "transform", "heal", "found"], "Expression": ["voice", "speak", "tell", "say", "declare"], "Descent": ["dive", "descend", "fall", "sink", "lower"] }

Create reverse lookup

word_to_archetype = {word: archetype for archetype, words in symbolic_archetypes.items() for word in words}

def translate_to_symbolic_triads(sentence): words = re.findall(r'\b\w+\b', sentence.lower()) matched = [] seen_archetypes = set()

for word in words:
    archetype = word_to_archetype.get(word)
    if archetype and archetype not in seen_archetypes:
        matched.append((word, archetype))
        seen_archetypes.add(archetype)
    if len(matched) == 3:
        break

return matched

def main(): if len(sys.argv) < 2: print("Usage: python triad_translator.py 'Your sentence here'") return

sentence = sys.argv[1]
triad = translate_to_symbolic_triads(sentence)

if triad:
    print("\nSymbolic Triad:")
    for word, archetype in triad:
        print(f"  {word:<10} → {archetype}")
else:
    print("\nNo symbolic triad could be extracted from the sentence.")

if name == "main": main()

