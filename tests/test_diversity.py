import pytest

from pygridplan.model.plan import Plan, Rect, Room, Site
from pygridplan.scoring.diversity import plan_distance, relative_pattern

SITE = Site(width_mm=20000, depth_mm=20000)


def _plan(*rects):
    return Plan(site=SITE, rooms=tuple(Room(id=f"r{i}", type="sala", rect=r) for i, r in enumerate(rects)))


def test_pattern_of_two_rooms():
    p = _plan(Rect(x=0, y=0, w=1000, h=1000), Rect(x=1000, y=0, w=1000, h=1000))
    assert relative_pattern(p) == {("r0", "r1"): (True, False, False, False)}


def test_distance_zero_for_same_plan(basic_house):
    assert plan_distance(basic_house, basic_house) == 0.0


def test_mirrored_plan_differs(basic_house):
    w = basic_house.site.width_mm
    mirrored = basic_house.model_copy(update={"rooms": tuple(
        r.model_copy(update={"rect": r.rect.model_copy(update={"x": w - r.rect.x2})}) for r in basic_house.rooms
    )})
    assert plan_distance(basic_house, mirrored) > 0


def test_distance_requires_same_rooms(basic_house):
    with pytest.raises(ValueError):
        plan_distance(basic_house, _plan(Rect(x=0, y=0, w=1000, h=1000)))


def test_diagonal_flip_is_not_a_real_difference():
    # r1 continua à direita de r0; só passou a estar também atrás: mesmo arranjo
    a = _plan(Rect(x=0, y=0, w=1000, h=1000), Rect(x=2000, y=0, w=1000, h=1000))
    b = _plan(Rect(x=0, y=0, w=1000, h=1000), Rect(x=2000, y=3000, w=1000, h=1000))
    assert plan_distance(a, b) == 0.0


def test_left_to_right_is_a_real_difference():
    a = _plan(Rect(x=0, y=0, w=1000, h=1000), Rect(x=2000, y=0, w=1000, h=1000))
    b = _plan(Rect(x=2000, y=0, w=1000, h=1000), Rect(x=0, y=0, w=1000, h=1000))
    assert plan_distance(a, b) == 1.0
