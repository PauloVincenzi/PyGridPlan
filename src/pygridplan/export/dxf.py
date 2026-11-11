"""Exportação da planta para DXF (mm, layers do MVP)."""

from pathlib import Path

from ezdxf import units
from ezdxf.enums import TextEntityAlignment
from ezdxf.filemanagement import new as new_drawing

from pygridplan.model.catalog import Catalog
from pygridplan.model.plan import Plan
from pygridplan.model.walls import Wall, derive_walls, useful_area_mm2, useful_bounds

LAYERS = (
    "A-TERRENO", "A-EIXOS", "A-PAREDES-EXT", "A-PAREDES-INT", "A-PORTAS", "A-JANELAS",
    "A-MOBILIARIO", "A-COTAS", "A-TEXTOS", "A-AREAS", "A-AVISOS",
)
LAYER_COLORS = {"A-EIXOS": 1, "A-PAREDES-INT": 8, "A-AREAS": 9}  # ACI: vermelho, cinza, cinza claro; demais 7
AXIS_LINETYPE = "CENTER"
LTSCALE = 50  # traço-ponto legível em desenho em mm
DIM_OFFSET_MM = 1000
DIM_STYLE = {"dimtxt": 250, "dimasz": 200, "dimexe": 100, "dimexo": 100}
BYLAYER = 256


def _box(x1: float, y1: float, x2: float, y2: float) -> list[tuple[float, float]]:
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def _end_extension(w: Wall, x: int, y: int, walls: list[Wall]) -> float:
    """Meia espessura da parede perpendicular mais grossa que passa pela ponta (x, y):
    estender a faixa até ali fecha quinas e encontros em T."""
    horizontal = w.y1 == w.y2
    halves = [
        o.thickness_mm / 2
        for o in walls
        if (o.y1 == o.y2) != horizontal
        and (o.x1 == x and o.y1 <= y <= o.y2 if horizontal else o.y1 == y and o.x1 <= x <= o.x2)
    ]
    return max(halves, default=0)


def _wall_band(w: Wall, walls: list[Wall]) -> list[tuple[float, float]]:
    """Faixa de largura `thickness_mm` centrada no eixo, estendida nas pontas."""
    h = w.thickness_mm / 2
    a = _end_extension(w, w.x1, w.y1, walls)
    b = _end_extension(w, w.x2, w.y2, walls)
    if w.y1 == w.y2:
        return _box(w.x1 - a, w.y1 - h, w.x2 + b, w.y1 + h)
    return _box(w.x1 - h, w.y1 - a, w.x1 + h, w.y2 + b)


def export_dxf(plan: Plan, path: Path, catalog: Catalog) -> None:
    doc = new_drawing("R2010", setup=["linetypes"])
    doc.units = units.MM
    doc.header["$LTSCALE"] = LTSCALE
    doc.styles.get("Standard").dxf.font = "arial.ttf"  # SHX padrão (txt) não tem "²" nem acentos
    for name in LAYERS:
        doc.layers.add(name, color=LAYER_COLORS.get(name, 7))
    doc.layers.get("A-EIXOS").dxf.linetype = AXIS_LINETYPE
    msp = doc.modelspace()
    width, depth = plan.site.width_mm, plan.site.depth_mm

    msp.add_lwpolyline(_box(0, 0, width, depth), close=True, dxfattribs={"layer": "A-TERRENO"})
    walls = derive_walls(plan)
    for w in walls:
        layer = "A-PAREDES-EXT" if w.kind == "ext" else "A-PAREDES-INT"
        hatch = msp.add_hatch(color=BYLAYER, dxfattribs={"layer": layer})
        hatch.paths.add_polyline_path(_wall_band(w, walls), is_closed=True)
        msp.add_line((w.x1, w.y1), (w.x2, w.y2), dxfattribs={"layer": "A-EIXOS"})
    for room in plan.rooms:
        r = room.rect
        msp.add_lwpolyline(_box(*useful_bounds(room, plan)), close=True, dxfattribs={"layer": "A-AREAS"})
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
