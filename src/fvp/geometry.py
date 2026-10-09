"""Box and point geometry for the pointing probe.

Boxes are [x1, y1, x2, y2] in pixel coordinates of the image they refer to.
SWiG uses [-1, -1, -1, -1] for roles that are labelled but not grounded.
"""

from __future__ import annotations

Box = list[float] | tuple[float, float, float, float]
Point = tuple[float, float]


def is_valid_box(box: Box | None) -> bool:
    if box is None or len(box) != 4:
        return False
    x1, y1, x2, y2 = box
    if any(v < 0 for v in box):
        return False
    return x2 > x1 and y2 > y1


def box_area(box: Box) -> float:
    x1, y1, x2, y2 = box
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def iou(a: Box, b: Box) -> float:
    """Intersection over union; 0 when either box is invalid."""
    if not (is_valid_box(a) and is_valid_box(b)):
        return 0.0
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    union = box_area(a) + box_area(b) - inter
    return inter / union if union > 0 else 0.0


def box_center(box: Box) -> Point:
    x1, y1, x2, y2 = box
    return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


def point_in_box(point: Point, box: Box) -> bool:
    if not is_valid_box(box):
        return False
    x, y = point
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]


def scale_box(box: Box, from_wh: tuple[float, float], to_wh: tuple[float, float]) -> list[float]:
    """Rescale a box from one image size to another (e.g. model input size to gold size)."""
    sx = to_wh[0] / from_wh[0]
    sy = to_wh[1] / from_wh[1]
    return [box[0] * sx, box[1] * sy, box[2] * sx, box[3] * sy]


def normalized_1000_to_abs(box: Box, wh: tuple[float, float]) -> list[float]:
    """Convert a box expressed on a 0-1000 grid to absolute pixels of an image of size wh."""
    w, h = wh
    return [box[0] / 1000.0 * w, box[1] / 1000.0 * h, box[2] / 1000.0 * w, box[3] / 1000.0 * h]
