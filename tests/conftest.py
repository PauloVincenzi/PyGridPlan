from pathlib import Path

import pytest

BASIC_HOUSE = Path(__file__).parent / "fixtures" / "plans" / "basic-house.json"


@pytest.fixture
def basic_house():
    from pygridplan.model.plan import load_plan

    return load_plan(BASIC_HOUSE)
