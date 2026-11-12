"""Catálogo de tipos de cômodo: fonte única de zona, passagem, atributos e mínimos."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, model_validator

from pygridplan.model.sources import DATA_DIR, DEFAULT_SOURCES_PATH, load_sources

DEFAULT_CATALOG_PATH = DATA_DIR / "room_types.yaml"
SOURCED_FIELDS = ("min_width_mm", "min_area_m2", "comfort_area_m2")


class RoomType(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    name: str
    description: str = ""
    zone: Literal["social", "intima", "servico"]
    passage: Literal["private", "traversable"]
    suite_access: tuple[str, ...] = ()  # tipos privativos alcançáveis através deste (design 5.5)
    wet: bool = False  # área molhada
    sun: bool = False  # prefere fachada norte/leste
    exterior: bool = False  # fora do envelope fechado (varanda, abrigo, gourmet)
    concentrated_use: bool = False  # atravessar custa mais (design 5.5)
    stay: Literal["prolonged", "transient"] | None = None  # permanência (iluminação/ventilação)
    min_width_mm: int | None = None
    min_area_m2: float | None = None
    comfort_area_m2: tuple[float, float] | None = None
    sources: dict[str, str] = {}  # campo -> id em data/sources.yaml

    @model_validator(mode="after")
    def _comfort_ordered(self) -> "RoomType":
        if self.comfort_area_m2 and self.comfort_area_m2[0] > self.comfort_area_m2[1]:
            raise ValueError(f"{self.id}: faixa de conforto invertida")
        return self


class Catalog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str
    updated: str
    types: dict[str, RoomType]

    def get(self, type_id: str) -> RoomType:
        """Tipo desconhecido vira um tipo personalizado atravessável e sem mínimos."""
        return self.types.get(type_id) or RoomType(
            id=type_id, name=type_id, zone="social", passage="traversable"
        )


def load_catalog(path: Path = DEFAULT_CATALOG_PATH, sources_path: Path = DEFAULT_SOURCES_PATH) -> Catalog:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    types: dict[str, dict] = {}
    for t in raw["types"]:
        if t["id"] in types:
            raise ValueError(f"ID de tipo duplicado no catálogo: {t['id']}")
        types[t["id"]] = t
    catalog = Catalog.model_validate({**raw, "types": types})

    known = load_sources(sources_path)
    for t in catalog.types.values():
        for field in SOURCED_FIELDS:
            if getattr(t, field) is not None and field not in t.sources:
                raise ValueError(f"{t.id}.{field} sem fonte (DEC-0024)")
        for field, source_id in t.sources.items():
            if source_id not in known:
                raise ValueError(f"{t.id}.{field}: fonte não registrada '{source_id}'")
    return catalog
