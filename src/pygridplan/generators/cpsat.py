"""Gerador CP-SAT da etapa 1: posição e tamanho dos cômodos na grade (design 8).

Variáveis em unidades de grade (GRID mm). Formulação fixada em docs/plans/m1-cpsat-generator.md (Tarefa 5).
"""

import math
from collections.abc import Sequence

from ortools.sat.python import cp_model

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan, Rect, Room
from pygridplan.model.request import Request
from pygridplan.scoring.diversity import Pattern
from pygridplan.scoring.score import CIRCULATION_TYPE, WEIGHTS, room_target_m2
from pygridplan.validation.access import MIN_PASSAGE_MM

GRID = 100
DEFAULT_TIME_LIMIT = 0.5  # unidades determinísticas do CP-SAT; ~4–5 s de relógio no hardware de referência


class _Box:
    """Variáveis de um cômodo."""

    def __init__(self, m: cp_model.CpModel, name: str, xr: tuple[int, int], yr: tuple[int, int],
                 min_side: int):
        self.x = m.new_int_var(*xr, f"x_{name}")
        self.y = m.new_int_var(*yr, f"y_{name}")
        self.x2 = m.new_int_var(*xr, f"x2_{name}")
        self.y2 = m.new_int_var(*yr, f"y2_{name}")
        self.w = m.new_int_var(min_side, xr[1] - xr[0], f"w_{name}")
        self.h = m.new_int_var(min_side, yr[1] - yr[0], f"h_{name}")
        self.ix = m.new_interval_var(self.x, self.w, self.x2, f"ix_{name}")
        self.iy = m.new_interval_var(self.y, self.h, self.y2, f"iy_{name}")


