"""Checagens de implantação no lote: janelas junto à divisa (CC art. 1.301) e permeabilidade."""

from pygridplan.model.plan import Plan
from pygridplan.model.site_defaults import SiteDefaults
from pygridplan.model.walls import exterior_sides
from pygridplan.validation.checks import Issue

SIDE_NAME = {"left": "esquerdo", "right": "direito", "front": "frontal", "back": "dos fundos"}


def _m(v: float) -> str:
    return f"{v / 1000:.2f}".replace(".", ",") + " m"


def fence_area_mm2(plan: Plan, defaults: SiteDefaults) -> int:
    w, d, t = plan.site.width_mm, plan.site.depth_mm, defaults.fence_thickness_mm
    return w * d - (w - 2 * t) * (d - 2 * t)


def green_area_mm2(plan: Plan, defaults: SiteDefaults) -> int:
    """Lote menos muro menos cômodos (inclusive os externos construídos)."""
    lot = plan.site.width_mm * plan.site.depth_mm
    return lot - fence_area_mm2(plan, defaults) - sum(r.rect.area_mm2 for r in plan.rooms)


def check_site(plan: Plan, defaults: SiteDefaults) -> list[Issue]:
    issues: list[Issue] = []
    ratio = green_area_mm2(plan, defaults) / (plan.site.width_mm * plan.site.depth_mm)
    if ratio < defaults.permeability_min:
        issues.append(Issue(
            code="permeability", recommended=defaults.permeability_min, actual=round(ratio, 3),
            message=f"área verde {ratio:.0%} < {defaults.permeability_min:.0%} (referência de Curitiba, "
                    "Lei 15.511/2019; confira a lei do seu município)".replace("%", " %"),
        ))
    e, w, d = plan.wall_ext_mm // 2, plan.site.width_mm, plan.site.depth_mm
    for room in plan.rooms:
        r = room.rect
        distance = {"left": r.x - e, "right": w - r.x2 - e, "front": r.y - e, "back": d - r.y2 - e}
        for side in sorted(exterior_sides(room, plan)):
            if distance[side] < defaults.window_min_distance_mm:
                issues.append(Issue(
                    code="no_window", room_ids=(room.id,),
                    message=f"{room.id}: lado {SIDE_NAME[side]} a {_m(distance[side])} da divisa — "
                            "sem janela (Código Civil, art. 1.301)",
                    recommended=defaults.window_min_distance_mm, actual=distance[side],
                ))
    return issues
