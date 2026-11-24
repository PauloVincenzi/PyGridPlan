"""Cópia exata do corpo de test_same_request_same_plans_when_the_search_stops_at_its_budget, sem o import de
DEFAULT_BATCHES, para conferir o RED contra o código antigo (main 672af29)."""

from pathlib import Path

from pygridplan.generators.cpsat import generate_alternatives
from pygridplan.model.catalog import load_catalog
from pygridplan.model.request import load_request

REQUESTS = Path(r"C:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan-worktrees\fix-cpsat-reproducibility\tests\fixtures\requests")


def test_same_request_same_plans_when_the_search_stops_at_its_budget(monkeypatch):
    from concurrent.futures import ThreadPoolExecutor

    from ortools.sat.python import cp_model

    statuses, solve = [], cp_model.CpSolver.solve

    def recording(self, *args, **kwargs):
        status = solve(self, *args, **kwargs)
        statuses.append(status)
        return status

    monkeypatch.setattr(cp_model.CpSolver, "solve", recording)
    request, catalog = load_request(REQUESTS / "large-house.json"), load_catalog()
    with ThreadPoolExecutor(2) as pool:
        first, second = pool.map(lambda _: generate_alternatives(request, catalog, k=2), range(2))
    assert cp_model.FEASIBLE in statuses  # a premissa: alguma resolução parou no orçamento, sem provar o ótimo
    assert [a.plan for a in first] == [a.plan for a in second]
