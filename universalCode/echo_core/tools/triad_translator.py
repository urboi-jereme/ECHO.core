# triad_translator.py v0.3.1
try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None

def extract_propositional_cores(sentence):
    """
    Very simple heuristic parser that identifies Subject-Predicate structure.
    Future version could use spaCy or NLTK for smarter parsing.
    """
    words = sentence.strip(".").split()
    if not words:
        return []

    # Naive split: assume first word is Subject, rest is Predicate
    subject = words[0]
    predicate = " ".join(words[1:]) if len(words) > 1 else "(none)"

    nested_cores = []

    # Example: Look for known patterns to simulate recursion
    if "you should leave" in sentence:
        nested_cores.append({
            "sentence": "you should leave",
            "subject": "you",
            "predicate": "should leave",
            "compression": "Anchor. Act. Shift.",
            "nested_cores": []
        })
    if "it rains" in sentence:
        nested_cores.append({
            "sentence": "it rains",
            "subject": "it",
            "predicate": "rains",
            "compression": "Anchor. State. Emerge.",
            "nested_cores": []
        })

    return [{
        "sentence": sentence,
        "subject": subject,
        "predicate": predicate,
        "compression": "Anchor. Split. Mean.",
        "nested_cores": nested_cores
    }]

def display_cores_yaml(cores):
    print(yaml.dump(cores, sort_keys=False, allow_unicode=True))

if __name__ == "__main__":
    test_input = "I believe you should leave before it rains."
    cores = extract_propositional_cores(test_input)
    display_cores_yaml(cores)
