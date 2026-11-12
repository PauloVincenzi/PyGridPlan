"""Pedido (programa de necessidades): terreno, cômodos pedidos e relações entre eles."""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from pygridplan.model.plan import Site


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class RoomRequest(_Frozen):
    id: str = Field(min_length=1)
    type: str
    target_area_m2: float | None = Field(default=None, gt=0)


class Relation(_Frozen):
    a: str
    b: str
    kind: Literal["near", "far"]  # aproximar / afastar
    intensity: int = Field(ge=1, le=5)


class Request(_Frozen):
    site: Site
    rooms: tuple[RoomRequest, ...] = Field(min_length=1)
    relations: tuple[Relation, ...] = ()

    @model_validator(mode="after")
    def _consistent(self) -> "Request":
        ids = [r.id for r in self.rooms]
        if len(ids) != len(set(ids)):
            raise ValueError("IDs de cômodo duplicados")
        pairs = set()
        for rel in self.relations:
            if rel.a == rel.b:
                raise ValueError(f"relação de {rel.a} com ele mesmo")
            if rel.a not in ids or rel.b not in ids:
                raise ValueError(f"relação cita cômodo inexistente: {rel.a}–{rel.b}")
            pair = frozenset((rel.a, rel.b))
            if pair in pairs:
                raise ValueError(f"relação repetida: {rel.a}–{rel.b}")
            pairs.add(pair)
        return self


def load_request(path: Path) -> Request:
    return Request.model_validate_json(Path(path).read_text(encoding="utf-8"))
