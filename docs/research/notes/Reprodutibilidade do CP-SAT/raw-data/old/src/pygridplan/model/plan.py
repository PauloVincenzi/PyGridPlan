"""Modelo central da planta. Unidade: milímetros inteiros.

Origem no canto frente-esquerda do terreno visto da rua; x ao longo da frente,
y da frente para o fundo.
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Side = Literal["left", "right", "back"]


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Rect(_Frozen):
    x: int
    y: int
    w: int = Field(gt=0)
    h: int = Field(gt=0)

    @property
    def x2(self) -> int:
        return self.x + self.w

    @property
    def y2(self) -> int:
        return self.y + self.h

    @property
    def area_mm2(self) -> int:
        return self.w * self.h

    def overlaps_interior(self, other: "Rect") -> bool:
        return (
            self.x < other.x2 and other.x < self.x2 and self.y < other.y2 and other.y < self.y2
        )

    def expanded(self, d: int) -> "Rect":
        return Rect(x=self.x - d, y=self.y - d, w=self.w + 2 * d, h=self.h + 2 * d)

    def contains(self, other: "Rect") -> bool:
        return (
            self.x <= other.x and other.x2 <= self.x2 and self.y <= other.y and other.y2 <= self.y2
        )


class Setbacks(_Frozen):
    front: int = Field(default=0, ge=0)
    back: int = Field(default=0, ge=0)
    left: int = Field(default=0, ge=0)
    right: int = Field(default=0, ge=0)


class Site(_Frozen):
    width_mm: int = Field(gt=0)
    depth_mm: int = Field(gt=0)
    setbacks: Setbacks = Setbacks()
    attached_sides: frozenset[Side] = frozenset()
    north: Literal["front", "back", "left", "right"] | None = None  # lado do lote voltado ao norte


class Room(_Frozen):
    id: str = Field(min_length=1)
    type: str
    rect: Rect
    floor: int = 0


class Plan(_Frozen):
    site: Site
    rooms: tuple[Room, ...] = ()
    wall_ext_mm: int = Field(default=150, gt=0)
    wall_int_mm: int = Field(default=100, gt=0)

    @model_validator(mode="after")
    def _unique_room_ids(self) -> "Plan":
        ids = [r.id for r in self.rooms]
        if len(ids) != len(set(ids)):
            raise ValueError("IDs de cômodo duplicados")
        return self


def load_plan(path: Path) -> Plan:
    return Plan.model_validate_json(Path(path).read_text(encoding="utf-8"))


def save_plan(plan: Plan, path: Path) -> None:
    Path(path).write_text(plan.model_dump_json(indent=2), encoding="utf-8")
