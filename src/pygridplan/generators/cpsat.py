"""Gerador CP-SAT da etapa 1: posição e tamanho dos cômodos (design 8 e 21).

Formulação por malha de linhas de parede (docs/plans/m1-1-calibration.md): cada cômodo ocupa um bloco de
células de uma malha cujas linhas têm posição variável, em múltiplos de GRID mm. Cômodos e recortes de
borda cobrem a malha exatamente, então a casa sai em bloco cheio e com paredes alinhadas por construção.
Resolve em duas fases: topologia (objetivo combinatório) e medidas (topologia fixa, objetivo exato).
"""

import math
from collections.abc import Sequence

from ortools.sat.python import cp_model
from pydantic import BaseModel, ConfigDict

from pygridplan.model.catalog import Catalog, RoomType
from pygridplan.model.plan import Plan, Rect, Room
from pygridplan.model.request import Request
from pygridplan.model.site_defaults import SiteDefaults, load_site_defaults
from pygridplan.scoring.diversity import Pattern, mirrored, relative_pattern
from pygridplan.scoring.score import CIRCULATION_TYPE, WEIGHTS, Score, room_target_m2, score_plan
from pygridplan.validation.access import MIN_PASSAGE_MM, check_access
from pygridplan.validation.checks import Issue, check_recommendations, validate_geometry
from pygridplan.validation.site import check_site

GRID = 100
# constantes de calibração (DEC-0089 a DEC-0091; medições em docs/plans/m1-1-calibration.md)
MAX_LINES = 6  # faixas da malha em cada eixo
MAX_VOIDS = 2  # recortes de borda (casa em L, T ou degrau); vazio fechado é impossível
MAX_TARGET_FACTOR = 1.5  # área aproximada (conservadora) <= 1,5 x alvo (ou x o menor cômodo possível, se o alvo for menor que ele)
MIN_TARGET_FACTOR = 0.7  # e nunca abaixo de 0,7 x alvo: quem pediu 10 m² não recebe 4 m²
MAX_ASPECT = 2.5  # lado maior <= 2,5 x lado menor (menos circulação e áreas externas)
CORRIDOR_MAX_WIDTH_MM = 1500  # circulação é faixa: lado menor (no eixo) até 1,50 m
AREA_WINDOW = (0.8, 1.25)  # fase 1: prêmio por ficar perto do alvo (o piso e o teto duros vêm à parte)
VOID_FIXED, VOID_CELL = 0.6, 0.05  # fase 1: custo de existir um recorte e por célula dele (x peso da compacidade)
VOID_SCALE = 1.0  # fase 2: o vazio custa o peso inteiro da compacidade por área
LINE_PRICE = 0.02  # fase 1: por faixa de malha usada (menos linhas = paredes mais alinhadas)
UNTARGETED_PRICE = 2.0  # área de circulação e de cômodo sem alvo (x peso da área)
MIN_DIFF_FRACTION = 0.15  # alternativas diferem em >= 15 % dos pares de cômodos
DEFAULT_TIME_LIMIT = 4.0  # fase 1, em unidades determinísticas do CP-SAT; ~10 s de relógio no hardware de referência
POLISH_TIME = 0.3  # fase 2


