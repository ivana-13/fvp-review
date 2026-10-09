from fvp.verify import parse_verify, verify_prompt


def test_prompt_mentions_both_roles_and_captions():
    p = verify_prompt("A dog bites my hand.", "A hand bites the dog.", [("agent", "the one who is biting (the agent)"), ("item", "the item being bitten")])
    assert "A: A dog bites my hand." in p and "B: A hand bites the dog." in p
    assert '"agent"' in p and '"item"' in p and "the item being bitten" in p


def test_parse_keyed_json():
    raw = '```json\n{"agent": {"name": "dog", "bbox_2d": [10, 20, 300, 400]}, "item": {"name": "hand", "bbox_2d": [350, 100, 600, 300]}, "answer": "A"}\n```'
    out = parse_verify(raw, ["agent", "item"])
    assert out["answer"] == "A"
    assert out["boxes"]["agent"] == [10, 20, 300, 400]
    assert out["boxes"]["item"] == [350, 100, 600, 300]


def test_parse_positional_fallback_and_plain_answer():
    raw = "Boxes: [[5, 5, 50, 50]] and [[60, 60, 90, 90]]. Answer: B"
    out = parse_verify(raw, ["agent", "victim"])
    assert out["answer"] == "B"
    assert out["boxes"]["agent"] == [5, 5, 50, 50] and out["boxes"]["victim"] == [60, 60, 90, 90]


def test_parse_missing_pieces():
    out = parse_verify("I cannot tell.", ["agent", "item"])
    assert out["answer"] is None and out["boxes"] == {"agent": None, "item": None}
    out = parse_verify('{"agent": {"bbox_2d": [1, 2, 3, 4]}, "answer": "B"}', ["agent", "item"])
    assert out["answer"] == "B" and out["boxes"]["agent"] == [1, 2, 3, 4] and out["boxes"]["item"] is None
