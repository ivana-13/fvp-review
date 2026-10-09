import pytest

from fvp.models.molmo import parse_points
from fvp.models.paligemma import parse_locs


def test_molmo_single_and_multi_points():
    raw = '<point x="52.3" y="61.0" alt="the dog">the dog</point>'
    (pt,) = parse_points(raw, (200, 100))
    assert pt == pytest.approx([104.6, 61.0])
    pts = parse_points('<points x1="10.0" y1="20.0" x2="30.0" y2="40.0" alt="hands">hands</points>', (100, 100))
    assert len(pts) == 2
    assert pts[0] == pytest.approx([10.0, 20.0])
    assert pts[1] == pytest.approx([30.0, 40.0])
    assert parse_points("I cannot find it.", (100, 100)) == []


def test_paligemma_loc_tokens_are_y_then_x():
    raw = "<loc0256><loc0512><loc0768><loc1023> dog"
    (box,) = parse_locs(raw, (1024, 1024))
    assert box == pytest.approx([512.0, 256.0, 1023.0, 768.0])
    assert parse_locs("dog", (10, 10)) == []
