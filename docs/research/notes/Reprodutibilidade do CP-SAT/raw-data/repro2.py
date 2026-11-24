"""Reprodutor do modelo nº 3 da casa grande: fase 1 da 2ª alternativa (semente 1, padrões da 1ª proibidos).

  python repro2.py prep            -> salva o padrão da 1ª alternativa em alt1-pattern.json
  python repro2.py run --label X [--set chave=valor ...] [--limit N]
"""

import argparse
import json
import math
import time
from pathlib import Path

import repro  # patch de CpSolver.solve
from pygridplan.generators import cpsat
from pygridplan.model.catalog import load_catalog
from pygridplan.model.request import load_request
from pygridplan.scoring.diversity import mirrored, relative_pattern

HERE = Path(__file__).resolve().parent
PATTERN = HERE / "alt1-pattern.json"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("prep", "run"))
    ap.add_argument("--label", default="")
    ap.add_argument("--limit", type=float, default=None)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--set", action="append", default=[])
    a = ap.parse_args()
    request, catalog = load_request(repro.REQ_DIR / "large-house.json"), load_catalog()
    if a.mode == "prep":
        plan = cpsat.solve_layout(request, catalog, seed=0)
        PATTERN.write_text(json.dumps([[k[0], k[1], list(v)] for k, v in relative_pattern(plan).items()]))
        print("padrão salvo", PATTERN)
        return
    for kv in a.set:
        k, v = kv.split("=", 1)
        repro.OVERRIDES[k] = repro.parse_value(v)
    pattern = {(x, y): tuple(v) for x, y, v in json.loads(PATTERN.read_text())}
    min_diff = max(1, math.ceil(cpsat.MIN_DIFF_FRACTION * math.comb(len(request.rooms), 2)))
    t0 = time.perf_counter()
    plan, status, topo = cpsat._phase(request, catalog, a.seed, repro.budget(a.limit), [pattern, mirrored(pattern)],
                                      min_diff, None, cpsat.SHAPE_ATTEMPTS[0])
    c = repro.calls[0]
    print(json.dumps(dict(label=a.label, overrides=repro.OVERRIDES, total=round(time.perf_counter() - t0, 1),
                          status=c["status"], obj=c["obj"], dtime=c["dtime"], sol=c["sol"], model=c["model"],
                          topo=hash(tuple(topo)) if topo else None)), flush=True)


if __name__ == "__main__":
    main()
