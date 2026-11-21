"""Nota decomposta por critério (design 5.3–5.6). Média ponderada linear no M1."""

from pydantic import BaseModel, ConfigDict

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan, Rect
from pygridplan.model.request import RoomRequest, Request
from pygridplan.model.walls import exterior_sides, useful_area_mm2
from pygridplan.validation.access import MIN_PASSAGE_MM, passages

# fonte única dos pesos: a nota e o objetivo do solver usam estes valores
WEIGHTS = {"relations": 3.0, "area_fit": 2.0, "compactness": 3.0, "circulation": 1.0, "solar": 1.0,
           "wet_grouping": 0.5, "alignment": 1.0, "zoning": 2.0, "ventilation": 1.0}
DEFAULT_TARGET_FACTOR = 1.25
CIRCULATION_TYPE = "circulacao"


class Criterion(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    value: float  # 0..1
    weight: float


class Score(BaseModel):
    model_config = ConfigDict(frozen=True)

    total: float
    criteria: tuple[Criterion, ...]


def room_target_m2(room: RoomRequest, catalog: Catalog) -> float | None:
    """Alvo explícito > início da faixa de conforto > mínimo × 1,25 > sem alvo. Circulação não tem alvo."""
    if room.target_area_m2 is not None:
        return room.target_area_m2
    t = catalog.get(room.type)
    if t.id == CIRCULATION_TYPE:
        return None
    target = t.comfort_area_m2[0] if t.comfort_area_m2 else (
        t.min_area_m2 * DEFAULT_TARGET_FACTOR if t.min_area_m2 else None)
    if target and t.min_width_mm:  # um alvo abaixo do quadrado da largura mínima é inalcançável
        target = max(target, (t.min_width_mm / 1000) ** 2)
    return target


def bounding_box(plan: Plan) -> Rect:
    xs = [r.rect.x for r in plan.rooms] + [r.rect.x2 for r in plan.rooms]
    ys = [r.rect.y for r in plan.rooms] + [r.rect.y2 for r in plan.rooms]
    return Rect(x=min(xs), y=min(ys), w=max(xs) - min(xs), h=max(ys) - min(ys))


def _clip(v: float) -> float:
    return max(0.0, min(1.0, v))


def score_plan(plan: Plan, request: Request, catalog: Catalog) -> Score:
    rooms = {r.id: r for r in plan.rooms}
    adjacent = {frozenset(p) for p, length in passages(plan).items() if length >= MIN_PASSAGE_MM}
    useful = {r.id: useful_area_mm2(r, plan) / 1e6 for r in plan.rooms}
    box = bounding_box(plan)
    values: dict[str, float] = {}

    if request.relations:
        span = plan.site.width_mm + plan.site.depth_mm
        total_w = sum(rel.intensity for rel in request.relations)
        acc = 0.0
        for rel in request.relations:
            if rel.kind == "near":
                v = float(frozenset((rel.a, rel.b)) in adjacent)
            else:
                a, b = rooms[rel.a].rect, rooms[rel.b].rect
                dist = abs((a.x + a.x2) - (b.x + b.x2)) / 2 + abs((a.y + a.y2) - (b.y + b.y2)) / 2
                v = _clip(dist / span)
            acc += v * rel.intensity
        values["relations"] = acc / total_w

    fits = []
    for req in request.rooms:
        target = room_target_m2(req, catalog)
        if target:
            fits.append(abs(useful[req.id] - target) / target)
    if fits:
        values["area_fit"] = _clip(1 - sum(fits) / len(fits))

    values["compactness"] = sum(r.rect.area_mm2 for r in plan.rooms) / box.area_mm2
    circulation = _circulation(plan, catalog, adjacent, useful)
    if circulation is not None:
        values["circulation"] = circulation

    sunny = [r for r in plan.rooms if catalog.get(r.type).sun]
    if request.site.north and sunny:
        on_north = {
            "front": lambda r: r.y == box.y, "back": lambda r: r.y2 == box.y2,
            "left": lambda r: r.x == box.x, "right": lambda r: r.x2 == box.x2,
        }[request.site.north]
        values["solar"] = sum(on_north(r.rect) for r in sunny) / len(sunny)

    wet = [r.id for r in plan.rooms if catalog.get(r.type).wet]
    if len(wet) >= 2:
        grouped = [w for w in wet if any(frozenset((w, o)) in adjacent for o in wet if o != w)]
        values["wet_grouping"] = len(grouped) / len(wet)

    zoning = zoning_value(plan, catalog, adjacent)
    if zoning is not None:
        values["zoning"] = zoning

    needing = [r for r in plan.rooms if catalog.get(r.type).window_need]
    if needing:
        values["ventilation"] = sum(bool(exterior_sides(r, plan)) for r in needing) / len(needing)

    alignment = _alignment(plan, adjacent)
    if alignment is not None:
        values["alignment"] = alignment

    criteria = tuple(Criterion(name=n, value=v, weight=WEIGHTS[n]) for n, v in values.items())
    total = sum(c.value * c.weight for c in criteria) / sum(c.weight for c in criteria)
    return Score(total=total, criteria=criteria)


def _circulation(plan: Plan, catalog: Catalog, adjacent: set[frozenset[str]],
                 useful: dict[str, float]) -> float | None:
    """Função x economia da circulação (design 21.2); sem cômodo de circulação o critério não se aplica.

    Função: fração dos privativos da zona íntima que abrem para a circulação. Quem abre para a própria
    suíte (closet, banheiro de suíte) não entra na conta. Economia: 1 − área de circulação / área útil total.
    """
    halls = [r.id for r in plan.rooms if r.type == CIRCULATION_TYPE]
    if not halls:
        return None
    need = []
    for r in plan.rooms:
        kind = catalog.get(r.type)
        in_suite = any(r.type in catalog.get(o.type).suite_access and frozenset((r.id, o.id)) in adjacent
                       for o in plan.rooms)
        if kind.passage == "private" and kind.zone == "intima" and not in_suite:
            need.append(r.id)
    served = sum(any(frozenset((rid, hall)) in adjacent for hall in halls) for rid in need) / len(need) if need else 1.0
    return served * _clip(1 - sum(useful[hall] for hall in halls) / sum(useful.values()))


def zoning_value(plan: Plan, catalog: Catalog, adjacent: set[frozenset[str]]) -> float | None:
    """Zoneamento (design 22.1): por onde se chega à circulação e aos cômodos de uso concentrado.

    Cada um vale o maior `access_hub` entre os vizinhos com passagem (sala 1, cozinha 0,5, área de serviço 0);
    para os de uso concentrado, a circulação também vale 1. Sem cômodo de acesso no programa, não se aplica.
    """
    hub = {r.id: catalog.get(r.type).access_hub or 0.0 for r in plan.rooms}
    halls = {r.id for r in plan.rooms if r.type == CIRCULATION_TYPE}
    items = list(halls) + [r.id for r in plan.rooms if catalog.get(r.type).concentrated_use]
    if not items or not any(hub.values()):
        return None
    credits = []
    for item in items:
        near = [o for o in hub if o != item and frozenset((item, o)) in adjacent]
        credits.append(max([1.0 if o in halls and item not in halls else hub[o] for o in near], default=0.0))
    return sum(credits) / len(credits)


def _alignment(plan: Plan, adjacent: set[frozenset[str]]) -> float | None:
    """Vizinhos com faces na mesma reta + cômodos do mesmo tipo com as mesmas dimensões (design 20.1)."""
    rooms = plan.rooms
    hits = total = 0
    for i, a in enumerate(rooms):
        for b in rooms[i + 1:]:
            ra, rb = a.rect, b.rect
            if frozenset((a.id, b.id)) in adjacent:
                total += 1
                side_by_side = ra.x2 == rb.x or rb.x2 == ra.x
                hits += (ra.y == rb.y or ra.y2 == rb.y2) if side_by_side else (ra.x == rb.x or ra.x2 == rb.x2)
            if a.type == b.type:
                total += 1
                hits += sorted((ra.w, ra.h)) == sorted((rb.w, rb.h))
    return hits / total if total else None