class _Cell:
    """Bloco de células [c1, c2) x [r1, r2) da malha; os cômodos têm também as coordenadas reais."""

    def __init__(self, m: cp_model.CpModel, name: str, X: list[cp_model.IntVar], Y: list[cp_model.IntVar],
                 xr: tuple[int, int], yr: tuple[int, int], present: cp_model.IntVar | None = None):
        P, Q = len(X) - 1, len(Y) - 1
        lo = 1 if present is None else 0
        self.c1, self.c2 = m.new_int_var(0, P, f"c1_{name}"), m.new_int_var(0, P, f"c2_{name}")
        self.r1, self.r2 = m.new_int_var(0, Q, f"r1_{name}"), m.new_int_var(0, Q, f"r2_{name}")
        cw, rh = m.new_int_var(lo, P, f"cw_{name}"), m.new_int_var(lo, Q, f"rh_{name}")
        m.add(self.c2 == self.c1 + cw)
        m.add(self.r2 == self.r1 + rh)
        self.cells = m.new_int_var(0, P * Q, f"n_{name}")
        m.add_multiplication_equality(self.cells, [cw, rh])
        if present is None:
            self.ic = m.new_interval_var(self.c1, cw, self.c2, f"ic_{name}")
            self.ir = m.new_interval_var(self.r1, rh, self.r2, f"ir_{name}")
            self.x, self.x2 = m.new_int_var(*xr, f"x_{name}"), m.new_int_var(*xr, f"x2_{name}")
            self.y, self.y2 = m.new_int_var(*yr, f"y_{name}"), m.new_int_var(*yr, f"y2_{name}")
            m.add_element(self.c1, X, self.x)
            m.add_element(self.c2, X, self.x2)
            m.add_element(self.r1, Y, self.y)
            m.add_element(self.r2, Y, self.y2)
        else:  # recorte opcional: ausente fica na origem, com tamanho zero
            self.ic = m.new_optional_interval_var(self.c1, cw, self.c2, present, f"ic_{name}")
            self.ir = m.new_optional_interval_var(self.r1, rh, self.r2, present, f"ir_{name}")
            m.add(cw >= 1).only_enforce_if(present)
            m.add(rh >= 1).only_enforce_if(present)
            for var in (self.c1, self.c2, self.r1, self.r2):
                m.add(var == 0).only_enforce_if(~present)


def _social_bath_pairs(types: Sequence[RoomType]) -> list[tuple[int, int]]:
    """Pares (banheiro, cômodo) que tornam um banheiro social (design 21.2, item 3): basta um deles existir.

    Banheiro da zona íntima abre para a circulação (ou, sem circulação, para um atravessável); o lavabo,
    da zona social, para qualquer atravessável. Abrir só para um quarto não conta.
    """
    trav = [j for j, t in enumerate(types) if t.passage == "traversable"]
    circ = [j for j in trav if types[j].id == CIRCULATION_TYPE]
    return [(i, j) for i, t in enumerate(types) if t.passage == "private" and t.wet
            for j in (circ if circ and t.zone == "intima" else trav)]


def solve_layout(request: Request, catalog: Catalog, *, seed: int = 0, time_limit: float = DEFAULT_TIME_LIMIT,
                 forbidden: Sequence[Pattern] = (), min_diff: int = 1) -> Plan | None:
    return _solve(request, catalog, seed=seed, time_limit=time_limit, forbidden=forbidden, min_diff=min_diff)[0]


def _solve(request: Request, catalog: Catalog, *, seed: int, time_limit: float,
           forbidden: Sequence[Pattern] = (), min_diff: int = 1) -> tuple[Plan | None, str]:
    """(planta, situação): situação é "ok", "infeasible" (provado que não cabe) ou "timeout"."""
    plan, status, topology = _phase(request, catalog, seed, time_limit, forbidden, min_diff, None)
    if plan is None:
        return None, status
    polished = _phase(request, catalog, seed, POLISH_TIME, forbidden, min_diff, topology)[0]
    return polished or plan, "ok"


