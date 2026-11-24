"""Reprodução da não reprodutibilidade do CP-SAT (S07).

Intercepta CpSolver.solve: registra impressão digital do modelo, parâmetros sobrescritos, status, objetivo,
limite, tempo de relógio, tempo determinístico e hash da solução.

Uso:
  python repro.py --request large-house --reps 3 --mode topo --limit 20 [--set chave=valor ...]
  --mode topo : só a fase 1 da primeira forma (retângulo, 1,5x)
  --mode full : solve_layout completo (formas + fase 2)
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from ortools.sat.python import cp_model

from pygridplan.generators import cpsat
from pygridplan.model.catalog import load_catalog
from pygridplan.model.request import load_request
from pygridplan.scoring.score import score_plan

REQ_DIR = Path(r"c:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan\tests\fixtures\requests")
# funciona com o código antigo (time_limit, unidades determinísticas) e com o novo (batches, lotes)
BUDGET_KW = "batches" if hasattr(cpsat, "DEFAULT_BATCHES") else "time_limit"
DEFAULT_BUDGET = getattr(cpsat, "DEFAULT_BATCHES", None) or getattr(cpsat, "DEFAULT_TIME_LIMIT")


def budget(value: float | None):
    if value is None:
        return DEFAULT_BUDGET
    return int(value) if BUDGET_KW == "batches" else value

calls: list[dict] = []
OVERRIDES: dict = {}
_orig_solve = cp_model.CpSolver.solve


def _patched(self, model, *args, **kwargs):
    for k, v in OVERRIDES.items():
        setattr(self.parameters, k, v)
    proto = str(model.Proto()).encode()
    t0 = time.perf_counter()
    status = _orig_solve(self, model, *args, **kwargs)
    wall = time.perf_counter() - t0
    resp = self.response_proto
    calls.append(dict(
        model=hashlib.sha1(proto).hexdigest()[:10],
        nvars=len(model.Proto().variables),
        status=self.status_name(status),
        obj=round(self.objective_value, 4) if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
        bound=round(self.best_objective_bound, 4),
        wall=round(wall, 2),
        dtime=round(self.deterministic_time, 3),
        branches=self.num_branches,
        conflicts=self.num_conflicts,
        sol=hashlib.sha1(str(list(resp.solution)).encode()).hexdigest()[:10],
    ))
    return status


cp_model.CpSolver.solve = _patched


def parse_value(v: str):
    if v in ("true", "false"):
        return v == "true"
    for cast in (int, float):
        try:
            return cast(v)
        except ValueError:
            pass
    return v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", default="large-house")
    ap.add_argument("--attached", default="")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--mode", choices=("topo", "full"), default="topo")
    ap.add_argument("--limit", type=float, default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--set", action="append", default=[])
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    for kv in a.set:
        k, v = kv.split("=", 1)
        OVERRIDES[k] = parse_value(v)

    request, catalog = load_request(REQ_DIR / f"{a.request}.json"), load_catalog()
    if a.attached:
        site = request.site.model_copy(update={"attached_sides": frozenset(a.attached.split(","))})
        request = request.model_copy(update={"site": site})

    for rep in range(a.reps):
        calls.clear()
        t0 = time.perf_counter()
        topo = None
        if a.mode == "topo":
            plan, _, topo = cpsat._phase(request, catalog, a.seed, budget(a.limit), (), 1, None, cpsat.SHAPE_ATTEMPTS[0])
        else:
            plan = cpsat.solve_layout(request, catalog, seed=a.seed, **{BUDGET_KW: budget(a.limit)})
        total = time.perf_counter() - t0
        rects = [(r.id, r.rect.x, r.rect.y, r.rect.w, r.rect.h) for r in plan.rooms] if plan else None
        extra = {}
        if plan is not None:
            crit = {c.name: round(c.value, 3) for c in score_plan(plan, request, catalog).criteria}
            extra = dict(score=round(score_plan(plan, request, catalog).total, 4), area=crit.get("area_fit"),
                         compact=crit.get("compactness"))
        out = dict(label=a.label, request=a.request, mode=a.mode, limit=a.limit, rep=rep,
                   overrides=OVERRIDES, total=round(total, 2),
                   plan=hashlib.sha1(str(rects).encode()).hexdigest()[:10],
                   topo=hashlib.sha1(str(topo).encode()).hexdigest()[:10] if topo else None,
                   **extra, calls=list(calls))
        print(json.dumps(out), flush=True)


if __name__ == "__main__":
    sys.exit(main())
