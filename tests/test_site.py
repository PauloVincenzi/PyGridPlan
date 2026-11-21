from pathlib import Path

import pytest

from pygridplan.generators.cpsat import DEFAULT_TIME_LIMIT as TIME, GenerationError, generate_alternatives
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import Site
from pygridplan.model.request import Request, RoomRequest, load_request
from pygridplan.model.walls import exterior_sides
from test_request import BASIC_PROGRAM

SMALL_LOT = Path(__file__).parent / "fixtures" / "requests" / "small-lot.json"


@pytest.fixture(scope="module")
def small_lot_alternative():
    return generate_alternatives(load_request(SMALL_LOT), load_catalog(), k=1, time_limit=TIME)[0]


def _codes(alt):
    return [w.code for w in alt.warnings]


def test_exterior_sides_of_basic_house(basic_house):
    sala = next(r for r in basic_house.rooms if r.id == "sala")
    assert exterior_sides(sala, basic_house) == {"left", "front"}


@pytest.mark.slow
def test_small_lot_attaches_automatically(small_lot_alternative):
    alt = small_lot_alternative
    assert "attached" in _codes(alt)
    assert "left" in alt.plan.site.attached_sides
    assert min(r.rect.x for r in alt.plan.rooms) == 100


@pytest.mark.slow
def test_no_window_on_attached_side(small_lot_alternative):
    alt = small_lot_alternative
    flagged = {w.room_ids[0] for w in alt.warnings if w.code == "no_window"}
    assert {r.id for r in alt.plan.rooms if r.rect.x == 100} <= flagged


@pytest.mark.slow
def test_explicit_attached_sides_are_kept():
    request = load_request(BASIC_PROGRAM)
    request = request.model_copy(update={"site": request.site.model_copy(update={"attached_sides": frozenset({"right"})})})
    alt = generate_alternatives(request, load_catalog(), k=1, time_limit=TIME)[0]
    assert "attached" not in _codes(alt)
    assert alt.plan.site.attached_sides == frozenset({"right"})


@pytest.mark.slow
def test_too_small_even_attached_raises():
    from pygridplan.model.plan import Setbacks

    # mesmo encostando nas laterais e no fundo, sobram 2,8 x 3,9 m: sala e quarto não cabem
    site = Site(width_mm=3000, depth_mm=8000, setbacks=Setbacks(front=4000, back=2000, left=1500, right=1500))
    rooms = (RoomRequest(id="s", type="sala"), RoomRequest(id="q", type="quarto"))
    with pytest.raises(GenerationError):
        generate_alternatives(Request(site=site, rooms=rooms), load_catalog(), time_limit=TIME)


def test_room_categories():
    c = load_catalog()
    assert (c.get("sala").category, c.get("banheiro").category, c.get("varanda").category) == ("dry", "wet", "built")


def test_green_area_and_permeability_warning(basic_house):
    from pygridplan.model.plan import Plan, Rect, Room
    from pygridplan.model.site_defaults import load_site_defaults
    from pygridplan.validation.site import check_site, green_area_mm2

    defaults = load_site_defaults()
    assert "permeability" not in [i.code for i in check_site(basic_house, defaults)]
    assert green_area_mm2(basic_house, defaults) > 0.5 * 10000 * 25000
    crowded = Plan(site=Site(width_mm=10000, depth_mm=10000),
                   rooms=(Room(id="s", type="sala", rect=Rect(x=300, y=300, w=9400, h=9400)),))
    assert "permeability" in [i.code for i in check_site(crowded, defaults)]


def test_timeout_does_not_trigger_auto_attach():
    # sem tempo para achar solução não é "não coube": não pode encostar na divisa
    with pytest.raises(GenerationError, match="esgotou"):
        generate_alternatives(load_request(BASIC_PROGRAM), load_catalog(), time_limit=0.001)


def test_front_side_never_flagged_no_window():
    from pygridplan.model.plan import Plan, Rect, Room, Setbacks
    from pygridplan.model.site_defaults import load_site_defaults
    from pygridplan.validation.site import check_site

    site = Site(width_mm=10000, depth_mm=10000, setbacks=Setbacks(front=0))
    plan = Plan(site=site, rooms=(Room(id="s", type="sala", rect=Rect(x=3000, y=100, w=4000, h=4000)),))
    assert not [i for i in check_site(plan, load_site_defaults()) if "frontal" in i.message]


@pytest.mark.slow
def test_both_sides_attached_is_centered():
    from pygridplan.generators.cpsat import solve_layout

    request = load_request(BASIC_PROGRAM)
    site = request.site.model_copy(update={"attached_sides": frozenset({"left", "right"})})
    plan = solve_layout(request.model_copy(update={"site": site}), load_catalog(), time_limit=TIME)
    left = min(r.rect.x for r in plan.rooms) - 100
    right = 9900 - max(r.rect.x2 for r in plan.rooms)
    assert abs(left - right) <= 100


@pytest.mark.slow
def test_every_alternative_has_a_bathroom_on_the_circulation():
    # o único banheiro da casa não pode ficar acessível só por dentro de um quarto (design 21.2)
    from pygridplan.validation.access import MIN_PASSAGE_MM, passages

    for alt in generate_alternatives(load_request(SMALL_LOT), load_catalog(), k=4, time_limit=TIME):
        touching = {frozenset(pair) for pair, length in passages(alt.plan).items() if length >= MIN_PASSAGE_MM}
        assert frozenset(("banheiro", "circulacao")) in touching
