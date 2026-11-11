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


def test_wall_entities_per_layer(doc):
    msp = doc.modelspace()
    assert len(msp.query("LWPOLYLINE[layer=='A-PAREDES-EXT']")) == 11
    assert len(msp.query("LWPOLYLINE[layer=='A-PAREDES-INT']")) == 11


def test_room_texts(doc):
    texts = [t.dxf.text for t in doc.modelspace().query("TEXT[layer=='A-TEXTOS']")]
    assert len(texts) == 7
    assert "Sala 15,02 m²" in texts


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
