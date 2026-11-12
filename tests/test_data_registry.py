"""Qualidade dos dados de referência: toda citação em data/ aponta para uma fonte registrada."""

from pathlib import Path

import yaml

from pygridplan.model.sources import DATA_DIR, load_sources


def _cited_ids(node):
    """IDs citados em qualquer chave `source` (str) ou `sources` (dict campo -> id)."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "source" and isinstance(value, str):
                yield value
            elif key == "sources" and isinstance(value, dict):
                yield from value.values()
            else:
                yield from _cited_ids(value)
    elif isinstance(node, list):
        for item in node:
            yield from _cited_ids(item)


def test_sources_registry_loads():
    sources = load_sources()
    assert "nbr15575-1-anexo" in sources
    assert sources["codigo-civil"].kind == "L-fed"


def test_every_citation_in_data_is_registered():
    known = set(load_sources())
    files = [p for p in Path(DATA_DIR).rglob("*.yaml") if p.name != "sources.yaml"]
    assert files
    for path in files:
        cited = set(_cited_ids(yaml.safe_load(path.read_text(encoding="utf-8"))))
        assert cited <= known, f"{path.name}: fontes não registradas {cited - known}"
