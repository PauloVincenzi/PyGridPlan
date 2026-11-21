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


def _bedrooms(offset_mm=0):
    from pygridplan.model.plan import Plan, Rect, Room, Site

    rooms = tuple(Room(id=f"q{i}", type="quarto",
                       rect=Rect(x=1000 + i * 3000, y=1000 + (offset_mm if i == 2 else 0), w=3000, h=4000))
                  for i in range(3))
    return Plan(site=Site(width_mm=20000, depth_mm=20000), rooms=rooms)


def test_alignment_value_on_hand_plan():
    aligned = _bedrooms()
    assert _criteria(score_plan(aligned, _request_for(aligned), load_catalog()))["alignment"].value == pytest.approx(1.0)
    shifted = _bedrooms(offset_mm=500)
    assert _criteria(score_plan(shifted, _request_for(shifted), load_catalog()))["alignment"].value < 1.0


def test_alignment_inactive_without_pairs():
    from pygridplan.model.plan import Plan, Rect, Room, Site

    plan = Plan(site=Site(width_mm=20000, depth_mm=20000),
                rooms=(Room(id="s", type="sala", rect=Rect(x=1000, y=1000, w=4000, h=4000)),))
    assert "alignment" not in _criteria(score_plan(plan, _request_for(plan), load_catalog()))


def test_target_never_below_minimum_width_square():
    # lavanderia: conforto começa em 2,1 m², mas a largura mínima de 1,80 m já exige 3,24 m²
    assert room_target_m2(RoomRequest(id="a", type="lavanderia"), load_catalog()) == pytest.approx(1.8 * 1.8)


def _hall_plan(second_bedroom_on_hall: bool):
    """Sala na frente, corredor atrás dela, quarto a no corredor; quarto b no corredor ou só na sala."""
    from pygridplan.model.plan import Plan, Rect, Room, Site

    b = Rect(x=4000, y=5000, w=3000, h=3000) if second_bedroom_on_hall else Rect(x=7000, y=1000, w=3000, h=3000)
    rooms = (Room(id="sala", type="sala", rect=Rect(x=1000, y=1000, w=6000, h=3000)),
             Room(id="hall", type="circulacao", rect=Rect(x=1000, y=4000, w=6000, h=1000)),
             Room(id="a", type="quarto", rect=Rect(x=1000, y=5000, w=3000, h=3000)),
             Room(id="b", type="quarto", rect=b))
    return Plan(site=Site(width_mm=20000, depth_mm=20000), rooms=rooms)


def test_circulation_rewards_bedrooms_opening_to_the_hall():
    def value(plan):
        economy = 1 - useful_area_mm2(plan.rooms[1], plan) / sum(useful_area_mm2(r, plan) for r in plan.rooms)
        return _criteria(score_plan(plan, _request_for(plan), load_catalog()))["circulation"].value / economy

    assert value(_hall_plan(True)) == pytest.approx(1.0)  # os dois quartos abrem para o corredor
    assert value(_hall_plan(False)) == pytest.approx(0.5)  # o quarto b só abre para a sala


def test_circulation_inactive_without_circulation_room():
    from pygridplan.model.plan import Plan, Rect, Room, Site

    plan = Plan(site=Site(width_mm=20000, depth_mm=20000),
                rooms=(Room(id="s", type="sala", rect=Rect(x=1000, y=1000, w=4000, h=4000)),
                       Room(id="q", type="quarto", rect=Rect(x=5000, y=1000, w=3000, h=4000))))
    assert "circulation" not in _criteria(score_plan(plan, _request_for(plan), load_catalog()))


def _hub_plan(host_type: str):
    """Corredor que só encosta num cômodo do tipo `host_type` (além do quarto); há uma sala longe dele."""
    from pygridplan.model.plan import Plan, Rect, Room, Site

    rooms = (Room(id="host", type=host_type, rect=Rect(x=1000, y=1000, w=6000, h=3000)),
             Room(id="hall", type="circulacao", rect=Rect(x=1000, y=4000, w=6000, h=1000)),
             Room(id="q", type="quarto", rect=Rect(x=1000, y=5000, w=3000, h=3000)),
             Room(id="sala_longe", type="sala", rect=Rect(x=12000, y=1000, w=4000, h=3000)))
    return Plan(site=Site(width_mm=20000, depth_mm=20000), rooms=rooms)


@pytest.mark.parametrize("host,expected", [("sala", 1.0), ("cozinha", 0.5), ("lavanderia", 0.0)])
def test_zoning_credit_depends_on_who_gives_access_to_the_hall(host, expected):
    plan = _hub_plan(host)
    assert _criteria(score_plan(plan, _request_for(plan), load_catalog()))["zoning"].value == pytest.approx(expected)


def test_ventilation_criterion_counts_rooms_with_exterior_wall():
    from pygridplan.model.plan import Plan, Rect, Room, Site

    # banheiro no meio, cercado: sem parede externa; a sala e o quarto têm
    rooms = (Room(id="s", type="sala", rect=Rect(x=1000, y=1000, w=9000, h=3000)),
             Room(id="q1", type="quarto", rect=Rect(x=1000, y=4000, w=3000, h=2000)),
             Room(id="b", type="banheiro", rect=Rect(x=4000, y=4000, w=2000, h=2000)),
             Room(id="q2", type="quarto", rect=Rect(x=6000, y=4000, w=4000, h=2000)),
             Room(id="c", type="cozinha", rect=Rect(x=1000, y=6000, w=9000, h=3000)))
    plan = Plan(site=Site(width_mm=20000, depth_mm=20000), rooms=rooms)
    assert _criteria(score_plan(plan, _request_for(plan), load_catalog()))["ventilation"].value == pytest.approx(4 / 5)


def test_zoning_does_not_apply_without_any_access_room():
    from pygridplan.model.plan import Plan, Rect, Room, Site

    rooms = (Room(id="l", type="lavanderia", rect=Rect(x=1000, y=1000, w=6000, h=3000)),
             Room(id="hall", type="circulacao", rect=Rect(x=1000, y=4000, w=6000, h=1000)))
    plan = Plan(site=Site(width_mm=20000, depth_mm=20000), rooms=rooms)
    assert "zoning" not in _criteria(score_plan(plan, _request_for(plan), load_catalog()))
