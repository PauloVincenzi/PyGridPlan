"""Catálogo de tipos de cômodo: fonte única de zona, passagem e mínimos."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict

DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[3] / "data" / "room_types.yaml"


class RoomType(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    name: str
    zone: Literal["social", "intima", "servico"]
    passage: Literal["private", "traversable"]
    min_width_mm: int | None = None
    min_area_m2: float | None = None
    source: str


class Catalog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str
    updated: str
    types: dict[str, RoomType]

    def get(self, type_id: str) -> RoomType:
        """Tipo desconhecido vira um tipo personalizado atravessável e sem mínimos."""
        return self.types.get(type_id) or RoomType(
            id=type_id,
            name=type_id,
            zone="social",
            passage="traversable",
            source="tipo personalizado",
        )


def load_catalog(path: Path = DEFAULT_CATALOG_PATH) -> Catalog:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    raw["types"] = {t["id"]: t for t in raw["types"]}
    return Catalog.model_validate(raw)
