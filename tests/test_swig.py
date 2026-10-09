from fvp.swig import SwigImage, SwigSpace, match_word_to_role


def _space():
    return SwigSpace(
        nouns={
            "n_man": {"gloss": ["man", "adult male"]},
            "n_torso": {"gloss": ["torso", "trunk"]},
            "n_gym": {"gloss": ["gym", "gymnasium"]},
            "n_women": {"gloss": ["woman", "adult female"]},
        },
        verbs={
            "exercising": {
                "roles": {
                    "agent": {"def": "The entity doing the exercise action"},
                    "bodypart": {"def": "The body part being exercised"},
                    "place": {"def": "The location"},
                }
            }
        },
    )


def _img():
    return SwigImage(
        image_file="exercising_255.jpg",
        split="test",
        verb="exercising",
        width=512,
        height=384,
        bb={"agent": [10, 10, 100, 200], "bodypart": [30, 60, 80, 120], "place": [-1, -1, -1, -1]},
        frames=[
            {"agent": "n_man", "bodypart": "n_torso", "place": "n_gym"},
            {"agent": "n_man", "bodypart": "n_torso", "place": "n_gym"},
            {"agent": "n_women", "bodypart": "n_torso", "place": ""},
        ],
    )


def test_match_exact_and_plural():
    assert match_word_to_role("man", _img(), _space()) == "agent"
    assert match_word_to_role("torso", _img(), _space()) == "bodypart"
    assert match_word_to_role("torsos", _img(), _space()) == "bodypart"


def test_match_uses_any_annotator_noun():
    assert match_word_to_role("woman", _img(), _space()) == "agent"


def test_match_prefers_non_place_and_returns_none_when_absent():
    assert match_word_to_role("gym", _img(), _space()) == "place"
    assert match_word_to_role("dog", _img(), _space()) is None
