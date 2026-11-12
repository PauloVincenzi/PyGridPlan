from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import Plan, Rect, Room, Site
from pygridplan.validation.access import MIN_PASSAGE_MM, check_access, passages

SITE = Site(width_mm=20000, depth_mm=20000)
SALA = Room(id="sala", type="sala", rect=Rect(x=1000, y=1000, w=4000, h=4000))


def _check(*rooms):
    return check_access(Plan(site=SITE, rooms=rooms), load_catalog())


def _codes(issues):
    return sorted((i.code, i.room_ids) for i in issues)


def test_basic_house_access_ok(basic_house):
    assert check_access(basic_house, load_catalog()) == []
    assert passages(basic_house)[("sala", "cozinha")] == 4000


def test_room_only_reachable_through_bedroom_is_unreachable():
    a = Room(id="qa", type="quarto", rect=Rect(x=5000, y=1000, w=3000, h=4000))
    b = Room(id="qb", type="quarto", rect=Rect(x=8000, y=1000, w=3000, h=4000))
    assert _codes(_check(SALA, a, b)) == [("unreachable", ("qb",))]


def test_suite_bathroom_is_reachable():
    q = Room(id="q", type="quarto", rect=Rect(x=5000, y=1000, w=3000, h=4000))
    wc = Room(id="wc", type="banheiro", rect=Rect(x=8000, y=1000, w=2000, h=2000))
    assert _check(SALA, q, wc) == []


def test_no_traversable_room_on_front():
    q = Room(id="q", type="quarto", rect=Rect(x=1000, y=1000, w=3000, h=4000))
    assert ("no_entrance", ()) in _codes(_check(q))


def test_short_shared_wall_is_not_a_passage():
    q = Room(id="q", type="quarto", rect=Rect(x=5000, y=4200, w=3000, h=3000))  # 800 mm em comum
    assert MIN_PASSAGE_MM == 900
    assert _codes(_check(SALA, q)) == [("unreachable", ("q",))]
