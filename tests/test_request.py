from pathlib import Path

import pytest
from pydantic import ValidationError

from conftest import BASIC_HOUSE
from pygridplan.model.plan import Site, load_plan
from pygridplan.model.request import Relation, Request, RoomRequest, load_request

BASIC_PROGRAM = Path(__file__).parent / "fixtures" / "requests" / "basic-program.json"
SITE = Site(width_mm=10000, depth_mm=10000)
ROOMS = (RoomRequest(id="a", type="sala"), RoomRequest(id="b", type="cozinha"))


def test_load_basic_program():
    req = load_request(BASIC_PROGRAM)
    assert len(req.rooms) == 8
    assert len(req.relations) == 5
    assert req.site.north == "back"


def test_relation_to_unknown_room_rejected():
    with pytest.raises(ValidationError):
        Request(site=SITE, rooms=ROOMS, relations=(Relation(a="a", b="x", kind="near", intensity=3),))


def test_self_relation_rejected():
    with pytest.raises(ValidationError):
        Request(site=SITE, rooms=ROOMS, relations=(Relation(a="a", b="a", kind="near", intensity=3),))


def test_duplicate_pair_rejected():
    rels = (Relation(a="a", b="b", kind="near", intensity=3), Relation(a="b", b="a", kind="far", intensity=1))
    with pytest.raises(ValidationError):
        Request(site=SITE, rooms=ROOMS, relations=rels)


@pytest.mark.parametrize("intensity", [0, 6])
def test_intensity_out_of_range_rejected(intensity):
    with pytest.raises(ValidationError):
        Relation(a="a", b="b", kind="near", intensity=intensity)


def test_basic_house_still_loads():
    assert load_plan(BASIC_HOUSE).site.north is None
