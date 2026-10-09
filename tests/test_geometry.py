from fvp.geometry import (
    box_center,
    iou,
    is_valid_box,
    normalized_1000_to_abs,
    point_in_box,
    scale_box,
)


def test_invalid_boxes():
    assert not is_valid_box([-1, -1, -1, -1])
    assert not is_valid_box([10, 10, 5, 20])
    assert is_valid_box([0, 0, 1, 1])


def test_iou_identical_and_disjoint():
    assert iou([0, 0, 10, 10], [0, 0, 10, 10]) == 1.0
    assert iou([0, 0, 10, 10], [20, 20, 30, 30]) == 0.0


def test_iou_partial():
    # 10x10 and 10x10 overlapping in a 5x10 strip: inter 50, union 150
    assert abs(iou([0, 0, 10, 10], [5, 0, 15, 10]) - 1 / 3) < 1e-9


def test_iou_with_ungrounded_role_is_zero():
    assert iou([0, 0, 10, 10], [-1, -1, -1, -1]) == 0.0


def test_point_in_box_and_center():
    box = [10, 20, 30, 40]
    assert box_center(box) == (20, 30)
    assert point_in_box((20, 30), box)
    assert point_in_box((10, 20), box)  # inclusive edges
    assert not point_in_box((31, 30), box)
    assert not point_in_box((20, 30), [-1, -1, -1, -1])


def test_scale_and_normalized_conversion():
    assert scale_box([0, 0, 100, 50], (200, 100), (400, 200)) == [0, 0, 200, 100]
    assert normalized_1000_to_abs([500, 500, 1000, 1000], (512, 384)) == [256, 192, 512, 384]
