"""Diagnóstico: por que deterministic_time passa do max_deterministic_time? Roda a fase 1 de um caso com o log
do CP-SAT ligado (só aqui; nas medições o log fica desligado). Uso: python diag_dt.py REQ K LIMIT"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cpsat_exp_v2 as X  # noqa: E402
import relock_experiment as R  # noqa: E402

_Orig = X.cp_model.CpSolver


class LoggingSolver(_Orig):
    def solve(self, model, cb=None):
        self.parameters.log_search_progress = True
        self.parameters.log_to_stdout = True
        return super().solve(model, cb)


X.cp_model.CpSolver = LoggingSolver
name, k, limit = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
base = json.loads(R.BASELINE.read_text(encoding="utf-8"))[name]
req = R.perturbed(R.load_base_request(name, base), base["perturbed_room"])
locks = {rid: base["rects"][rid] for rid in base["lock_order"][:k]}
s = {}
X._phase(req, R.CATALOG, 0, limit, (), 1, None, X.SHAPE_ATTEMPTS[base["shape_index"]], locks=locks, stats=s)
print("STATS", {key: v for key, v in s.items() if "values" not in key and "names" not in key})
