"""SVG autocontido de uma planta (frente do terreno embaixo, como no DXF)."""

from html import escape

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan
from pygridplan.model.site_defaults import SiteDefaults, load_site_defaults
from pygridplan.model.walls import useful_area_mm2

# fonte única das 4 categorias de cor (design 20.1, item 7): (cor SVG, cor ACI do DXF, rótulo)
CATEGORY_STYLE = {
    "dry": ("#d97757", 30, "Interna seca"),
    "wet": ("#5fa8d3", 150, "Interna molhada"),
    "built": ("#8a8a80", 8, "Externa construída"),
    "green": ("#6fae7a", 3, "Externa verde"),
}
FENCE_FILL = "#5c5c55"


def plan_to_svg(plan: Plan, catalog: Catalog, defaults: SiteDefaults | None = None) -> str:
    fence = (defaults or load_site_defaults()).fence_thickness_mm
    w, d = plan.site.width_mm, plan.site.depth_mm
    pad = 500
    font = max(w, d) / 60

    def y(v: float) -> float:  # inverte o eixo y: frente (y = 0) embaixo
        return d - v

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {d + 2 * pad}" '
        f'preserveAspectRatio="xMidYMid meet">',
        f'<rect x="0" y="0" width="{w}" height="{d}" fill="{FENCE_FILL}"/>',  # muro: faixa entre os dois retângulos
        f'<rect x="{fence}" y="{fence}" width="{w - 2 * fence}" height="{d - 2 * fence}" fill="{CATEGORY_STYLE["green"][0]}" '
        f'fill-opacity="0.25"/>',
    ]
    for room in plan.rooms:
        r, kind = room.rect, catalog.get(room.type)
        area = f"{useful_area_mm2(room, plan) / 1e6:.2f}".replace(".", ",")
        parts.append(
            f'<rect x="{r.x}" y="{y(r.y2)}" width="{r.w}" height="{r.h}" fill="{CATEGORY_STYLE[kind.category][0]}" '
            f'fill-opacity="0.55" stroke="#ecebe6" stroke-width="{font / 6}"/>'
        )
        cx, cy = r.x + r.w / 2, y(r.y + r.h / 2)
        parts.append(
            f'<text x="{cx}" y="{cy}" font-size="{font}" fill="#ecebe6" text-anchor="middle" '
            f'font-family="system-ui, sans-serif">{escape(kind.name)}'
            f'<tspan x="{cx}" dy="{font * 1.2}">{area} m²</tspan></text>'
        )
    parts.append("</svg>")
    return "".join(parts)
