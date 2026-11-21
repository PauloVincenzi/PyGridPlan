import math
from itertools import combinations

import pytest

from pygridplan.generators.cpsat import DEFAULT_TIME_LIMIT as TIME, GenerationError, generate_alternatives
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import Site
from pygridplan.model.request import Request, RoomRequest, load_request
from pygridplan.scoring.diversity import plan_distance
from pygridplan.validation.access import check_access
from pygridplan.validation.checks import validate_geometry
from test_request import BASIC_PROGRAM

pytestmark = pytest.mark.slow
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
    width = request.site.width_mm
    for a, b in combinations(alts, 2):
        assert plan_distance(a.plan, b.plan) >= min_diff / pairs
        # o lote é simétrico na largura: uma alternativa também não pode ser o espelho de outra
        flipped = a.plan.model_copy(update={"rooms": tuple(
            r.model_copy(update={"rect": r.rect.model_copy(update={"x": width - r.rect.x2})}) for r in a.plan.rooms)})
        assert plan_distance(flipped, b.plan) >= min_diff / pairs


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


def test_all_attempts_rejected_raises(monkeypatch):
    import pygridplan.generators.cpsat as g

    monkeypatch.setattr(g, "check_access", lambda plan, catalog: ["rejeitada"])  # força rejeição
    with pytest.raises(GenerationError):
        g.generate_alternatives(_req("sala", "cozinha"), load_catalog(), k=1, time_limit=TIME, max_attempts=2)


def test_no_room_inflates_past_double_its_target():
    from pygridplan.model.walls import useful_area_mm2
    from pygridplan.scoring.score import room_target_m2

    request, catalog = load_request(BASIC_PROGRAM), load_catalog()
    targets = {r.id: room_target_m2(r, catalog) for r in request.rooms}
    for alt in generate_alternatives(request, catalog, k=4, time_limit=TIME):
        for room in alt.plan.rooms:
            if targets[room.id]:
                assert useful_area_mm2(room, alt.plan) / 1e6 <= 2 * targets[room.id], room.id


def test_no_room_shrinks_far_below_its_target():
    # na 3ª alternativa deste pedido a cozinha saía com 3,6 m² para um alvo de 10 m² (calibração do M1.1)
    from pygridplan.model.walls import useful_area_mm2
    from pygridplan.scoring.score import room_target_m2

    request, catalog = load_request(BASIC_PROGRAM.parent / "three-bedroom.json"), load_catalog()
    targets = {r.id: room_target_m2(r, catalog) for r in request.rooms}
    for alt in generate_alternatives(request, catalog, k=3, time_limit=TIME):
        for room in alt.plan.rooms:
            if targets[room.id]:
                assert useful_area_mm2(room, alt.plan) / 1e6 >= 0.7 * targets[room.id], room.id
