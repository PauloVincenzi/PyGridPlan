import ezdxf
import pytest

from conftest import BASIC_HOUSE
from pygridplan.__main__ import main
from pygridplan.export.dxf import LAYERS, export_dxf
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import Plan, Site


@pytest.fixture
def doc(basic_house, tmp_path):
    path = tmp_path / "p.dxf"
    export_dxf(basic_house, path, load_catalog())
    return ezdxf.readfile(path)


def test_all_layers_exist(doc):
    assert all(name in doc.layers for name in LAYERS)


def test_units_are_mm(doc):
    assert doc.header["$INSUNITS"] == 4


def test_lot_outline(doc):
    lots = doc.modelspace().query("LWPOLYLINE[layer=='A-TERRENO']")
    assert len(lots) == 1
    assert lots[0].closed
    assert [(p[0], p[1]) for p in lots[0].get_points()] == [(0, 0), (10000, 0), (10000, 25000), (0, 25000)]


def _hatch_boxes(doc, layer):
    """Caixas (xmin, ymin, xmax, ymax) das hachuras de um layer."""
    boxes = []
    for h in doc.modelspace().query(f"HATCH[layer=='{layer}']"):
        xs, ys = zip(*[(v[0], v[1]) for v in h.paths.paths[0].vertices])
        boxes.append((min(xs), min(ys), max(xs), max(ys)))
    return boxes


def _covered(boxes, x, y):
    return any(x0 < x < x1 and y0 < y < y1 for x0, y0, x1, y1 in boxes)


def test_walls_are_solid_hatches(doc):
    assert len(_hatch_boxes(doc, "A-PAREDES-EXT")) == 11
    assert len(_hatch_boxes(doc, "A-PAREDES-INT")) == 11
    assert len(doc.modelspace().query("LWPOLYLINE[layer=='A-PAREDES-EXT']")) == 0


def test_wall_corners_are_closed(doc):
    ext = _hatch_boxes(doc, "A-PAREDES-EXT")
    assert _covered(ext, 1530, 4030)  # quina externa frente-esquerda (eixo em 1600, 4100)
    assert _covered(ext, 8470, 14170)  # quina externa fundo-direita (eixo em 8400, 14100)
    walls = ext + _hatch_boxes(doc, "A-PAREDES-INT")
    assert _covered(walls, 5600, 8100)  # encontro em T sala/cozinha/circulação


def test_axes_layer_has_its_own_color(doc):
    assert len(doc.modelspace().query("LINE[layer=='A-EIXOS']")) == 22
    axis_color = doc.layers.get("A-EIXOS").color
    assert axis_color not in {doc.layers.get(n).color for n in ("A-PAREDES-EXT", "A-PAREDES-INT")}


def test_area_outline_is_useful_rectangle(doc):
    areas = [[(p[0], p[1]) for p in pl.get_points()] for pl in doc.modelspace().query("LWPOLYLINE[layer=='A-AREAS']")]
    assert [(1675, 4175), (5550, 4175), (5550, 8050), (1675, 8050)] in areas  # sala: 3875 x 3875


def test_room_texts(doc):
    texts = [t.dxf.text for t in doc.modelspace().query("TEXT[layer=='A-TEXTOS']")]
    assert len(texts) == 7
    assert "Sala de estar 15,02 m²" in texts


def test_lot_dimensions(doc):
    dims = doc.modelspace().query("DIMENSION[layer=='A-COTAS']")
    assert len(dims) == 2
    assert {round(d.get_measurement()) for d in dims} == {10000, 25000}


def test_empty_plan_exports_lot_only(tmp_path):
    path = tmp_path / "e.dxf"
    export_dxf(Plan(site=Site(width_mm=5000, depth_mm=5000)), path, load_catalog())
    msp = ezdxf.readfile(path).modelspace()
    for layer in ("A-PAREDES-EXT", "A-PAREDES-INT", "A-TEXTOS"):
        assert len(msp.query(f"*[layer=='{layer}']")) == 0


def test_cli_exports_file(tmp_path):
    out = tmp_path / "x" / "p.dxf"
    assert main(["export-dxf", str(BASIC_HOUSE), str(out)]) == 0
    assert out.exists()


def test_text_style_uses_truetype_font(doc):
    # fonte SHX padrão (txt) não tem "²" nem acentos
    assert doc.styles.get("Standard").dxf.font.lower().endswith(".ttf")
