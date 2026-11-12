"""Acesso potencial antes das portas: entrada pela frente e alcançabilidade (design 5.1, 5.5)."""

from collections import deque

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan
from pygridplan.model.walls import derive_walls
from pygridplan.validation.checks import Issue

MIN_PASSAGE_MM = 900  # parede comum mínima para caber uma porta com folga


def passages(plan: Plan) -> dict[tuple[str, str], int]:
    """Comprimento total de parede interna compartilhada por par (ordem de `plan.rooms`)."""
    shared: dict[tuple[str, str], int] = {}
    for w in derive_walls(plan):
        if w.kind == "int":
            a, b = w.room_ids
            shared[(a, b)] = shared.get((a, b), 0) + abs(w.x2 - w.x1) + abs(w.y2 - w.y1)
    return shared


def check_access(plan: Plan, catalog: Catalog) -> list[Issue]:
    if not plan.rooms:
        return []
    types = {r.id: catalog.get(r.type) for r in plan.rooms}
    neighbors: dict[str, set[str]] = {r.id: set() for r in plan.rooms}
    for (a, b), length in passages(plan).items():
        if length >= MIN_PASSAGE_MM:
            neighbors[a].add(b)
            neighbors[b].add(a)

    front = min(r.rect.y for r in plan.rooms)
    entrances = [r.id for r in plan.rooms if r.rect.y == front and types[r.id].passage == "traversable"]
    issues: list[Issue] = []
    if not entrances:
        issues.append(Issue(code="no_entrance", message="nenhum cômodo atravessável na frente da casa"))

    # entra-se em qualquer vizinho; sai-se de um atravessável para qualquer um,
    # e de um privativo só para os tipos do seu suite_access (quarto -> closet -> banheiro)
    reached, queue = set(entrances), deque(entrances)
    while queue:
        here = types[current := queue.popleft()]
        for nxt in neighbors[current] - reached:
            if here.passage == "traversable" or types[nxt].id in here.suite_access:
                reached.add(nxt)
                queue.append(nxt)

    for r in plan.rooms:
        if r.id not in reached:
            issues.append(Issue(code="unreachable", message=f"{r.id}: sem acesso a partir da entrada",
                                room_ids=(r.id,)))
    return issues
