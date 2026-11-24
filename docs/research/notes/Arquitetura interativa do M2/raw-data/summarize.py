"""Tabelas em Markdown a partir de baseline.json e results.jsonl (impressas no stdout)."""

import json
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).parent
base = json.loads((HERE / "baseline.json").read_text(encoding="utf-8"))
rows = [json.loads(l) for l in (HERE / "results.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def f(x, d=2):
    return "–" if x is None else f"{x:.{d}f}"


def gap(s):
    if not s or s.get("objective") is None:
        return None
    o, b = s["objective"], s["bound"]
    return abs(b - o) / max(abs(b), 1e-9) * 100


def p1sum(r, key):
    return sum(s.get(key) or 0 for s in r["phase1"])


print("## Base\n")
print("| Pedido | Formato | Total (s) | F1 status | F1 build+solve (s) | F1 dt | F1 obj | F1 bound | F1 gap % | F1 1ª sol (s) | F2 status | F2 (s) | F2 obj | F2 gap % | Nota | Travas (ordem) | Perturbado | concorrência |")
print("|" + "---|" * 18)
for name, b in base.items():
    p1, p2 = b["phase1"][-1], b["phase2"]
    print(f"| {name} | {b['shape_index']} | {f(b['total_s'])} | {p1['status']} | {f(p1sum(b,'build_s'))}+{f(p1sum(b,'solve_s'))} | "
          f"{f(p1sum(b,'det_time'))} | {f(p1['objective'],3)} | {f(p1['bound'],3)} | {f(gap(p1),1)} | {f(p1['first_solution_s'])} | "
          f"{p2['status']} | {f(p2['build_s']+p2['solve_s'])} | {f(p2['objective'],3)} | {f(gap(p2),2)} | {f(b['score'],3)} | "
          f"{', '.join(b['lock_order'])} | {b['perturbed_room']} ({b['perturbed_target_old']:.2f}→{b['perturbed_target_old']*1.25:.2f} m²) | "
          f"{len(b.get('foreign_before', []))}/{len(b.get('foreign_after', []))} |")

checks = {(r["request"], r["k"]): r["status"] for r in rows if r["variant"] == "hint_check"}
print("\n## Execuções (rep 0)\n")
print("| Pedido | k | Variante | dica viável | Status | Formato | Total (s) | F1 (s) | F1 dt | F1 1ª sol (s) | F1 status | F1 gap % | F2 (s) | F2 obj | Nota | travados exatos | cômodos mudados | área perturbado antes→depois (m², retângulo) | concorrência |")
print("|" + "---|" * 19)
for r in rows:
    if r["variant"] == "hint_check" or r.get("rep", 0) != 0:
        continue
    p1 = r["phase1"][-1]
    p2 = r["phase2"] or {}
    print(f"| {r['request']} | {r['k']} | {r['variant']} | {checks.get((r['request'], r['k']), '?') if r['hint'] else '–'} | {r['status']} | {r['shape_index']} | "
          f"{f(r['total_s'])} | {f(p1sum(r,'build_s')+p1sum(r,'solve_s'))} | {f(p1sum(r,'det_time'))} | {f(p1.get('first_solution_s'))} | {p1.get('status')} | {f(gap(p1),1)} | "
          f"{f((p2.get('build_s') or 0)+(p2.get('solve_s') or 0))} | {f(p2.get('objective'),3)} | {f(r.get('score_perturbed_request'),3)} | "
          f"{r.get('locked_exact')} | {len(r.get('rooms_changed', []))} | {f(r.get('perturbed_area_m2_before'))}→{f(r.get('perturbed_area_m2_after'))} | "
          f"{len(r.get('foreign_before', []))}/{len(r.get('foreign_after', []))} |")

reps = [r for r in rows if r.get("rep", 0) > 0]
if reps:
    print("\n## Repetições\n")
    groups = {}
    for r in rows:
        if r["variant"] != "hint_check":
            groups.setdefault((r["request"], r["k"], r["variant"]), []).append(r)
    print("| Pedido | k | Variante | n | Total (s) por rodada | F1 dt | F2 obj por rodada | Nota por rodada | plantas distintas | concorrência |")
    print("|" + "---|" * 10)
    for key, g in groups.items():
        if not any(r.get("rep", 0) > 0 for r in g):
            continue
        plans = {json.dumps(r.get("rects"), sort_keys=True) for r in g}
        print(f"| {key[0]} | {key[1]} | {key[2]} | {len(g)} | {', '.join(f(r['total_s']) for r in g)} | "
              f"{', '.join(f(p1sum(r,'det_time')) for r in g)} | {', '.join(f((r['phase2'] or {}).get('objective'),3) for r in g)} | "
              f"{', '.join(f(r.get('score_perturbed_request'),3) for r in g)} | {len(plans)} | "
              f"{', '.join(str(len(r.get('foreign_before', []))) for r in g)} |")
