import pytest
from pydantic import ValidationError

from pygridplan.model.catalog import load_catalog


def test_default_catalog_loads():
    catalog = load_catalog()
    assert len(catalog.types) == 12
    assert catalog.version == "0.1"


def test_private_types():
    types = load_catalog().types.values()
    assert {t.id for t in types if t.passage == "private"} == {
        "quarto",
        "banheiro",
        "lavabo",
        "closet",
    }


def test_unknown_type_is_traversable_without_minimums():
    t = load_catalog().get("quadra_de_areia")
    assert t.passage == "traversable"
    assert t.min_width_mm is None
    assert t.min_area_m2 is None


def test_every_type_has_source():
    assert all(t.source for t in load_catalog().types.values())


def test_invalid_zone_is_rejected(tmp_path):
    path = tmp_path / "c.yaml"
    path.write_text(
        'version: "x"\nupdated: "x"\ntypes:\n'
        "  - {id: a, name: A, zone: x, passage: private, source: s}\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError):
        load_catalog(path)
