"""Bancada S07: generate_alternatives(k=4) nos pedidos de referência, com tempo, nota, área e hash de cada planta.

Uso: python bench.py --label antes [--requests a,b] [--k 4] [--limit 20] [--set chave=valor ...]
Saída: uma linha JSON por pedido.
"""

import argparse
import hashlib
import json
import time

import repro  # aplica o patch em CpSolver.solve (registra cada resolução em repro.calls)
from pygridplan.generators import cpsat
from pygridplan.model.catalog import load_catalog
from pygridplan.model.request import load_request

ALL = ("one-bedroom", "small-lot", "basic-program", "three-bedroom", "large-house")


def plan_hash(plan) -> str:
    rects = [(r.id, r.rect.x, r.rect.y, r.rect.w, r.rect.h) for r in plan.rooms]
    return hashlib.sha1(str(rects).encode()).hexdigest()[:8]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--requests", default=",".join(ALL))
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--limit", type=float, default=None)
    ap.add_argument("--set", action="append", default=[])
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    for kv in a.set:
        k, v = kv.split("=", 1)
        repro.OVERRIDES[k] = repro.parse_value(v)
    catalog = load_catalog()
    for name in a.requests.split(","):
        request = load_request(repro.REQ_DIR / f"{name}.json")
        repro.calls.clear()
        t0 = time.perf_counter()
        alts = cpsat.generate_alternatives(request, catalog, k=a.k, **{repro.BUDGET_KW: repro.budget(a.limit)})
        total = time.perf_counter() - t0
        rows = []
        for alt in alts:
            crit = {c.name: round(c.value, 3) for c in alt.score.criteria}
            rows.append(dict(plan=plan_hash(alt.plan), score=round(alt.score.total, 4), area=crit.get("area_fit"),
                             compact=crit.get("compactness")))
        print(json.dumps(dict(label=a.label, request=name, k=a.k, limit=repro.budget(a.limit), overrides=repro.OVERRIDES,
                              total=round(total, 1), alts=rows,
                              calls=[{k: c[k] for k in ("status", "obj", "wall", "dtime", "sol", "model")}
                                     for c in repro.calls])),
              flush=True)


if __name__ == "__main__":
    main()
