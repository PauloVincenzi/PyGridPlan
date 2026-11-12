import pytest

from pygridplan.model.site_defaults import load_site_defaults


def test_site_defaults_load():
    d = load_site_defaults()
    assert d.fence_thickness_mm == 150
    assert d.window_min_distance_mm == 1500
    assert d.permeability_min == 0.25


def test_site_default_without_source_rejected(tmp_path):
    path = tmp_path / "s.yaml"
    path.write_text("fence_thickness_mm: 150\nwindow_min_distance_mm: 1500\npermeability_min: 0.25\n"
                    "sources: {fence_thickness_mm: agente, window_min_distance_mm: codigo-civil}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="sem fonte"):
        load_site_defaults(path)
