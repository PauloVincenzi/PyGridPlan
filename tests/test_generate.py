import math
from itertools import combinations

import pytest

from pygridplan.generators.cpsat import DEFAULT_BATCHES as BATCHES, GenerationError, generate_alternatives
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
    alts = generate_alternatives(request, catalog, k=4, batches=BATCHES)
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
        generate_alternatives(Request(site=site, rooms=rooms), load_catalog(), batches=BATCHES)


def test_no_traversable_room_raises():
    with pytest.raises(GenerationError, match="atravessável"):
        generate_alternatives(_req("quarto", "quarto"), load_catalog(), batches=BATCHES)


def test_small_program_returns_fewer():
    # sala + cozinha só têm 4 arranjos realmente diferentes (esquerda, direita, frente, atrás)
    alts = generate_alternatives(_req("sala", "cozinha"), load_catalog(), k=6, batches=BATCHES)
    assert 1 <= len(alts) < 6


def test_same_seed_same_plans():
    req = _req("sala", "cozinha", "quarto")
    first = generate_alternatives(req, load_catalog(), k=2, batches=BATCHES)
    second = generate_alternatives(req, load_catalog(), k=2, batches=BATCHES)
    assert [a.plan for a in first] == [a.plan for a in second]


def test_same_request_same_plans_when_the_search_stops_at_its_budget(monkeypatch):
    # a casa grande não prova o ótimo no orçamento: antes da S07, da 2ª alternativa em diante a planta mudava de uma
    # execução para outra (nota de 0,87 a 0,93 na mesma alternativa), porque o LNS e a troca de cláusulas binárias do
    # CP-SAT dependiam do tempo das threads (DEC-0123). As duas gerações rodam ao mesmo tempo, como num servidor
    from concurrent.futures import ThreadPoolExecutor

    from ortools.sat.python import cp_model

    statuses, solve = [], cp_model.CpSolver.solve

    def recording(self, *args, **kwargs):
        status = solve(self, *args, **kwargs)
        statuses.append(status)
        return status

    monkeypatch.setattr(cp_model.CpSolver, "solve", recording)
    request, catalog = load_request(BASIC_PROGRAM.parent / "large-house.json"), load_catalog()
    with ThreadPoolExecutor(2) as pool:
        first, second = pool.map(lambda _: generate_alternatives(request, catalog, k=2), range(2))
    assert cp_model.FEASIBLE in statuses  # a premissa: alguma resolução parou no orçamento, sem provar o ótimo
    assert [a.plan for a in first] == [a.plan for a in second]


def test_all_attempts_rejected_raises(monkeypatch):
    import pygridplan.generators.cpsat as g

    monkeypatch.setattr(g, "check_access", lambda plan, catalog: ["rejeitada"])  # força rejeição
    with pytest.raises(GenerationError):
        g.generate_alternatives(_req("sala", "cozinha"), load_catalog(), k=1, batches=BATCHES, max_attempts=2)


def test_no_room_inflates_past_double_its_target():
    from pygridplan.model.walls import useful_area_mm2
    from pygridplan.scoring.score import room_target_m2

    request, catalog = load_request(BASIC_PROGRAM), load_catalog()
    targets = {r.id: room_target_m2(r, catalog) for r in request.rooms}
    for alt in generate_alternatives(request, catalog, k=4, batches=BATCHES):
        for room in alt.plan.rooms:
            if targets[room.id]:
                assert useful_area_mm2(room, alt.plan) / 1e6 <= 2 * targets[room.id], room.id


def test_no_room_shrinks_far_below_its_target():
    # na 3ª alternativa deste pedido a cozinha saía com 3,6 m² para um alvo de 10 m² (calibração do M1.1)
    from pygridplan.model.walls import useful_area_mm2
    from pygridplan.scoring.score import room_target_m2

    request, catalog = load_request(BASIC_PROGRAM.parent / "three-bedroom.json"), load_catalog()
    targets = {r.id: room_target_m2(r, catalog) for r in request.rooms}
    for alt in generate_alternatives(request, catalog, k=3, batches=BATCHES):
        for room in alt.plan.rooms:
            if targets[room.id]:
                assert useful_area_mm2(room, alt.plan) / 1e6 >= 0.7 * targets[room.id], room.id


OFFICE_PROGRAM = Request(
    site=Site(width_mm=14000, depth_mm=30000),
    rooms=tuple(RoomRequest(id=t, type=t) for t in
                ("sala", "cozinha", "lavanderia", "escritorio", "circulacao", "quarto", "banheiro")),
)


@pytest.fixture(scope="module")
def office_alternatives():
    return generate_alternatives(OFFICE_PROGRAM, load_catalog(), k=2)


def _touching(plan):
    from pygridplan.validation.access import MIN_PASSAGE_MM, passages

    return {frozenset(pair) for pair, length in passages(plan).items() if length >= MIN_PASSAGE_MM}


def test_rooms_with_required_window_have_an_exterior_wall(office_alternatives):
    # design 22.2 (revisto na S06): sala e quartos sempre; banheiro, cozinha e escritório só preferem
    from pygridplan.model.walls import exterior_sides

    catalog = load_catalog()
    for alt in office_alternatives:
        for room in alt.plan.rooms:
            if catalog.get(room.type).window_need == "required":
                assert exterior_sides(room, alt.plan), room.id
        flagged = {w.room_ids[0] for w in alt.warnings if w.code == "no_exterior_wall"}
        assert flagged == {r.id for r in alt.plan.rooms
                           if catalog.get(r.type).window_need and not exterior_sides(r, alt.plan)}


def test_strict_window_rule_gives_every_window_room_an_exterior_wall():
    from pygridplan.model.walls import exterior_sides

    catalog = load_catalog()
    request = OFFICE_PROGRAM.model_copy(update={"window_rule": "strict"})
    for alt in generate_alternatives(request, catalog, k=1):
        assert all(exterior_sides(r, alt.plan) for r in alt.plan.rooms if catalog.get(r.type).window_need)


def test_circulation_and_office_are_reached_from_the_living_room(office_alternatives):
    # design 22.1: preferência (não proibição); com espaço sobrando, a melhor alternativa segue a preferência
    for alt in office_alternatives[:1]:
        touching = _touching(alt.plan)
        assert frozenset(("circulacao", "sala")) in touching
        assert touching & {frozenset(("escritorio", "sala")), frozenset(("escritorio", "circulacao"))}
