"""Parâmetros de implantação com fonte (muro, distância de janela, permeabilidade de referência)."""

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict

from pygridplan.model.sources import DATA_DIR, DEFAULT_SOURCES_PATH, check_sourced, load_sources

DEFAULT_SITE_DEFAULTS_PATH = DATA_DIR / "site_defaults.yaml"


class SiteDefaults(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    fence_thickness_mm: int
    window_min_distance_mm: int
    permeability_min: float
    sources: dict[str, str]


def load_site_defaults(path: Path = DEFAULT_SITE_DEFAULTS_PATH,
                       sources_path: Path = DEFAULT_SOURCES_PATH) -> SiteDefaults:
    defaults = SiteDefaults.model_validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")))
    values = defaults.model_dump(exclude={"sources"})
    check_sourced("site_defaults", values, defaults.sources, load_sources(sources_path))
    return defaults