def solve_layout(request: Request, catalog: Catalog, *, seed: int = 0, time_limit: float = DEFAULT_TIME_LIMIT,
                 forbidden: Sequence[Pattern] = (), min_diff: int = 1) -> Plan | None:
    site = request.site
    ext = Plan(site=site).wall_ext_mm
    e, sb, att = ext // 2, site.setbacks, site.attached_sides
    xr = (math.ceil(((0 if "left" in att else sb.left) + e) / GRID),
          (site.width_mm - (0 if "right" in att else sb.right) - e) // GRID)
    yr = (math.ceil((sb.front + e) / GRID),
          (site.depth_mm - (0 if "back" in att else sb.back) - e) // GRID)
    if xr[1] <= xr[0] or yr[1] <= yr[0]:
        return None

    m = cp_model.CpModel()
    reqs = request.rooms
    types = [catalog.get(r.type) for r in reqs]
    n = len(reqs)
    gap_min = math.ceil(ext / GRID)  # vão entre paredes: 0 ou >= uma parede externa (design 5.1)
    door = math.ceil(MIN_PASSAGE_MM / GRID)

    boxes = []
    for r, t in zip(reqs, types):
        min_side = math.ceil(((t.min_width_mm or 0) + ext) / GRID)
        boxes.append(_Box(m, r.id, xr, yr, max(min_side, gap_min + 1)))
    m.add_no_overlap_2d([b.ix for b in boxes], [b.iy for b in boxes])

    # área útil aproximada (conservadora: meia parede externa em todos os lados), em mm²
    area = []
    for b, t in zip(boxes, types):
        uw = m.new_int_var(0, (xr[1] - xr[0]) * GRID, "")
        uh = m.new_int_var(0, (yr[1] - yr[0]) * GRID, "")
        m.add(uw == b.w * GRID - ext)
        m.add(uh == b.h * GRID - ext)
        a = m.new_int_var(0, (xr[1] - xr[0]) * (yr[1] - yr[0]) * GRID * GRID, "")
        m.add_multiplication_equality(a, [uw, uh])
        if t.min_area_m2:
            m.add(a >= round(t.min_area_m2 * 1e6))
        area.append(a)

    # posições relativas reificadas (o Pattern) e vão entre paredes
    rel: dict[tuple[int, int], tuple] = {}
    for i in range(n):
        for j in range(i + 1, n):
            bi, bj = boxes[i], boxes[j]
            lits = []
            for lo, hi in ((bi.x2, bj.x), (bj.x2, bi.x), (bi.y2, bj.y), (bj.y2, bi.y)):
                b = m.new_bool_var("")
                m.add(lo <= hi).only_enforce_if(b)
                m.add(lo > hi).only_enforce_if(~b)
                touch = m.new_bool_var("")
                m.add(hi == lo).only_enforce_if(touch)
                m.add(hi - lo >= gap_min).only_enforce_if([b, ~touch])
                lits.append(b)
            m.add_bool_or(lits)
            rel[(i, j)] = tuple(lits)

    adj_cache: dict[tuple[int, int], cp_model.IntVar] = {}

    def adj(i: int, j: int) -> cp_model.IntVar:
        """Booleano: i e j compartilham parede >= MIN_PASSAGE_MM (só a implicação adj => contato)."""
        key = (min(i, j), max(i, j))
        if key not in adj_cache:
            bi, bj = boxes[key[0]], boxes[key[1]]
            subs = []
            for same, (a1, a2, b1, b2) in (
                ((bi.x2, bj.x), (bi.y, bi.y2, bj.y, bj.y2)), ((bj.x2, bi.x), (bi.y, bi.y2, bj.y, bj.y2)),
                ((bi.y2, bj.y), (bi.x, bi.x2, bj.x, bj.x2)), ((bj.y2, bi.y), (bi.x, bi.x2, bj.x, bj.x2)),
            ):
                s = m.new_bool_var("")
                m.add(same[0] == same[1]).only_enforce_if(s)
                m.add(a1 + door <= b2).only_enforce_if(s)
                m.add(b1 + door <= a2).only_enforce_if(s)
                subs.append(s)
            v = m.new_bool_var("")
            m.add_bool_or(subs).only_enforce_if(v)
            adj_cache[key] = v
        return adj_cache[key]

    # caixa envolvente e frente da casa
    bx1, by1 = m.new_int_var(*xr, ""), m.new_int_var(*yr, "")
    bx2, by2 = m.new_int_var(*xr, ""), m.new_int_var(*yr, "")
    m.add_min_equality(bx1, [b.x for b in boxes])
    m.add_min_equality(by1, [b.y for b in boxes])
    m.add_max_equality(bx2, [b.x2 for b in boxes])
    m.add_max_equality(by2, [b.y2 for b in boxes])

    def on_side(b: _Box, side: str) -> cp_model.IntVar:
        v = m.new_bool_var("")
        expr = {"front": (b.y, by1), "back": (b.y2, by2), "left": (b.x, bx1), "right": (b.x2, bx2)}[side]
        m.add(expr[0] == expr[1]).only_enforce_if(v)
        return v

    # acesso local (condição necessária; a global é checada depois por check_access)
    trav = [i for i in range(n) if types[i].passage == "traversable"]
    front = {i: on_side(boxes[i], "front") for i in trav}
    m.add_bool_or([front[i] for i in trav])
    for i in range(n):
        if types[i].passage == "traversable":
            m.add_bool_or([adj(i, j) for j in trav if j != i] + [front[i]])
        else:
            hosts = [j for j in range(n) if j != i and (j in trav or types[i].id in types[j].suite_access)]
            m.add_bool_or([adj(i, j) for j in hosts])

    # diversidade: diferir dos padrões proibidos em pelo menos min_diff pares
    ids = [r.id for r in reqs]
    for pattern in forbidden:
        diffs = []
        for (i, j), lits in rel.items():
            old = pattern.get((ids[i], ids[j]))
            if old is None:
                continue
            d = m.new_bool_var("")
            m.add_bool_or([lit if not was else ~lit for lit, was in zip(lits, old)]).only_enforce_if(d)
            diffs.append(d)
        m.add(sum(diffs) >= min_diff)

    # objetivo (pesos de scoring.WEIGHTS)
    span = (site.width_mm + site.depth_mm) / GRID
    terms = []
    if request.relations:
        total_int = sum(r.intensity for r in request.relations)
        index = {rid: k for k, rid in enumerate(ids)}
        for r in request.relations:
            i, j = index[r.a], index[r.b]
            coef = WEIGHTS["relations"] * r.intensity / total_int
            if r.kind == "near":
                terms.append(coef * adj(i, j))
            else:
                dx, dy = m.new_int_var(0, 4 * int(span), ""), m.new_int_var(0, 4 * int(span), "")
                m.add_abs_equality(dx, boxes[i].x + boxes[i].x2 - boxes[j].x - boxes[j].x2)
                m.add_abs_equality(dy, boxes[i].y + boxes[i].y2 - boxes[j].y - boxes[j].y2)
                terms.append(coef / (2 * span) * (dx + dy))
    targets = [(k, room_target_m2(r, catalog)) for k, r in enumerate(reqs)]
    targets = [(k, t) for k, t in targets if t]
    for k, t in targets:
        dev = m.new_int_var(0, 10**10, "")
        m.add_abs_equality(dev, area[k] - round(t * 1e6))
        terms.append(-WEIGHTS["area_fit"] / len(targets) / (t * 1e6) * dev)
    terms.append(-WEIGHTS["compactness"] / span * (bx2 - bx1 + by2 - by1))
    total_target = sum(t for _, t in targets) * 1e6 or 1.0
    for k, r in enumerate(reqs):
        if types[k].id == CIRCULATION_TYPE:
            terms.append(-WEIGHTS["circulation"] / total_target * area[k])
    sunny = [k for k in range(n) if types[k].sun]
    if site.north and sunny:
        terms += [WEIGHTS["solar"] / len(sunny) * on_side(boxes[k], site.north) for k in sunny]
    wet = [k for k in range(n) if types[k].wet]
    wet_pairs = [(a, b) for x, a in enumerate(wet) for b in wet[x + 1:]]
    terms += [WEIGHTS["wet_grouping"] / len(wet_pairs) * adj(a, b) for a, b in wet_pairs]
    m.maximize(sum(terms))

    solver = cp_model.CpSolver()
    solver.parameters.random_seed = seed
    solver.parameters.max_deterministic_time = time_limit
    solver.parameters.num_workers = 8
    solver.parameters.interleave_search = True  # torna o paralelo reprodutível (mesma semente = mesma planta)
    if solver.solve(m) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    rooms = tuple(
        Room(id=r.id, type=r.type, rect=Rect(x=solver.value(b.x) * GRID, y=solver.value(b.y) * GRID,
                                             w=solver.value(b.w) * GRID, h=solver.value(b.h) * GRID))
        for r, b in zip(reqs, boxes)
    )
    return Plan(site=site, rooms=rooms)
