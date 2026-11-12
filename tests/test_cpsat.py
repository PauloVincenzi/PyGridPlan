import pytest

from pygridplan.generators.cpsat import solve_layout
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import Site
from pygridplan.model.request import Request, RoomRequest, load_request
from pygridplan.scoring.diversity import plan_distance, relative_pattern
from pygridplan.validation.checks import check_recommendations, validate_geometry
from test_request import BASIC_PROGRAM

TIME = 0.5


@pytest.fixture(scope="module")
def solved():
    request, catalog = load_request(BASIC_PROGRAM), load_catalog()
    return request, catalog, solve_layout(request, catalog, time_limit=TIME)


def test_solution_is_valid(solved):
    _, _, plan = solved
    assert plan is not None
    assert validate_geometry(plan) == []


def test_respects_setbacks_and_grid(solved):
    _, catalog, plan = solved
    assert not [i for i in check_recommendations(plan, catalog) if i.code == "setback"]
    for r in plan.rooms:
        assert all(v % 100 == 0 for v in (r.rect.x, r.rect.y, r.rect.w, r.rect.h))


def test_respects_minimums(solved):
    _, catalog, plan = solved
    assert not [i for i in check_recommendations(plan, catalog) if i.code in ("min_width", "min_area")]


def test_forbidden_pattern_is_avoided(solved):
    request, catalog, first = solved
    second = solve_layout(request, catalog, time_limit=TIME, forbidden=[relative_pattern(first)], min_diff=3)
    assert second is not None
    pairs = len(relative_pattern(first))
    assert plan_distance(first, second) >= 3 / pairs


def test_infeasible_returns_none():
    # cada cômodo precisa de >= 2,55 m nos dois sentidos; num lote útil de 4,85 m só cabe um
    site = Site(width_mm=5000, depth_mm=5000)
    rooms = (RoomRequest(id="s", type="sala"), RoomRequest(id="q1", type="quarto"), RoomRequest(id="q2", type="quarto"))
    assert solve_layout(Request(site=site, rooms=rooms), load_catalog(), time_limit=TIME) is None
