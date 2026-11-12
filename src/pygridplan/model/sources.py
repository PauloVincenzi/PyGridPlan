"""Registro de fontes: toda citação em data/ aponta para um ID daqui (DEC-0024)."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
DEFAULT_SOURCES_PATH = DATA_DIR / "sources.yaml"

# N norma ABNT · L-fed lei federal · L-mun lei municipal · F programa federal
# A acadêmico · P prática/popular · X proposta do agente (sem fonte externa)
SourceKind = Literal["N", "L-fed", "L-mun", "F", "A", "P", "X"]


class Source(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    title: str
    org: str
    year: int | None = None
    url: str | None = None
    kind: SourceKind
    accessed: str
    note: str = ""


def load_sources(path: Path = DEFAULT_SOURCES_PATH) -> dict[str, Source]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    sources: dict[str, Source] = {}
    for item in raw["sources"]:
        if item["id"] in sources:
            raise ValueError(f"ID de fonte duplicado: {item['id']}")
        sources[item["id"]] = Source.model_validate(item)
    return sources
