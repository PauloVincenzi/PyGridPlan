"""Fase 2 com 1, 2 e 3 lotes sobre a topologia da fase 1 (6 lotes); e fase 1 com 1 lote (caminho "timeout")."""

import time

import repro  # patch de CpSolver.solve
from pygridplan.generators import cpsat
from pygridplan.model.catalog import load_catalog
from pygridplan.model.request import load_request

catalog = load_catalog()
for name in ("one-bedroom", "basic-program", "three-bedroom", "large-house"):
    request = load_request(repro.REQ_DIR / f"{name}.json")
    shape = cpsat.SHAPE_ATTEMPTS[0]
    plan, status, topo = cpsat._phase(request, catalog, 0, cpsat.DEFAULT_BATCHES, (), 1, None, shape)
    for b in (1, 2, 3):
        repro.calls.clear()
        t0 = time.perf_counter()
        polished = cpsat._phase(request, catalog, 0, b, (), 1, topo, shape)[0]
        c = repro.calls[0]
        print(f"{name:14} fase2 lotes={b} {c['status']:9} obj={c['obj']} dtime={c['dtime']} wall={time.perf_counter() - t0:.2f}s")
request = load_request(repro.REQ_DIR / "basic-program.json")
repro.calls.clear()
print("basic-program fase1 lotes=1:", cpsat._phase(request, catalog, 0, 1, (), 1, None, cpsat.SHAPE_ATTEMPTS[0])[1],
      repro.calls[0]["status"])
