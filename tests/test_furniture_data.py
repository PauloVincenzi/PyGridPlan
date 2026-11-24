"""Registro do mobiliário (trilha D2 → M1.2): todo número de data/furniture.yaml tem fonte, e toda referência existe.

A citação em si (id registrado em sources.yaml) já é conferida por test_data_registry.py.
"""

import yaml

from pygridplan.model.catalog import load_catalog
from pygridplan.model.sources import DATA_DIR

FURNITURE = yaml.safe_load((DATA_DIR / "furniture.yaml").read_text(encoding="utf-8"))
MEASURE_KEYS = {"w", "d", "mm"}  # toda medida é um mapa com uma destas chaves e uma `source`
PROFILES = FURNITURE["profiles"]


def _measures(node, path="furniture"):
    if isinstance(node, dict):
        if MEASURE_KEYS & node.keys():
            yield path, node
        for key, value in node.items():
            yield from _measures(value, f"{path}.{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _measures(value, f"{path}[{i}]")


def test_every_measure_is_a_positive_integer_with_a_real_source():
    measures = list(_measures(FURNITURE))
    assert len(measures) > 50
    for path, m in measures:
        assert m.get("source"), f"{path}: medida sem fonte"
        assert m["source"] != "agente", f"{path}: a D2 só promove valor com fonte externa"
        for key in MEASURE_KEYS & m.keys():
            assert isinstance(m[key], int) and m[key] > 0, f"{path}.{key}: precisa ser inteiro positivo (mm)"


def test_profiles_fall_back_without_cycles_to_the_base_profile():
    assert FURNITURE["default_profile"] in PROFILES
    for name in PROFILES:
        seen, current = [], name
        while current is not None:
            assert current in PROFILES, f"{name}: fallback para perfil desconhecido {current}"
            assert current not in seen, f"{name}: ciclo de fallback {seen}"
            seen.append(current)
            current = PROFILES[current].get("fallback")
        assert seen[-1] == "nbr", f"{name}: a cadeia deve terminar no perfil-base nbr"


def test_profile_keyed_values_use_known_profiles():
    for cid, by_profile in FURNITURE["clearances"].items():
        assert by_profile and set(by_profile) <= set(PROFILES), f"folga {cid}"
    for type_id, by_profile in FURNITURE["room_min_width"].items():
        assert set(by_profile) <= set(PROFILES), f"largura de {type_id}"
    for iid, item in FURNITURE["items"].items():
        assert set(item.get("by_profile", {})) <= set(PROFILES), f"item {iid}"


def test_items_have_a_footprint_and_zones_point_to_known_clearances():
    clearances = set(FURNITURE["clearances"])
    for iid, item in FURNITURE["items"].items():
        assert {"w", "d"} <= item["footprint"].keys(), f"{iid}: sem dimensão física"
        for side, cid in item.get("zones", {}).items():
            assert side in {"front", "back", "left", "right", "side"}, f"{iid}: lado {side}"
            assert cid in clearances, f"{iid}: folga desconhecida {cid}"
        if "paired_side" in item:
            assert item["paired_side"] in clearances


def test_room_sets_use_known_items_and_room_types_with_one_default_each():
    items, types = set(FURNITURE["items"]), set(load_catalog().types)
    defaults: dict[str, str] = {}
    for sid, room_set in FURNITURE["room_sets"].items():
        assert room_set["type"] in types, f"{sid}: tipo de cômodo desconhecido"
        assert room_set["items"] and set(room_set["items"]) <= items, f"{sid}: item desconhecido"
        if room_set.get("default"):
            assert room_set["type"] not in defaults, f"dois conjuntos padrão para {room_set['type']}"
            defaults[room_set["type"]] = sid
    assert set(FURNITURE["room_min_width"]) <= types
    for zone in PROFILES["mcmv"].get("free_zones", {}).values():
        assert set(zone.get("rooms", [])) | set(zone.get("rooms_except", [])) <= types


def test_two_profiles_disagree_where_the_sources_disagree():
    """Âncoras da D2: cama de solteiro e folga entre camas do MCMV maiores que as da NBR."""
    bed = FURNITURE["items"]["cama_solteiro"]
    assert bed["footprint"]["w"] == 800 and bed["by_profile"]["mcmv"]["w"] == 900
    between = FURNITURE["clearances"]["entre_camas"]
    assert between["nbr"]["mm"] == 600 and between["mcmv"]["mm"] == 800
