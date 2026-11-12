import math
from itertools import combinations

import pytest

from pygridplan.generators.cpsat import GenerationError, generate_alternatives
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import Site
from pygridplan.model.request import Request, RoomRequest, load_request
from pygridplan.scoring.diversity import plan_distance
from pygridplan.validation.access import check_access
from pygridplan.validation.checks import validate_geometry
from test_request import BASIC_PROGRAM

TIME = 0.5
LOT = Site(width_mm=10000, depth_mm=25000)


def _req(*types):
    return Request(site=LOT, rooms=tuple(RoomRequest(id=f"{t}{i}", type=t) for i, t in enumerate(types)))


def test_four_valid_diverse_alternatives():
    request, catalog = load_request(BASIC_PROGRAM), load_catalog()
    alts = generate_alternatives(request, catalog, k=4, time_limit=TIME)
    assert len(alts) == 4
    for alt in alts:
        assert validate_geometry(alt.plan) == []
        assert check_access(alt.plan, catalog) == []
    pairs = math.comb(len(request.rooms), 2)
    min_diff = max(1, math.ceil(0.15 * pairs))
    for a, b in combinations(alts, 2):
        assert plan_distance(a.plan, b.plan) >= min_diff / pairs


def test_program_too_big_raises():
    site = Site(width_mm=5000, depth_mm=5000)
    rooms = (RoomRequest(id="s", type="sala"), RoomRequest(id="q1", type="quarto"), RoomRequest(id="q2", type="quarto"))
    with pytest.raises(GenerationError, match="caber"):
        generate_alternatives(Request(site=site, rooms=rooms), load_catalog(), time_limit=TIME)


def test_no_traversable_room_raises():
    with pytest.raises(GenerationError, match="atravessável"):
        generate_alternatives(_req("quarto", "quarto"), load_catalog(), time_limit=TIME)


def test_small_program_returns_fewer():
    # sala + cozinha só têm 4 arranjos realmente diferentes (esquerda, direita, frente, atrás)
    alts = generate_alternatives(_req("sala", "cozinha"), load_catalog(), k=6, time_limit=TIME)
    assert 1 <= len(alts) < 6


def test_same_seed_same_plans():
    req = _req("sala", "cozinha", "quarto")
    first = generate_alternatives(req, load_catalog(), k=2, time_limit=TIME)
    second = generate_alternatives(req, load_catalog(), k=2, time_limit=TIME)
    assert [a.plan for a in first] == [a.plan for a in second]