def _phase(request: Request, catalog: Catalog, seed: int, time_limit: float, forbidden: Sequence[Pattern],
           min_diff: int, topology: list[int] | None) -> tuple[Plan | None, str, list[int]]:
    """Uma fase do gerador; devolve (planta, situação, índices da malha).

    Sem `topology` (fase 1): escolhe quem fica onde, com objetivo combinatório (janelas de área, relações,
    recortes). Com `topology` (fase 2): os índices ficam fixos e só as linhas se movem, com o objetivo exato.
    """
    topo_phase = topology is None
    site = request.site
    ext = Plan(site=site).wall_ext_mm
    e, sb, att = ext // 2, site.setbacks, site.attached_sides
    xr = (math.ceil(((0 if "left" in att else sb.left) + e) / GRID),
          (site.width_mm - (0 if "right" in att else sb.right) - e) // GRID)
    yr = (math.ceil((sb.front + e) / GRID),
          (site.depth_mm - (0 if "back" in att else sb.back) - e) // GRID)
    if xr[1] <= xr[0] or yr[1] <= yr[0]:
        return None, "infeasible", []
    W, H = xr[1] - xr[0], yr[1] - yr[0]

    m = cp_model.CpModel()
    reqs = request.rooms
    types = [catalog.get(r.type) for r in reqs]
    n = len(reqs)
    # linhas de parede distam >= uma passagem: em toda parede comum cabe uma porta, e não há frestas nem
    # paredes quase alinhadas
    gap = math.ceil(max(ext, MIN_PASSAGE_MM) / GRID)
    # lado mínimo universal: cabe uma porta entre as paredes (despensa, depósito, tipos sem mínimo)
    side_min = math.ceil((MIN_PASSAGE_MM + ext) / GRID)
    P, Q = max(1, min(MAX_LINES, n, W // gap)), max(1, min(MAX_LINES, n, H // gap))

    # malha: linhas X[0..P] e Y[0..Q]; só as p (q) primeiras faixas são usadas, as demais ficam em posição canônica
    X = [m.new_int_var(xr[0], xr[1] + P * gap, f"X{k}") for k in range(P + 1)]
    Y = [m.new_int_var(yr[0], yr[1] + Q * gap, f"Y{k}") for k in range(Q + 1)]
    p, q = m.new_int_var(1, P, "p"), m.new_int_var(1, Q, "q")
    for lines, count in ((X, p), (Y, q)):
        for k in range(1, len(lines)):
            used = m.new_bool_var("")
            m.add(count >= k).only_enforce_if(used)
            m.add(count < k).only_enforce_if(~used)
            m.add(lines[k] - lines[k - 1] >= gap).only_enforce_if(used)
            m.add(lines[k] - lines[k - 1] == gap).only_enforce_if(~used)
    bx1, by1 = X[0], Y[0]
    bx2, by2 = m.new_int_var(*xr, "bx2"), m.new_int_var(*yr, "by2")
    m.add_element(p, X, bx2)
    m.add_element(q, Y, by2)

    # implantação previsível (design 20.1, item 4): frente no recuo frontal; centralizada na largura,
    # ou encostada no lado pedido
    m.add(by1 == yr[0])
    if "left" in att and "right" not in att:
        m.add(bx1 == xr[0])
    elif "right" in att and "left" not in att:
        m.add(bx2 == xr[1])
    else:  # nenhuma ou as duas laterais encostadas: centralizada na largura
        m.add((bx1 - xr[0]) - (xr[1] - bx2) <= 1)
        m.add((xr[1] - bx2) - (bx1 - xr[0]) <= 1)

    targets = {k: t for k, r in enumerate(reqs) if (t := room_target_m2(r, catalog))}
    total_target_mm2 = sum(targets.values()) * 1e6 or 1e6
    cells = [_Cell(m, r.id, X, Y, xr, yr) for r in reqs]
    w, h, area, rect_area = [], [], [], []
    limits: dict[int, tuple[int, float]] = {}
    for k, (c, t) in enumerate(zip(cells, types)):
        m.add(c.c2 <= p)
        m.add(c.r2 <= q)
        min_side = max(math.ceil(((t.min_width_mm or 0) + ext) / GRID), side_min)
        max_w, max_h = max(W, min_side), max(H, min_side)
        if k in targets:
            # trava: nunca muito acima do alvo, mas sempre com folga sobre o mínimo do próprio cômodo
            side = max(t.min_width_mm or 0, side_min * GRID - ext)
            smallest = max((t.min_area_m2 or 0) * 1e6, side * side)
            cap = round(MAX_TARGET_FACTOR * max(targets[k] * 1e6, smallest))
            limits[k] = (cap, smallest)
            longest = int((cap / (min_side * GRID - ext) + ext) // GRID)  # lado máximo que respeita a trava
            max_w, max_h = max(min(max_w, longest), min_side), max(min(max_h, longest), min_side)
        wk, hk = m.new_int_var(min_side, max_w, ""), m.new_int_var(min_side, max_h, "")
        m.add(wk == c.x2 - c.x)
        m.add(hk == c.y2 - c.y)
        if t.id == CIRCULATION_TYPE:  # circulação é faixa estreita, não cômodo de enchimento
            narrow = m.new_bool_var("")
            m.add(wk <= CORRIDOR_MAX_WIDTH_MM // GRID).only_enforce_if(narrow)
            m.add(hk <= CORRIDOR_MAX_WIDTH_MM // GRID).only_enforce_if(~narrow)
        elif not t.exterior:
            m.add(10 * wk <= round(MAX_ASPECT * 10) * hk)
            m.add(10 * hk <= round(MAX_ASPECT * 10) * wk)
        ra = m.new_int_var(min_side * min_side, max_w * max_h, "")
        m.add_multiplication_equality(ra, [wk, hk])
        # área útil aproximada (conservadora: meia parede externa em todos os lados), em mm²
        a = GRID * GRID * ra - GRID * ext * (wk + hk) + ext * ext
        if t.min_area_m2:
            m.add(a >= round(t.min_area_m2 * 1e6))
        if k in limits:
            m.add(a <= limits[k][0])
            m.add(a >= min(round(MIN_TARGET_FACTOR * targets[k] * 1e6), limits[k][0]))
        w.append(wk)
        h.append(hk)
        area.append(a)
        rect_area.append(ra)

    voids = []
    for v in range(MAX_VOIDS):
        present = m.new_bool_var(f"void{v}")
        c = _Cell(m, f"void{v}", X, Y, xr, yr, present)
        m.add(c.c2 <= p)
        m.add(c.r2 <= q)
        edge = [m.new_bool_var("") for _ in range(4)]  # recorte só na borda: nunca um vazio fechado
        m.add(c.c1 == 0).only_enforce_if(edge[0])
        m.add(c.c2 == p).only_enforce_if(edge[1])
        m.add(c.r1 == 0).only_enforce_if(edge[2])
        m.add(c.r2 == q).only_enforce_if(edge[3])
        m.add_bool_or(edge).only_enforce_if(present)
        voids.append((present, c))
    for (first, _), (second, _) in zip(voids, voids[1:]):
        m.add_implication(second, first)  # simetria: o segundo recorte só existe se o primeiro existir

    every = cells + [c for _, c in voids]
    m.add_no_overlap_2d([c.ic for c in every], [c.ir for c in every])
    pq = m.new_int_var(1, P * Q, "pq")
    m.add_multiplication_equality(pq, [p, q])
    m.add(sum(c.cells for c in every) == pq)  # cômodos + recortes cobrem a malha exatamente

    def at(var: cp_model.IntVar, value: cp_model.IntVar | int) -> cp_model.IntVar:
        """Booleano que implica var == value."""
        b = m.new_bool_var("")
        m.add(var == value).only_enforce_if(b)
        return b

    side_cache: dict[tuple[int, str], cp_model.IntVar] = {}

    def on_side(i: int, side: str) -> cp_model.IntVar:
        if (i, side) not in side_cache:
            c = cells[i]
            var, value = {"front": (c.r1, 0), "back": (c.r2, q), "left": (c.c1, 0), "right": (c.c2, p)}[side]
            side_cache[(i, side)] = at(var, value)
        return side_cache[(i, side)]

    # a malha é a caixa envolvente dos cômodos (a frente vem da entrada); cada linha interna usada é face
    # de algum bloco, senão a mesma planta teria várias representações
    for side in ("left", "right", "back"):
        m.add_bool_or([on_side(i, side) for i in range(n)])
    for k in range(1, P):
        m.add_bool_or([at(c.c1, k) for c in every] + [at(p, kk) for kk in range(1, k + 1)])
    for k in range(1, Q):
        m.add_bool_or([at(c.r1, k) for c in every] + [at(q, kk) for kk in range(1, k + 1)])

    adj_cache: dict[tuple[int, int], cp_model.IntVar] = {}

    def adj(i: int, j: int) -> cp_model.IntVar:
        """Booleano que implica parede comum: como as linhas distam >= uma passagem, qualquer trecho comum serve."""
        key = (min(i, j), max(i, j))
        if key not in adj_cache:
            ci, cj = cells[key[0]], cells[key[1]]
            subs = []
            for same, (a1, a2, b1, b2) in (
                ((ci.c2, cj.c1), (ci.r1, ci.r2, cj.r1, cj.r2)), ((cj.c2, ci.c1), (ci.r1, ci.r2, cj.r1, cj.r2)),
                ((ci.r2, cj.r1), (ci.c1, ci.c2, cj.c1, cj.c2)), ((cj.r2, ci.r1), (ci.c1, ci.c2, cj.c1, cj.c2)),
            ):
                s = m.new_bool_var("")
                m.add(same[0] == same[1]).only_enforce_if(s)
                m.add(a1 < b2).only_enforce_if(s)
                m.add(b1 < a2).only_enforce_if(s)
                subs.append(s)
            v = m.new_bool_var("")
            m.add_bool_or(subs).only_enforce_if(v)
            adj_cache[key] = v
        return adj_cache[key]

    # acesso local (condição necessária; a global é checada depois por check_access). A circulação tem
    # função (design 21.2): a entrada da casa não é por ela, ela liga pelo menos dois cômodos, e os
    # privativos da zona íntima abrem para ela (ou para a própria suíte), não para a sala ou a cozinha
    trav = [i for i in range(n) if types[i].passage == "traversable"]
    circ = [i for i in trav if types[i].id == CIRCULATION_TYPE]
    entry = [i for i in trav if i not in circ] or trav
    m.add_bool_or([on_side(i, "front") for i in entry])
    for i in range(n):
        if types[i].passage == "traversable":
            m.add_bool_or([adj(i, j) for j in trav if j != i] + ([on_side(i, "front")] if i in entry else []))
        else:
            suite = [j for j in range(n) if j != i and types[i].id in types[j].suite_access]
            access = circ if circ and types[i].zone == "intima" else trav
            m.add_bool_or([adj(i, j) for j in dict.fromkeys(access + suite)])
    if n >= 3:
        for c in circ:
            m.add(sum(adj(c, j) for j in range(n) if j != c) >= 2)
    social_baths = _social_bath_pairs(types)
    if social_baths:
        m.add_bool_or([adj(i, j) for i, j in social_baths])

    # conectividade global dos atravessáveis (fluxo de uma única entrada na frente): sem isso o solver
    # cria "ilhas" e check_access rejeita a planta
    if len(trav) > 1:
        big = len(trav) - 1
        root = {i: m.new_bool_var("") for i in entry}
        m.add_exactly_one(root.values())
        flow: dict[tuple[int, int], cp_model.IntVar] = {}
        for i in trav:
            if i in root:
                m.add_implication(root[i], on_side(i, "front"))
            for j in trav:
                if i != j:
                    f = m.new_int_var(0, big, "")
                    m.add(f == 0).only_enforce_if(~adj(i, j))
                    flow[(i, j)] = f
        for i in trav:
            inflow = sum(flow[(j, i)] for j in trav if j != i)
            outflow = sum(flow[(i, j)] for j in trav if j != i)
            m.add(inflow - outflow == 1 - len(trav) * (root[i] if i in root else 0))

    # diversidade: diferir dos padrões proibidos em pelo menos min_diff pares
    ids = [r.id for r in reqs]
    rel: dict[tuple[int, int], list[cp_model.IntVar]] = {}
    for i in range(n if forbidden else 0):
        for j in range(i + 1, n):
            ci, cj = cells[i], cells[j]
            for lo, hi in ((ci.c2, cj.c1), (cj.c2, ci.c1), (ci.r2, cj.r1), (cj.r2, ci.r1)):
                b = m.new_bool_var("")
                m.add(lo <= hi).only_enforce_if(b)
                m.add(lo > hi).only_enforce_if(~b)
                rel.setdefault((i, j), []).append(b)
    for pattern in forbidden:
        diffs = []
        for (i, j), lits in rel.items():
            old = pattern.get((ids[i], ids[j]))
            if old is None:
                continue
            # difere de verdade só se nenhuma relação que valia continua valendo (diagonal não conta)
            d = m.new_bool_var("")
            for lit, was in zip(lits, old):
                if was:
                    m.add_implication(d, ~lit)
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
                m.add_abs_equality(dx, cells[i].x + cells[i].x2 - cells[j].x - cells[j].x2)
                m.add_abs_equality(dy, cells[i].y + cells[i].y2 - cells[j].y - cells[j].y2)
                terms.append(coef / (2 * span) * (dx + dy))
    for k, t in targets.items():
        cap, smallest = limits[k]
        if topo_phase:  # o desvio de área (um produto) fica para a fase 2; aqui, estar dentro das janelas
            lo_f, hi_f = AREA_WINDOW
            hi = min(cap, round(max(hi_f * t * 1e6, 1.25 * smallest)))
            inside = m.new_bool_var("")
            m.add(area[k] >= min(round(lo_f * t * 1e6), hi)).only_enforce_if(inside)
            m.add(area[k] <= hi).only_enforce_if(inside)
            # metade do peso da área (calibrado na bancada; uma segunda janela, folgada, era inerte com o piso duro)
            terms.append(WEIGHTS["area_fit"] / len(targets) / 2 * inside)
        else:
            dev = m.new_int_var(0, 10**10, "")
            m.add_abs_equality(dev, area[k] - round(t * 1e6))
            # maior entre o relativo (protege cômodos pequenos) e o absoluto (protege os grandes)
            coef = max(1 / (len(targets) * t * 1e6), 1 / total_target_mm2)
            terms.append(-WEIGHTS["area_fit"] * coef * dev)
    # bloco cheio (design 20.1, item 1): recortes custam caro
    if topo_phase:
        for present, c in voids:
            terms.append(-WEIGHTS["compactness"] * (VOID_FIXED * present + VOID_CELL * c.cells))
        terms.append(-LINE_PRICE * (p + q))
    else:
        bw, bh = m.new_int_var(0, W, ""), m.new_int_var(0, H, "")
        m.add(bw == bx2 - bx1)
        m.add(bh == by2 - by1)
        box_area = m.new_int_var(0, W * H, "")
        m.add_multiplication_equality(box_area, [bw, bh])
        terms.append(-WEIGHTS["compactness"] * VOID_SCALE / (total_target_mm2 / GRID**2) * (box_area - sum(rect_area)))
    # cômodos iguais (mesmo tipo e mesmo alvo) com as mesmas medidas (design 20.1, item 3)
    twins = [(i, j) for i in range(n) for j in range(i + 1, n)
             if types[i].id == types[j].id and targets.get(i) == targets.get(j)]
    for i, j in twins:
        same = m.new_bool_var("")
        m.add(w[i] == w[j]).only_enforce_if(same)
        m.add(h[i] == h[j]).only_enforce_if(same)
        terms.append(WEIGHTS["alignment"] / len(twins) * same)
    # circulação e cômodos sem área-alvo: área custa, senão incham para encher o bloco
    price = UNTARGETED_PRICE * WEIGHTS["area_fit"] / total_target_mm2
    for k in range(n):
        if k not in targets:
            # fase 1: semiperímetro como substituto linear da área (1 m de corredor ~ 1 m²)
            terms.append(-price * (GRID * 1000 * (w[k] + h[k]) if topo_phase else area[k]))
    sunny = [k for k in range(n) if types[k].sun]
    if site.north and sunny:
        terms += [WEIGHTS["solar"] / len(sunny) * on_side(k, site.north) for k in sunny]
    wet = [k for k in range(n) if types[k].wet]
    wet_pairs = [(a, b) for x, a in enumerate(wet) for b in wet[x + 1:]]
    terms += [WEIGHTS["wet_grouping"] / len(wet_pairs) * adj(a, b) for a, b in wet_pairs]
    m.maximize(sum(terms))

    index_vars = [p, q] + [v for c in every for v in (c.c1, c.c2, c.r1, c.r2)]
    for var, value in zip(index_vars, topology or ()):
        m.add(var == value)

    solver = cp_model.CpSolver()
    solver.parameters.random_seed = seed
    solver.parameters.max_deterministic_time = time_limit
    solver.parameters.num_workers = 8
    # reprodutível (mesma semente = mesma planta): oito estratégias de busca rodam lado a lado e vale a melhor
    solver.parameters.interleave_search = True
    status = solver.solve(m)
    if status == cp_model.MODEL_INVALID:  # erro de programação, não "sem tempo"
        raise RuntimeError(f"modelo CP-SAT inválido: {m.validate()}")
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, "infeasible" if status == cp_model.INFEASIBLE else "timeout", []
    rooms = tuple(
        Room(id=r.id, type=r.type, rect=Rect(x=solver.value(c.x) * GRID, y=solver.value(c.y) * GRID,
                                             w=solver.value(wk) * GRID, h=solver.value(hk) * GRID))
        for r, c, wk, hk in zip(reqs, cells, w, h)
    )
    return Plan(site=site, rooms=rooms), "ok", [solver.value(v) for v in index_vars]


class GenerationError(Exception):
    """O pedido não gera nenhuma planta válida."""


class Alternative(BaseModel):
    model_config = ConfigDict(frozen=True)

    plan: Plan
    score: Score
    warnings: tuple[Issue, ...]


ATTACH_SEQUENCE = (("left",), ("left", "right"), ("left", "right", "back"))  # design 20.1, item 5
SIDE_PT = {"left": "esquerda", "right": "direita", "back": "do fundo"}


def _attach_if_needed(request: Request, catalog: Catalog, seed: int, time_limit: float,
                      min_diff: int) -> tuple[Request, Plan | None, Issue | None]:
    """Primeira resolução; sem lados encostados no pedido e sem solução, tenta encostar nas divisas."""
    plan, status = _solve(request, catalog, seed=seed, time_limit=time_limit, min_diff=min_diff)
    if status == "timeout":
        raise GenerationError("A busca esgotou o tempo sem achar nenhuma planta: aumente --time-limit "
                              "(isso não significa que o programa não cabe no terreno).")
    if plan is not None or request.site.attached_sides:
        return request, plan, None
    for sides in ATTACH_SEQUENCE:
        attached = request.model_copy(update={"site": request.site.model_copy(update={"attached_sides": frozenset(sides)})})
        plan, status = _solve(attached, catalog, seed=seed, time_limit=time_limit, min_diff=min_diff)
        if plan is not None:
            names = " e ".join(SIDE_PT[s] for s in sides)
            note = Issue(code="attached", message=f"casa encostada na divisa {names}: o programa, com as áreas "
                                                  "pedidas, não coube com os afastamentos")
            return attached, plan, note
    return request, None, None


def generate_alternatives(request: Request, catalog: Catalog, *, k: int = 4, seed: int = 0,
                          time_limit: float = DEFAULT_TIME_LIMIT, max_attempts: int = 20,
                          defaults: SiteDefaults | None = None) -> list[Alternative]:
    """K plantas válidas e diferentes entre si; soluções rejeitadas são proibidas e o solver roda de novo."""
    if not any(catalog.get(r.type).passage == "traversable" for r in request.rooms):
        raise GenerationError("O programa precisa de ao menos um cômodo atravessável (ex.: sala) para a entrada.")
    pairs = math.comb(len(request.rooms), 2)
    min_diff = max(1, math.ceil(MIN_DIFF_FRACTION * pairs))
    defaults = defaults or load_site_defaults()
    seen: list[Pattern] = []
    accepted: list[Alternative] = []
    request, plan, attach_note = _attach_if_needed(request, catalog, seed, time_limit, min_diff)
    if plan is None:
        raise GenerationError(_no_fit_message(request, catalog))
    # num lote simétrico na largura, a planta espelhada não é uma alternativa de verdade
    site = request.site
    symmetric = site.north not in ("left", "right") and len(site.attached_sides & {"left", "right"}) != 1
    for attempt in range(max_attempts):
        if len(accepted) == k:
            break
        if attempt > 0:
            forbidden = seen + [mirrored(s) for s in seen] if symmetric else seen
            plan = solve_layout(request, catalog, seed=seed + attempt, time_limit=time_limit,
                                forbidden=forbidden, min_diff=min_diff)
            if plan is None:
                break  # não há mais alternativas diferentes
        assert plan is not None
        seen.append(relative_pattern(plan))
        if validate_geometry(plan) or check_access(plan, catalog):
            continue
        notes = ((attach_note,) if attach_note else ()) + tuple(check_recommendations(plan, catalog))
        accepted.append(Alternative(plan=plan, score=score_plan(plan, request, catalog),
                                    warnings=notes + tuple(check_site(plan, defaults))))
    if not accepted:
        raise GenerationError(f"Nenhuma das {len(seen)} soluções encontradas gerou uma planta válida (acesso ou geometria). "
                              "Tente mais tempo de busca (--time-limit) ou revise o programa.")
    return accepted


def _no_fit_message(request: Request, catalog: Catalog) -> str:
    site, sb = request.site, request.site.setbacks
    buildable = (site.width_mm - sb.left - sb.right) * (site.depth_mm - sb.front - sb.back) / 1e6
    needed = 0.0  # o gerador exige de cada cômodo o maior entre o mínimo do tipo e 0,7 x a área-alvo
    for r in request.rooms:
        target = room_target_m2(r, catalog)
        needed += max(catalog.get(r.type).min_area_m2 or 0, MIN_TARGET_FACTOR * target if target else 0)
    return (f"Nenhuma planta coube no terreno: os mínimos e as áreas pedidas somam ≈ {needed:.1f} m² de área útil "
            f"(cada cômodo com pelo menos {MIN_TARGET_FACTOR:.0%} do alvo), a área edificável (terreno menos "
            f"recuos) é ≈ {buildable:.1f} m², e as larguras mínimas e passagens também precisam caber. "
            "Tente menos cômodos, áreas menores, recuos menores ou mais tempo de busca.")
