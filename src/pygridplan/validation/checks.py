"""Validação da planta: erros de validade (inegociáveis) e avisos de recomendação."""

from pydantic import BaseModel, ConfigDict

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan, Rect
from pygridplan.model.walls import useful_area_mm2, useful_dims_mm


class Issue(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    message: str
    room_ids: tuple[str, ...] = ()
    recommended: float | None = None
    actual: float | None = None


def _mm(v: float) -> str:
    return f"{v:,.0f}".replace(",", " ") + " mm"


def validate_geometry(plan: Plan) -> list[Issue]:
    issues: list[Issue] = []
    rooms = plan.rooms
    for i, a in enumerate(rooms):
        for b in rooms[i + 1 :]:
            if a.rect.overlaps_interior(b.rect):
                issues.append(Issue(code="overlap", message=f"{a.id} e {b.id} se sobrepõem",
                                    room_ids=(a.id, b.id)))
    lot = Rect(x=0, y=0, w=plan.site.width_mm, h=plan.site.depth_mm)
    for r in rooms:
        if not lot.contains(r.rect.expanded(plan.wall_ext_mm // 2)):
            issues.append(Issue(code="outside_lot", message=f"{r.id}: paredes fora do terreno",
                                room_ids=(r.id,)))
    return issues


def _setback_issues(plan: Plan) -> list[Issue]:
    site, sb = plan.site, plan.site.setbacks
    issues: list[Issue] = []
    for r in plan.rooms:
        e = r.rect.expanded(plan.wall_ext_mm // 2)
        distances = {  # lado: (distância até a divisa, recuo recomendado, pode encostar?)
            "frente": (e.y, sb.front, False),
            "fundo": (site.depth_mm - e.y2, sb.back, "back" in site.attached_sides),
            "esquerda": (e.x, sb.left, "left" in site.attached_sides),
            "direita": (site.width_mm - e.x2, sb.right, "right" in site.attached_sides),
        }
        for side, (dist, required, attached) in distances.items():
            if not attached and dist < required:
                issues.append(Issue(
                    code="setback",
                    message=f"{r.id}: recuo {side} {_mm(dist)} < {_mm(required)} recomendados",
                    room_ids=(r.id,), recommended=required, actual=dist,
                ))
    return issues


def check_recommendations(plan: Plan, catalog: Catalog) -> list[Issue]:
    issues = _setback_issues(plan)
    for r in plan.rooms:
        t = catalog.get(r.type)
        width = min(useful_dims_mm(r, plan))
        if t.min_width_mm is not None and width < t.min_width_mm:
            issues.append(Issue(
                code="min_width",
                message=f"{r.id}: largura útil {_mm(width)} < {_mm(t.min_width_mm)} recomendados",
                room_ids=(r.id,), recommended=t.min_width_mm, actual=width,
            ))
        area = useful_area_mm2(r, plan) / 1e6
        if t.min_area_m2 is not None and area < t.min_area_m2:
            issues.append(Issue(
                code="min_area",
                message=f"{r.id}: área útil {area:.2f} m² < {t.min_area_m2:.2f} m² recomendados",
                room_ids=(r.id,), recommended=t.min_area_m2, actual=round(area, 2),
            ))
    return issues
