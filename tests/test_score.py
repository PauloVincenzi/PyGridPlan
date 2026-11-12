import pytest

from pygridplan.model.catalog import load_catalog
from pygridplan.model.request import Relation, Request, RoomRequest
from pygridplan.model.walls import useful_area_mm2
from pygridplan.scoring.score import WEIGHTS, room_target_m2, score_plan


def _request_for(plan, relations=(), north=None):
    """Pedido com os mesmos IDs e tipos da planta."""
    rooms = tuple(RoomRequest(id=r.id, type=r.type) for r in plan.rooms)
    site = plan.site.model_copy(update={"north": north})
    return Request(site=site, rooms=rooms, relations=relations)


def _criteria(score):
    return {c.name: c for c in score.criteria}


def test_basic_house_compactness_is_one(basic_house):
    s = score_plan(basic_house, _request_for(basic_house), load_catalog())
    assert _criteria(s)["compactness"].value == pytest.approx(1.0)


def test_basic_house_circulation_value(basic_house):
    s = score_plan(basic_house, _request_for(basic_house), load_catalog())
    total = sum(useful_area_mm2(r, basic_house) for r in basic_house.rooms)
    circ = next(r for r in basic_house.rooms if r.id == "circulacao")
    expected = 1 - useful_area_mm2(circ, basic_house) / total
    assert _criteria(s)["circulation"].value == pytest.approx(expected)


def test_near_relation_satisfied(basic_house):
    req = _request_for(basic_house, (Relation(a="sala", b="cozinha", kind="near", intensity=3),))
    assert _criteria(score_plan(basic_house, req, load_catalog()))["relations"].value == pytest.approx(1.0)


def test_solar_inactive_without_north(basic_house):
    s = score_plan(basic_house, _request_for(basic_house), load_catalog())
    assert "solar" not in _criteria(s)
    s_north = score_plan(basic_house, _request_for(basic_house, north="back"), load_catalog())
    assert 0.0 <= _criteria(s_north)["solar"].value <= 1.0


def test_total_is_weighted_mean_of_active(basic_house):
    s = score_plan(basic_house, _request_for(basic_house, north="back"), load_catalog())
    expected = sum(c.value * c.weight for c in s.criteria) / sum(c.weight for c in s.criteria)
    assert s.total == pytest.approx(expected)
    assert all(c.weight == WEIGHTS[c.name] for c in s.criteria)


def test_room_target_prefers_explicit_then_comfort_then_minimum():
    c = load_catalog()
    assert room_target_m2(RoomRequest(id="a", type="quarto", target_area_m2=13), c) == 13
    assert room_target_m2(RoomRequest(id="a", type="quarto"), c) == 10.0  # comfort_area_m2[0]
    assert room_target_m2(RoomRequest(id="a", type="garagem"), c) == pytest.approx(12.5 * 1.25)
    assert room_target_m2(RoomRequest(id="a", type="circulacao"), c) is None
