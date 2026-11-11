import pytest
from pydantic import ValidationError

from pygridplan.model.plan import Plan, Rect, Room, Site, load_plan, save_plan


def test_rect_overlap_rules():
    a = Rect(x=0, y=0, w=1000, h=1000)
    assert a.overlaps_interior(Rect(x=500, y=500, w=1000, h=1000))
    assert not a.overlaps_interior(Rect(x=1000, y=0, w=1000, h=1000))  # aresta
    assert not a.overlaps_interior(Rect(x=1000, y=1000, w=1000, h=1000))  # canto


def test_rect_expanded():
    assert Rect(x=0, y=0, w=10, h=10).expanded(5) == Rect(x=-5, y=-5, w=20, h=20)


def test_rect_rejects_non_positive_size():
    with pytest.raises(ValidationError):
        Rect(x=0, y=0, w=0, h=10)


def test_plan_rejects_duplicate_room_ids():
    r = Rect(x=0, y=0, w=1000, h=1000)
    with pytest.raises(ValidationError):
        Plan(
            site=Site(width_mm=5000, depth_mm=5000),
            rooms=(Room(id="a", type="sala", rect=r), Room(id="a", type="sala", rect=r)),
        )


def test_load_basic_house(basic_house):
    assert len(basic_house.rooms) == 7
    assert basic_house.site.width_mm == 10000


def test_save_load_roundtrip(basic_house, tmp_path):
    path = tmp_path / "p.json"
    save_plan(basic_house, path)
    assert load_plan(path) == basic_house


def test_empty_plan_is_allowed():
    plan = Plan(site=Site(width_mm=5000, depth_mm=5000))
    assert plan.rooms == ()
