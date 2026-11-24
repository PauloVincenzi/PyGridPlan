"""Diagnóstico extra: o limite curto é respeitado? Fase 1 de um caso, sem log, variando o limite e
interleave_search (só aqui; as medições principais usam a configuração do repositório).
Uso: python diag_limit.py REQ K LIMIT INTERLEAVE(0/1)"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import cpsat_exp_v2 as X
import relock_experiment as R

name, k, limit, inter = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4] == "1"
_Orig = X.cp_model.CpSolver
class S(_Orig):
    def solve(self, model, cb=None):
        self.parameters.interleave_search = inter
        return super().solve(model, cb)
X.cp_model.CpSolver = S
base = json.loads(R.BASELINE.read_text(encoding="utf-8"))[name]
req = R.perturbed(R.load_base_request(name, base), base["perturbed_room"])
locks = {rid: base["rects"][rid] for rid in base["lock_order"][:k]}
s = {}
X._phase(req, R.CATALOG, 0, limit, (), 1, None, X.SHAPE_ATTEMPTS[base["shape_index"]], locks=locks, stats=s)
row = {"request": name, "k": k, "limit": limit, "interleave": inter,
       **{a: b for a, b in s.items() if "values" not in a and "names" not in a}}
with (R.HERE / "diag_limit.jsonl").open("a", encoding="utf-8") as f:
    f.write(json.dumps(row) + "\n")
print(row["status"], round(row["solve_s"], 2), round(row["det_time"], 2), row["objective"], row["bound"])
