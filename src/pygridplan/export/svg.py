"""SVG autocontido de uma planta (frente do terreno embaixo, como no DXF)."""

from html import escape

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan
from pygridplan.model.walls import useful_area_mm2

ZONE_FILL = {"social": "#d97757", "intima": "#9b87f5", "servico": "#8a8a80"}  # paleta do projeto (DEC-0013)


def plan_to_svg(plan: Plan, catalog: Catalog) -> str:
    w, d = plan.site.width_mm, plan.site.depth_mm
    pad = 500
    font = max(w, d) / 60

    def y(v: float) -> float:  # inverte o eixo y: frente (y = 0) embaixo
        return d - v

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {d + 2 * pad}" '
        f'preserveAspectRatio="xMidYMid meet">',
        f'<rect x="0" y="0" width="{w}" height="{d}" fill="none" stroke="#5c5c55" '
        f'stroke-width="{font / 8}" stroke-dasharray="{font} {font / 2}"/>',
    ]
    for room in plan.rooms:
        r, t = room.rect, catalog.get(room.type)
        area = f"{useful_area_mm2(room, plan) / 1e6:.2f}".replace(".", ",")
        parts.append(
            f'<rect x="{r.x}" y="{y(r.y2)}" width="{r.w}" height="{r.h}" fill="{ZONE_FILL[t.zone]}" '
            f'fill-opacity="0.35" stroke="#ecebe6" stroke-width="{font / 6}"/>'
        )
        cx, cy = r.x + r.w / 2, y(r.y + r.h / 2)
        parts.append(
            f'<text x="{cx}" y="{cy}" font-size="{font}" fill="#ecebe6" text-anchor="middle" '
            f'font-family="system-ui, sans-serif">{escape(t.name)}'
            f'<tspan x="{cx}" dy="{font * 1.2}">{area} m²</tspan></text>'
        )
    parts.append("</svg>")
    return "".join(parts)
