from pathlib import Path

import pytest

from pygridplan.generators.cpsat import GenerationError, generate_alternatives
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import Site
from pygridplan.model.request import Request, RoomRequest, load_request
from pygridplan.model.walls import exterior_sides
from test_request import BASIC_PROGRAM

SMALL_LOT = Path(__file__).parent / "fixtures" / "requests" / "small-lot.json"
TIME = 0.5


@pytest.fixture(scope="module")
def small_lot_alternative():
    return generate_alternatives(load_request(SMALL_LOT), load_catalog(), k=1, time_limit=TIME)[0]


def _codes(alt):
    return [w.code for w in alt.warnings]


def test_exterior_sides_of_basic_house(basic_house):
    sala = next(r for r in basic_house.rooms if r.id == "sala")
    assert exterior_sides(sala, basic_house) == {"left", "front"}


def test_small_lot_attaches_automatically(small_lot_alternative):
    alt = small_lot_alternative
    assert "attached" in _codes(alt)
    assert "left" in alt.plan.site.attached_sides
    assert min(r.rect.x for r in alt.plan.rooms) == 100


def test_no_window_on_attached_side(small_lot_alternative):
    alt = small_lot_alternative
    flagged = {w.room_ids[0] for w in alt.warnings if w.code == "no_window"}
    assert {r.id for r in alt.plan.rooms if r.rect.x == 100} <= flagged


def test_explicit_attached_sides_are_kept():
    request = load_request(BASIC_PROGRAM)
    request = request.model_copy(update={"site": request.site.model_copy(update={"attached_sides": frozenset({"right"})})})
    alt = generate_alternatives(request, load_catalog(), k=1, time_limit=TIME)[0]
    assert "attached" not in _codes(alt)
    assert alt.plan.site.attached_sides == frozenset({"right"})


def test_too_small_even_attached_raises():
    from pygridplan.model.plan import Setbacks

    # mesmo encostando nas laterais e no fundo, sobram 2,8 x 3,9 m: sala e quarto não cabem
    site = Site(width_mm=3000, depth_mm=8000, setbacks=Setbacks(front=4000, back=2000, left=1500, right=1500))
    rooms = (RoomRequest(id="s", type="sala"), RoomRequest(id="q", type="quarto"))
    with pytest.raises(GenerationError):
        generate_alternatives(Request(site=site, rooms=rooms), load_catalog(), time_limit=TIME)
