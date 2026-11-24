"""Experimento: travar 1 a 3 cômodos e re-resolver (CP-SAT do PyGridPlan), medindo tempo e qualidade.

Uso:
  python relock_experiment.py baseline            -> baseline.json (planta-base por pedido)
  python relock_experiment.py runs [REQ ...]      -> acrescenta linhas em results.jsonl
  python relock_experiment.py repeat REQ K VARIANT N  -> repete um caso N vezes (rep = 1..N)
Cada execução é gravada assim que termina (JSONL), para um travamento não perder dados.
"""

import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cpsat_exp_v2 as X  # noqa: E402  (cópia com patches; ver cpsat_exp_v2.diff)

from pygridplan.model.catalog import load_catalog  # noqa: E402
from pygridplan.model.request import load_request  # noqa: E402
from pygridplan.scoring.score import room_target_m2, score_plan  # noqa: E402
from pygridplan.validation.access import check_access  # noqa: E402
from pygridplan.validation.checks import validate_geometry  # noqa: E402

HERE = Path(__file__).parent
REQ_DIR = Path(r"c:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan\tests\fixtures\requests")
REQUESTS = ["basic-program", "large-house", "one-bedroom", "small-lot", "three-bedroom"]
RUN_ORDER = ["one-bedroom", "small-lot", "basic-program", "three-bedroom", "large-house"]
BASELINE = HERE / "baseline.json"
RESULTS = HERE / "results.jsonl"
SEED = 0
FAST_TIME = 2.0
PERTURB = 1.25
CATALOG = load_catalog()

# variantes: (dica, limite da fase 1 em unidades determinísticas). Dica "complete" = valores de TODAS as
# variáveis do modelo perturbado (obtidos fixando a planta-base e completando as auxiliares do objetivo);
# "prefix" = só as variáveis criadas antes do objetivo (as auxiliares do objetivo ficam sem dica)
VARIANTS = {
    "cold": (None, X.DEFAULT_TIME_LIMIT),
    "hinted": ("complete", X.DEFAULT_TIME_LIMIT),
    "fast_hint": ("complete", FAST_TIME),
    "fast_partial": ("prefix", FAST_TIME),
    "fast_cold": (None, FAST_TIME),
}


def solve_x(request, *, time_limit, locks=None, hint=None):
    """Igual a cpsat._solve (tentativas de formato em ordem + polimento), com travas e dica na fase 1.
    A fase 2 recebe as mesmas travas (sem dica: a topologia já vem fixada)."""
    pairs = math.comb(len(request.rooms), 2)
    min_diff = max(1, math.ceil(X.MIN_DIFF_FRACTION * pairs))  # como generate_alternatives (inerte sem forbidden)
    attempts = []
    t0 = time.perf_counter()
    status = "infeasible"
    for si, shape in enumerate(X.SHAPE_ATTEMPTS):
        s1 = {"shape_index": si}
        plan, status, topology = X._phase(request, CATALOG, SEED, time_limit, (), min_diff, None, shape,
                                          locks=locks, hint=hint, stats=s1)
        attempts.append(s1)
        if plan is not None:
            s2 = {}
            polished = X._phase(request, CATALOG, SEED, X.POLISH_TIME, (), min_diff, topology, shape,
                                locks=locks, stats=s2)[0]
            return {"plan": polished or plan, "status": "ok", "shape_index": si, "phase1": attempts,
                    "phase2": s2, "total_s": time.perf_counter() - t0, "polish_failed": polished is None}
        if status != "infeasible":
            break
    return {"plan": None, "status": status, "shape_index": None, "phase1": attempts, "phase2": None,
            "total_s": time.perf_counter() - t0}


