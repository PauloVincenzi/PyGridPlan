"""Tabelas compactas (rep 0) por pedido, para a nota."""
import json
from pathlib import Path
HERE = Path(__file__).parent
rows = [json.loads(l) for l in (HERE / "results.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
base = json.loads((HERE / "baseline.json").read_text(encoding="utf-8"))
chk = {(r["request"], r["k"]): r["status"] for r in rows if r["variant"] == "hint_check"}
order = ["cold", "hinted", "fast_cold", "fast_partial", "fast_hint"]
def f(x, d=2): return "–" if x is None else f"{x:.{d}f}"
for name in ["one-bedroom", "small-lot", "basic-program", "three-bedroom", "large-house"]:
    b = base[name]
    print(f"\n#### {name}\n")
    print("| k | variante | total (s) | F1 (s) | F1 dt | F1 status | F1 gap % | 1ª sol. (s) | F2 obj | nota | mudaram | conc. |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k in (0, 1, 2, 3):
        for v in order:
            g = [r for r in rows if r["request"] == name and r["k"] == k and r["variant"] == v and r.get("rep", 0) == 0]
            if not g: continue
            r = g[0]; p = r["phase1"]; last = p[-1]
            gap = abs(last["bound"] - last["objective"]) / abs(last["bound"]) * 100
            f1 = sum(a["build_s"] + a["solve_s"] for a in p); dt = sum(a["det_time"] for a in p)
            vv = v + (" (dica inviável → prefixo)" if r.get("hint_completion_status") == "INFEASIBLE" else "")
            conc = "sim" if r.get("foreign_before") or r.get("foreign_after") else "não"
            print(f"| {k} | {vv} | {f(r['total_s'])} | {f(f1)} | {f(dt)} | {last['status']} | {f(gap,1)} | {f(last['first_solution_s'])} | "
                  f"{f(r['phase2']['objective'],3)} | {f(r['score_perturbed_request'],3)} | {len(r['rooms_changed'])} | {conc} |")
