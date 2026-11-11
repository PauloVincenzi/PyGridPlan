"""Paredes derivadas dos retângulos dos cômodos (modelo de eixos) e área útil.

As paredes não são armazenadas: arestas compartilhadas viram paredes internas,
trechos de lado sem vizinho viram paredes externas.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from pygridplan.model.plan import Plan, Rect, Room

SideName = Literal["left", "right", "bottom", "top"]
OPPOSITE: dict[SideName, SideName] = {"left": "right", "right": "left", "bottom": "top", "top": "bottom"}


class Wall(BaseModel):
    model_config = ConfigDict(frozen=True)

    x1: int
    y1: int
    x2: int
    y2: int
    thickness_mm: int
    kind: Literal["ext", "int"]
    room_ids: tuple[str, ...]


def _side(r: Rect, name: SideName) -> tuple[int, int, int]:
    """(coordenada fixa, início, fim) do lado."""
    return {
        "left": (r.x, r.y, r.y2),
        "right": (r.x2, r.y, r.y2),
        "bottom": (r.y, r.x, r.x2),
        "top": (r.y2, r.x, r.x2),
    }[name]


def _shared(a: Rect, side: SideName, b: Rect) -> tuple[int, int] | None:
    """Trecho (comprimento > 0) do lado `side` de `a` encostado no lado oposto de `b`."""
    ca, lo_a, hi_a = _side(a, side)
    cb, lo_b, hi_b = _side(b, OPPOSITE[side])
    lo, hi = max(lo_a, lo_b), min(hi_a, hi_b)
    return (lo, hi) if ca == cb and lo < hi else None


def _uncovered(lo: int, hi: int, covers: list[tuple[int, int]]) -> list[tuple[int, int]]:
    gaps, pos = [], lo
    for c_lo, c_hi in sorted(covers):
        if c_lo > pos:
            gaps.append((pos, c_lo))
        pos = max(pos, c_hi)
    if pos < hi:
        gaps.append((pos, hi))
    return gaps


def _exterior_parts(room: Room, side: SideName, plan: Plan) -> list[tuple[int, int]]:
    _, lo, hi = _side(room.rect, side)
    covers = [s for o in plan.rooms if o.id != room.id if (s := _shared(room.rect, side, o.rect))]
    return _uncovered(lo, hi, covers)


def _segment(side: SideName, coord: int, lo: int, hi: int) -> tuple[int, int, int, int]:
    return (coord, lo, coord, hi) if side in ("left", "right") else (lo, coord, hi, coord)


def derive_walls(plan: Plan) -> list[Wall]:
    walls: list[Wall] = []
    rooms = plan.rooms
    for i, a in enumerate(rooms):
        for b in rooms[i + 1 :]:
            for side in OPPOSITE:
                if seg := _shared(a.rect, side, b.rect):
                    x1, y1, x2, y2 = _segment(side, _side(a.rect, side)[0], *seg)
                    walls.append(Wall(x1=x1, y1=y1, x2=x2, y2=y2, thickness_mm=plan.wall_int_mm,
                                      kind="int", room_ids=(a.id, b.id)))
    for room in rooms:
        for side in OPPOSITE:
            coord = _side(room.rect, side)[0]
            for lo, hi in _exterior_parts(room, side, plan):
                x1, y1, x2, y2 = _segment(side, coord, lo, hi)
                walls.append(Wall(x1=x1, y1=y1, x2=x2, y2=y2, thickness_mm=plan.wall_ext_mm,
                                  kind="ext", room_ids=(room.id,)))
    return walls


def _half_thickness(room: Room, side: SideName, plan: Plan) -> int:
    """Lado com qualquer trecho externo usa a espessura externa (conservador)."""
    exterior = bool(_exterior_parts(room, side, plan))
    return (plan.wall_ext_mm if exterior else plan.wall_int_mm) // 2


def useful_dims_mm(room: Room, plan: Plan) -> tuple[int, int]:
    t = {side: _half_thickness(room, side, plan) for side in OPPOSITE}
    return room.rect.w - t["left"] - t["right"], room.rect.h - t["bottom"] - t["top"]


def useful_area_mm2(room: Room, plan: Plan) -> int:
    w, h = useful_dims_mm(room, plan)
    return w * h
