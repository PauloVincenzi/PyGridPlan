"""Bancada: generate_alternatives(k=4, semente 0) nos pedidos de referência; uma linha JSON por pedido.

Uso: PYTHONPATH=<src> python bench.py RÓTULO PASTA_DOS_PEDIDOS [pedido ...]
Registra tempo, nota, área, retângulos (para comparar plantas) e cada resolução do CP-SAT (tempo e situação).
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import ortools
from ortools.sat.python import cp_model

from pygridplan.generators import cpsat
from pygridplan.model.catalog import load_catalog
from pygridplan.model.request import load_request

ALL = ("one-bedroom", "small-lot", "basic-program", "three-bedroom", "large-house")
calls: list[dict] = []
_solve = cp_model.CpSolver.solve


def recording(self, *args, **kwargs):
    t0 = time.perf_counter()
    status = _solve(self, *args, **kwargs)
    calls.append(dict(status=self.status_name(status), wall=round(time.perf_counter() - t0, 2)))
    return status


cp_model.CpSolver.solve = recording
label, folder, names = sys.argv[1], Path(sys.argv[2]), sys.argv[3:] or ALL
catalog = load_catalog()
for name in names:
    request = load_request(folder / f"{name}.json")
    calls.clear()
    start, cpu = time.perf_counter(), time.process_time()
    alts = cpsat.generate_alternatives(request, catalog, k=4)
    total, cpu = time.perf_counter() - start, time.process_time() - cpu
    rows = []
    for alt in alts:
        rects = [(r.id, r.rect.x, r.rect.y, r.rect.w, r.rect.h) for r in alt.plan.rooms]
        crit = {c.name: round(c.value, 3) for c in alt.score.criteria}
        rows.append(dict(plan=hashlib.sha1(str(rects).encode()).hexdigest()[:8], score=round(alt.score.total, 4),
                         area=crit["area_fit"]))
    print(json.dumps(dict(label=label, request=name, ortools=ortools.__version__, total=round(total, 1),
                          cpu=round(cpu, 1), alts=rows, calls=list(calls))), flush=True)
