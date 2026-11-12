"""Diversidade entre plantas pelo padrão de posições relativas (design 9)."""

from pygridplan.model.plan import Plan

# por par (i, j): (i à esquerda de j, à direita, à frente, atrás)
Pattern = dict[tuple[str, str], tuple[bool, bool, bool, bool]]


def relative_pattern(plan: Plan) -> Pattern:
    rooms = plan.rooms
    return {
        (a.id, b.id): (a.rect.x2 <= b.rect.x, b.rect.x2 <= a.rect.x, a.rect.y2 <= b.rect.y, b.rect.y2 <= a.rect.y)
        for i, a in enumerate(rooms)
        for b in rooms[i + 1 :]
    }


def plan_distance(a: Plan, b: Plan) -> float:
    """Fração de pares cuja posição relativa mudou de verdade: nenhuma relação que valia
    numa planta vale na outra (estar "à direita e também atrás" não difere de "à direita")."""
    pa, pb = relative_pattern(a), relative_pattern(b)
    if pa.keys() != pb.keys():
        raise ValueError("as plantas não têm os mesmos cômodos na mesma ordem")
    differs = sum(not any(x and y for x, y in zip(pa[k], pb[k])) for k in pa)
    return differs / len(pa) if pa else 0.0
