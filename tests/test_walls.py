from pygridplan.model.plan import Plan, Rect, Room, Site
from pygridplan.model.walls import Wall, derive_walls, useful_area_mm2, useful_dims_mm


def _plan(*rects: Rect) -> Plan:
    rooms = tuple(Room(id=f"r{i}", type="sala", rect=r) for i, r in enumerate(rects))
    return Plan(site=Site(width_mm=20000, depth_mm=20000), rooms=rooms)


def _room(plan: Plan, room_id: str) -> Room:
    return next(r for r in plan.rooms if r.id == room_id)


def test_basic_house_wall_counts(basic_house):
    walls = derive_walls(basic_house)
    assert sum(w.kind == "int" for w in walls) == 11
    assert sum(w.kind == "ext" for w in walls) == 11


def test_shared_wall_between_sala_and_cozinha(basic_house):
    expected = Wall(
        x1=5600, y1=4100, x2=5600, y2=8100, thickness_mm=100, kind="int", room_ids=("sala", "cozinha")
    )
    assert expected in derive_walls(basic_house)


def test_corner_touch_is_not_a_wall():
    walls = derive_walls(_plan(Rect(x=0, y=0, w=1000, h=1000), Rect(x=1000, y=1000, w=1000, h=1000)))
    assert sum(w.kind == "int" for w in walls) == 0
    assert sum(w.kind == "ext" for w in walls) == 8


def test_useful_area_sala(basic_house):
    sala = _room(basic_house, "sala")
    assert useful_dims_mm(sala, basic_house) == (3875, 3875)
    assert useful_area_mm2(sala, basic_house) == 15_015_625


def test_useful_dims_banheiro_all_interior(basic_house):
    assert useful_dims_mm(_room(basic_house, "banheiro"), basic_house) == (1500, 2400)


def test_partially_shared_side_uses_external_thickness():
    plan = _plan(Rect(x=0, y=0, w=2000, h=2000), Rect(x=2000, y=0, w=2000, h=1000))
    width, _ = useful_dims_mm(_room(plan, "r0"), plan)
    assert width == 2000 - 75 - 75
