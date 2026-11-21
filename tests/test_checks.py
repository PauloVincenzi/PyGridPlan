from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import Plan, Rect, Room, Setbacks, Site
from pygridplan.validation.checks import check_recommendations, validate_geometry

LOT = Site(width_mm=10000, depth_mm=10000)


def _codes(issues):
    return [i.code for i in issues]


def test_basic_house_is_valid_and_clean(basic_house):
    assert validate_geometry(basic_house) == []
    assert check_recommendations(basic_house, load_catalog()) == []


def test_overlap_detected():
    plan = Plan(site=LOT, rooms=(
        Room(id="a", type="sala", rect=Rect(x=1000, y=1000, w=3000, h=3000)),
        Room(id="b", type="sala", rect=Rect(x=2000, y=2000, w=3000, h=3000)),
    ))
    issues = validate_geometry(plan)
    assert _codes(issues) == ["overlap"]
    assert issues[0].room_ids == ("a", "b")


def test_room_on_lot_edge_is_outside():
    plan = Plan(site=LOT, rooms=(Room(id="a", type="sala", rect=Rect(x=0, y=1000, w=3000, h=3000)),))
    assert _codes(validate_geometry(plan)) == ["outside_lot"]


def test_setback_warning_unless_attached():
    room = Room(id="a", type="sala", rect=Rect(x=75, y=5000, w=4000, h=4000))
    site = Site(width_mm=10000, depth_mm=10000, setbacks=Setbacks(left=1500))
    plan = Plan(site=site, rooms=(room,))
    assert _codes(check_recommendations(plan, load_catalog())) == ["setback"]
    attached = plan.model_copy(update={"site": site.model_copy(update={"attached_sides": frozenset({"left"})})})
    assert check_recommendations(attached, load_catalog()) == []


def test_min_width_warning():
    plan = Plan(site=LOT, rooms=(Room(id="q", type="quarto", rect=Rect(x=1000, y=1000, w=2300, h=5000)),))
    issues = check_recommendations(plan, load_catalog())
    assert _codes(issues) == ["min_width"]
    assert issues[0].recommended == 2400


def test_unknown_type_has_no_minimum_warnings():
    plan = Plan(site=LOT, rooms=(Room(id="x", type="quadra_de_areia", rect=Rect(x=1000, y=1000, w=500, h=500)),))
    assert check_recommendations(plan, load_catalog()) == []


def test_wall_overlap_between_close_rooms():
    plan = Plan(site=LOT, rooms=(
        Room(id="a", type="sala", rect=Rect(x=1000, y=1000, w=4000, h=4000)),
        Room(id="b", type="sala", rect=Rect(x=5100, y=1000, w=4000, h=4000)),  # vão de 100 mm < 150
    ))
    issues = validate_geometry(plan)
    assert _codes(issues) == ["wall_overlap"]
    assert issues[0].room_ids == ("a", "b")


def test_room_smaller_than_its_walls():
    plan = Plan(site=LOT, rooms=(Room(id="x", type="quadra_de_areia", rect=Rect(x=1000, y=1000, w=50, h=50)),))
    assert _codes(validate_geometry(plan)) == ["too_small"]


def _ring(center_type=None):
    """Anel 3x3 de cômodos de 1 000 mm, com ou sem cômodo no centro."""
    rooms = [Room(id=f"r{cx}{cy}", type="sala", rect=Rect(x=1000 + cx * 1000, y=1000 + cy * 1000, w=1000, h=1000))
             for cx in range(3) for cy in range(3) if (cx, cy) != (1, 1)]
    if center_type:
        rooms.append(Room(id="centro", type=center_type, rect=Rect(x=2000, y=2000, w=1000, h=1000)))
    return Plan(site=LOT, rooms=tuple(rooms))


def test_ring_with_hole_is_enclosed_void():
    from pygridplan.validation.checks import enclosed_void_area_mm2

    plan = _ring()
    assert enclosed_void_area_mm2(plan) == 1_000_000
    assert "enclosed_void" in _codes(validate_geometry(plan))


def test_notch_open_to_border_is_not_a_void():
    from pygridplan.validation.checks import enclosed_void_area_mm2

    rooms = (Room(id="a", type="sala", rect=Rect(x=1000, y=1000, w=1000, h=3000)),
             Room(id="b", type="sala", rect=Rect(x=2000, y=1000, w=1000, h=1000)),
             Room(id="c", type="sala", rect=Rect(x=3000, y=1000, w=1000, h=3000)))  # U aberto para trás
    assert enclosed_void_area_mm2(Plan(site=LOT, rooms=rooms)) == 0


def test_requested_patio_is_not_a_void():
    assert "enclosed_void" not in _codes(validate_geometry(_ring("patio")))


def test_basic_house_has_no_void(basic_house):
    from pygridplan.validation.checks import enclosed_void_area_mm2

    assert enclosed_void_area_mm2(basic_house) == 0


def test_interior_bathroom_gets_a_duct_or_skylight_suggestion_but_closet_does_not():
    from pygridplan.validation.checks import check_ventilation

    site = Site(width_mm=20000, depth_mm=20000)
    rooms = (Room(id="s", type="sala", rect=Rect(x=1000, y=1000, w=9000, h=3000)),
             Room(id="q1", type="quarto", rect=Rect(x=1000, y=4000, w=3000, h=2000)),
             Room(id="b", type="banheiro", rect=Rect(x=4000, y=4000, w=2000, h=2000)),
             Room(id="cl", type="closet", rect=Rect(x=6000, y=4000, w=2000, h=2000)),
             Room(id="q2", type="quarto", rect=Rect(x=8000, y=4000, w=2000, h=2000)),
             Room(id="c", type="cozinha", rect=Rect(x=1000, y=6000, w=9000, h=3000)))
    issues = check_ventilation(Plan(site=site, rooms=rooms), load_catalog())
    assert [i.room_ids for i in issues] == [("b",)]
    assert "claraboia" in issues[0].message