def rects(plan):
    return {r.id: [r.rect.x // X.GRID, r.rect.y // X.GRID, r.rect.w // X.GRID, r.rect.h // X.GRID] for r in plan.rooms}


def choose(request):
    """Ordem de travamento: maior área-alvo efetiva primeiro (room_target_m2; empate = ordem do pedido;
    sem alvo, por último). Perturbado: o 4.º da ordem (nunca travado com k <= 3)."""
    ranked = sorted(range(len(request.rooms)),
                    key=lambda i: (-(room_target_m2(request.rooms[i], CATALOG) or -1), i))
    ids = [request.rooms[i].id for i in ranked]
    return ids[:3], ids[3]


def perturbed(request, room_id):
    rooms = []
    for r in request.rooms:
        if r.id == room_id:
            t = room_target_m2(r, CATALOG)
            r = r.model_copy(update={"target_area_m2": round(t * PERTURB, 3)})
        rooms.append(r)
    return request.model_copy(update={"rooms": tuple(rooms)})


def strip(res):
    """Resumo serializável (sem os vetores grandes)."""
    def clean(s):
        return None if s is None else {k: v for k, v in s.items()
                                       if k not in ("prefix_values", "prefix_names", "full_values")}
    return {"status": res["status"], "shape_index": res["shape_index"], "total_s": res["total_s"],
            "phase1": [clean(s) for s in res["phase1"]], "phase2": clean(res["phase2"]),
            "polish_failed": res.get("polish_failed")}


def foreign_python():
    """PIDs de python fora deste processo (outra carga de CP-SAT na máquina contamina os tempos)."""
    import os
    import subprocess
    mine = {os.getpid(), os.getppid()}
    out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True).stdout
    pids = []
    for line in out.splitlines():
        cols = [c.strip('"') for c in line.split('","')]
        if len(cols) > 1 and cols[0].lower().startswith("python") and int(cols[1]) not in mine:
            pids.append(int(cols[1]))
    return pids


def append(row):
    with RESULTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_baseline(names):
    data = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    for name in names:
        foreign_before = foreign_python()
        req = load_request(REQ_DIR / f"{name}.json")
        res = solve_x(req, time_limit=X.DEFAULT_TIME_LIMIT)
        plan = res["plan"]
        locks, pert = choose(req)
        p2 = res["phase2"] if res["phase2"] and res["phase2"].get("prefix_values") else res["phase1"][-1]
        entry = strip(res)
        entry.update(
            rects=rects(plan), lock_order=locks, perturbed_room=pert,
            perturbed_target_old=room_target_m2(next(r for r in req.rooms if r.id == pert), CATALOG),
            score=score_plan(plan, req, CATALOG).total,
            geometry_issues=len(validate_geometry(plan)), access_issues=len(check_access(plan, CATALOG)),
            hint={"n_prefix": len(p2["prefix_values"]), "values": p2["prefix_values"],
                  "names": {n: v for n, v in zip(p2["prefix_names"], p2["prefix_values"]) if n}},
            hint_source="phase2" if p2 is res["phase2"] else "phase1",
            foreign_before=foreign_before, foreign_after=foreign_python(), t_wall=time.strftime("%H:%M:%S"),
        )
        data[name] = entry
        print(name, entry["status"], entry["shape_index"], round(entry["total_s"], 2),
              [(s["status"], round(s["solve_s"], 2), round(s["det_time"], 2)) for s in entry["phase1"]],
              flush=True)
        BASELINE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def hint_feasible(req, locks, base, shape_index):
    """A dica (planta-base inteira) satisfaz o modelo perturbado com travas? Fixa as variáveis e resolve."""
    s = {}
    plan, status, _ = X._phase(req, CATALOG, SEED, 5.0, (), 1, None, X.SHAPE_ATTEMPTS[shape_index],
                               locks=locks, hint=base["hint"], fix_hint=True, stats=s)
    return s.get("status"), s.get("hint_mode")


def one_run(name, k, variant, rep=0, base=None):
    base = base or json.loads(BASELINE.read_text(encoding="utf-8"))[name]
    req0 = load_request(REQ_DIR / f"{name}.json")
    req = perturbed(req0, base["perturbed_room"])
    lock_ids = base["lock_order"][:k]
    locks = {rid: base["rects"][rid] for rid in lock_ids}
    hint_kind, limit = VARIANTS[variant]
    use_hint = hint_kind is not None
    foreign_before = foreign_python()
    hint, completion = None, {}
    t_c = time.perf_counter()
    if hint_kind == "prefix":
        hint = base["hint"]
    elif hint_kind == "complete":
        s = {}
        X._phase(req, CATALOG, SEED, 5.0, (), 1, None, X.SHAPE_ATTEMPTS[base["shape_index"]],
                 locks=locks, hint=base["hint"], fix_hint=True, stats=s)
        completion = {"hint_completion_status": s.get("status"), "hint_completion_s": time.perf_counter() - t_c}
        hint = dict(base["hint"], full_values=s["full_values"]) if s.get("full_values") else base["hint"]
    res = solve_x(req, time_limit=limit, locks=locks, hint=hint)
    row = {"request": name, "k": k, "variant": variant, "rep": rep, "locked": lock_ids,
           "perturbed_room": base["perturbed_room"], "time_limit": limit, "hint": hint_kind, **completion, **strip(res),
           "t_wall": time.strftime("%H:%M:%S"), "foreign_before": foreign_before,
           "foreign_after": foreign_python()}
    plan = res["plan"]
    if plan is not None:
        rr = rects(plan)
        row["rects"] = rr
        row["locked_exact"] = all(rr[r] == base["rects"][r] for r in lock_ids)
        row["rooms_changed"] = sorted(r for r in rr if rr[r] != base["rects"][r])
        pr = next(r for r in plan.rooms if r.id == base["perturbed_room"])
        pb = base["rects"][base["perturbed_room"]]
        row["perturbed_rect_before"], row["perturbed_rect_after"] = pb, rr[base["perturbed_room"]]
        row["perturbed_area_m2_after"] = pr.rect.w * pr.rect.h / 1e6
        row["perturbed_area_m2_before"] = pb[2] * pb[3] * X.GRID**2 / 1e6
        row["score_perturbed_request"] = score_plan(plan, req, CATALOG).total
        row["geometry_issues"] = len(validate_geometry(plan))
        row["access_issues"] = len(check_access(plan, CATALOG))
    append(row)
    assert plan is None or row["locked_exact"], (name, k, variant)
    p1 = res["phase1"][-1]
    print(name, k, variant, rep, res["status"], res["shape_index"], f"tot={res['total_s']:.2f}s",
          f"p1={p1.get('status')} {p1.get('solve_s', 0):.2f}s dt={p1.get('det_time', 0):.2f}",
          f"obj2={(res['phase2'] or {}).get('objective')}", flush=True)
    return row


def run_all(names, plan="AB"):
    """A (barato): k = 0..3 x variantes de 2 dt. B: k = 1..3 x cold/hinted (20 dt). C: k = 0 x cold/hinted."""
    allbase = json.loads(BASELINE.read_text(encoding="utf-8"))
    for name in names:
        base = allbase[name]
        req = perturbed(load_request(REQ_DIR / f"{name}.json"), base["perturbed_room"])
        if "A" in plan:
            for k in (0, 1, 2, 3):
                locks = {rid: base["rects"][rid] for rid in base["lock_order"][:k]}
                st, mode = hint_feasible(req, locks, base, base["shape_index"])
                append({"request": name, "k": k, "variant": "hint_check", "status": st, "hint_mode": mode})
                print(name, k, "hint_check", st, mode, flush=True)
                for variant in ("fast_cold", "fast_partial", "fast_hint"):
                    one_run(name, k, variant, base=base)
        for k in ((1, 2, 3) if "B" in plan else ()) + ((0,) if "C" in plan else ()):
            for variant in ("cold", "hinted"):
                one_run(name, k, variant, base=base)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "baseline":
        run_baseline(sys.argv[2:] or REQUESTS)
    elif cmd == "runs":
        run_all(sys.argv[3:] or RUN_ORDER, sys.argv[2]) if len(sys.argv) > 2 else run_all(RUN_ORDER)
    elif cmd == "repeat":
        name, k, variant, n = sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
        for rep in range(1, n + 1):
            one_run(name, k, variant, rep=rep)
