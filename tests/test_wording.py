import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_wording import phrase_b, sample_items  # noqa: E402


def test_phrase_b_names_the_role():
    assert phrase_b("agent", "The entity doing the bite action", "biting") == "the agent of the biting action"
    assert phrase_b("item", "The item being bitten", "biting") == "the item of the biting action"
    assert phrase_b("agentpart", "...", "exercising") == "the body part of the agent of the exercising action"


def test_sample_is_deterministic_and_keeps_file_order():
    items = [{"valse_id": f"id{i}"} for i in range(50)]
    a = sample_items(items, 10, 0)
    b = sample_items(items, 10, 0)
    assert a == b and len(a) == 10
    assert [x["valse_id"] for x in a] == sorted([x["valse_id"] for x in a], key=lambda s: int(s[2:]))
    assert sample_items(items, 10, 1) != a
