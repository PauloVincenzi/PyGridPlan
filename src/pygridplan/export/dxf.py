"""Exportação da planta para DXF (mm, layers do MVP)."""

from pathlib import Path

from ezdxf import units
from ezdxf.enums import TextEntityAlignment
from ezdxf.filemanagement import new as new_drawing

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan
from pygridplan.model.walls import Wall, derive_walls, useful_area_mm2

LAYERS = (
    "A-TERRENO", "A-PAREDES-EXT", "A-PAREDES-INT", "A-PORTAS", "A-JANELAS",
    "A-MOBILIARIO", "A-COTAS", "A-TEXTOS", "A-AREAS", "A-AVISOS",
)
DIM_OFFSET_MM = 1000
DIM_STYLE = {"dimtxt": 250, "dimasz": 200, "dimexe": 100, "dimexo": 100}


def _box(x1: float, y1: float, x2: float, y2: float) -> list[tuple[float, float]]:
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def _wall_band(w: Wall) -> list[tuple[float, float]]:
    """Faixa de largura `thickness_mm` centrada no eixo da parede."""
    h = w.thickness_mm / 2
    if w.y1 == w.y2:
        return _box(w.x1, w.y1 - h, w.x2, w.y1 + h)
    return _box(w.x1 - h, w.y1, w.x1 + h, w.y2)


def export_dxf(plan: Plan, path: Path, catalog: Catalog) -> None:
    doc = new_drawing("R2010")
    doc.units = units.MM
    for name in LAYERS:
        doc.layers.add(name)
    msp = doc.modelspace()
    width, depth = plan.site.width_mm, plan.site.depth_mm

    msp.add_lwpolyline(_box(0, 0, width, depth), close=True, dxfattribs={"layer": "A-TERRENO"})
    for w in derive_walls(plan):
        layer = "A-PAREDES-EXT" if w.kind == "ext" else "A-PAREDES-INT"
        msp.add_lwpolyline(_wall_band(w), close=True, dxfattribs={"layer": layer})
    for room in plan.rooms:
        r = room.rect
        msp.add_lwpolyline(_box(r.x, r.y, r.x2, r.y2), close=True, dxfattribs={"layer": "A-AREAS"})
        area = f"{useful_area_mm2(room, plan) / 1e6:.2f}".replace(".", ",")
        text = msp.add_text(f"{catalog.get(room.type).name} {area} m²", height=200,
                            dxfattribs={"layer": "A-TEXTOS"})
        text.set_placement((r.x + r.w / 2, r.y + r.h / 2), align=TextEntityAlignment.MIDDLE_CENTER)

    cotas = {"layer": "A-COTAS"}
    msp.add_linear_dim(base=(0, -DIM_OFFSET_MM), p1=(0, 0), p2=(width, 0), angle=0,
                       override=DIM_STYLE, dxfattribs=cotas).render()
    msp.add_linear_dim(base=(-DIM_OFFSET_MM, 0), p1=(0, 0), p2=(0, depth), angle=90,
                       override=DIM_STYLE, dxfattribs=cotas).render()
    doc.saveas(path)
