"""Nota decomposta por critério (design 5.3–5.6). Média ponderada linear no M1."""

from pydantic import BaseModel, ConfigDict

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan, Rect
from pygridplan.model.request import RoomRequest, Request
from pygridplan.model.walls import useful_area_mm2
from pygridplan.validation.access import MIN_PASSAGE_MM, passages

# fonte única dos pesos: a nota e o objetivo do solver usam estes valores
WEIGHTS = {"relations": 3.0, "area_fit": 2.0, "compactness": 1.0, "circulation": 1.0, "solar": 1.0, "wet_grouping": 0.5}
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
    if t.comfort_area_m2:
        return t.comfort_area_m2[0]
    return t.min_area_m2 * DEFAULT_TARGET_FACTOR if t.min_area_m2 else None


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
    circulation = sum(useful[r.id] for r in plan.rooms if r.type == CIRCULATION_TYPE)
    values["circulation"] = _clip(1 - circulation / sum(useful.values()))

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

    criteria = tuple(Criterion(name=n, value=v, weight=WEIGHTS[n]) for n, v in values.items())
    total = sum(c.value * c.weight for c in criteria) / sum(c.weight for c in criteria)
    return Score(total=total, criteria=criteria)
