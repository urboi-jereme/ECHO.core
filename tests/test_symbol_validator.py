from symbol_validator import validate_triad


def test_validate_triad_high_score():
    score = validate_triad(["🔥", "🪞", "🗿"])
    assert 0.5 < score <= 1.0


def test_validate_triad_invalid_length():
    assert validate_triad(["🔥", "🪞"]) == 0.0
