import pytest
from pydantic import ValidationError

from pygridplan.model.catalog import load_catalog

HEADER = 'version: "x"\nupdated: "x"\ntypes:\n'


def _write(tmp_path, body):
    path = tmp_path / "c.yaml"
    path.write_text(HEADER + body, encoding="utf-8")
    return path


def test_default_catalog_loads():
    catalog = load_catalog()
    assert catalog.version == "0.3"
    assert {"sala", "cozinha", "quarto", "banheiro", "closet", "circulacao", "lavanderia"} <= set(catalog.types)


def test_private_types():
    types = load_catalog().types.values()
    assert {t.id for t in types if t.passage == "private"} == {
        "quarto", "quarto_solteiro", "banheiro", "lavabo", "closet", "rouparia", "despensa", "deposito",
    }


def test_suite_access_and_flags():
    c = load_catalog()
    assert c.get("quarto").suite_access == ("closet", "banheiro")
    assert c.get("closet").suite_access == ("banheiro",)
    assert c.get("banheiro").wet and c.get("cozinha").wet and not c.get("sala").wet
    assert c.get("sala").sun and c.get("quarto").sun and not c.get("banheiro").sun


def test_unknown_type_is_traversable_without_minimums():
    t = load_catalog().get("quadra_de_areia")
    assert t.passage == "traversable"
    assert t.min_width_mm is None
    assert t.min_area_m2 is None


def test_every_value_has_a_registered_source():
    # DEC-0024: todo valor numérico tem fonte; load_catalog já valida, aqui fixamos o contrato
    for t in load_catalog().types.values():
        for field in ("min_width_mm", "min_area_m2", "comfort_area_m2"):
            if getattr(t, field) is not None:
                assert field in t.sources, f"{t.id}.{field} sem fonte"


def test_value_without_source_rejected(tmp_path):
    path = _write(tmp_path, "  - {id: a, name: A, zone: social, passage: traversable, min_width_mm: 900}\n")
    with pytest.raises(ValueError, match="sem fonte"):
        load_catalog(path)


def test_unknown_source_rejected(tmp_path):
    path = _write(tmp_path, "  - {id: a, name: A, zone: social, passage: traversable, min_width_mm: 900,"
                            " sources: {min_width_mm: fonte-inexistente}}\n")
    with pytest.raises(ValueError, match="fonte-inexistente"):
        load_catalog(path)


def test_comfort_range_must_be_ordered(tmp_path):
    path = _write(tmp_path, "  - {id: a, name: A, zone: social, passage: traversable, comfort_area_m2: [12, 10],"
                            " sources: {comfort_area_m2: agente}}\n")
    with pytest.raises(ValidationError):
        load_catalog(path)


def test_invalid_zone_is_rejected(tmp_path):
    path = _write(tmp_path, "  - {id: a, name: A, zone: x, passage: private}\n")
    with pytest.raises(ValidationError):
        load_catalog(path)


def test_unknown_catalog_key_is_rejected(tmp_path):
    path = _write(tmp_path, "  - {id: a, name: A, zone: social, passage: private, min_widht_mm: 900}\n")
    with pytest.raises(ValidationError):
        load_catalog(path)


def test_duplicate_catalog_ids_rejected(tmp_path):
    path = _write(tmp_path, "  - {id: a, name: A, zone: social, passage: private}\n"
                            "  - {id: a, name: B, zone: social, passage: private}\n")
    with pytest.raises(ValueError, match="duplicado"):
        load_catalog(path)


def test_no_municipal_or_state_law_as_national_default():
    # data/README.md regra 4: lei municipal ou estadual nunca vira padrão nacional
    from pygridplan.model.sources import load_sources

    kinds = {k: s.kind for k, s in load_sources().items()}
    for t in load_catalog().types.values():
        for field in ("min_width_mm", "min_area_m2"):
            if getattr(t, field) is not None:
                assert kinds[t.sources[field]] not in ("L-mun", "L-est"), f"{t.id}.{field}"


def test_comfort_range_not_below_minimum():
    for t in load_catalog().types.values():
        if t.comfort_area_m2 and t.min_area_m2:
            assert t.comfort_area_m2[0] >= t.min_area_m2, t.id


def test_patio_is_exterior():
    assert load_catalog().get("patio").exterior


def test_window_need_follows_sources():
    # design 22.2 (revisto na S06): janela obrigatória só com fonte federal; o resto é preferência
    c = load_catalog()
    assert c.get("sala").window_need == "required" and c.get("quarto").window_need == "required"
    assert c.get("banheiro").window_need == "preferred" and c.get("lavabo").window_need == "preferred"
    assert c.get("closet").window_need is None and c.get("circulacao").window_need is None


def test_access_hub_ranks_living_rooms_over_kitchen():
    # design 22.1 (revisto na S06): chegar à circulação pela sala é o natural; pela cozinha, aceitável
    c = load_catalog()
    assert c.get("sala").access_hub == 1.0 and c.get("cozinha").access_hub == 0.5
    assert c.get("lavanderia").access_hub is None
