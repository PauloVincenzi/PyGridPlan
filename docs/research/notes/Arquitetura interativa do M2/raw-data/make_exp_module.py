"""Gera cpsat_exp.py: cópia textual de src/pygridplan/generators/cpsat.py com patches mínimos e verificados.

Os patches (marcados com "# EXP") só acrescentam: travas de cômodos, dica (AddHint) ou fixação da dica,
callback de primeira solução e coleta de estatísticas. Nenhuma linha do modelo original é alterada.
Rodar: python make_exp_module.py  (escreve cpsat_exp.py e cpsat_exp.diff ao lado)
"""

import difflib
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(r"c:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan\src\pygridplan\generators\cpsat.py")

PATCHES = [
    ("import math\n", "import math\nimport time  # EXP\n"),
    (
        "           shape: tuple[int, float] = SHAPE_ATTEMPTS[0]) -> tuple[Plan | None, str, list[int]]:\n",
        "           shape: tuple[int, float] = SHAPE_ATTEMPTS[0],\n"
        "           locks=None, hint=None, fix_hint=False, stats=None) -> tuple[Plan | None, str, list[int]]:  # EXP\n",
    ),
    ("    max_voids, cap_factor = shape\n", "    _t_start = time.perf_counter()  # EXP\n    max_voids, cap_factor = shape\n"),
    (
        "    # objetivo (pesos de scoring.WEIGHTS)\n",
        "    _exp_n_prefix = _exp_lock_and_hint(m, reqs, cells, w, h, locks, hint, fix_hint, stats)  # EXP\n"
        "    # objetivo (pesos de scoring.WEIGHTS)\n",
    ),
    (
        "    solver = cp_model.CpSolver()\n",
        "    _exp_full_hint(m, hint, stats)  # EXP\n    solver = cp_model.CpSolver()\n",
    ),
    (
        "    status = solver.solve(m)\n",
        "    _cb = _FirstSolution()  # EXP\n"
        "    _t_solve = time.perf_counter()  # EXP\n"
        "    status = solver.solve(m, _cb)  # EXP (original: solver.solve(m))\n"
        "    _exp_stats(stats, solver, status, _cb, _t_start, _t_solve, m, _exp_n_prefix)  # EXP\n",
    ),
]

APPENDIX = '''

# ---------------------------------------------------------------- EXP: código só do experimento
class _FirstSolution(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        super().__init__()
        self.t0 = time.perf_counter()
        self.first_s = None
        self.first_obj = None
        self.count = 0

    def on_solution_callback(self):
        if self.first_s is None:
            self.first_s = time.perf_counter() - self.t0
            self.first_obj = self.objective_value
        self.count += 1


def _exp_lock_and_hint(m, reqs, cells, w, h, locks, hint, fix_hint, stats):
    """Travas: x, y, w, h (unidades de GRID) do cômodo iguais aos valores dados. Dica: valores da planta-base
    para as variáveis criadas antes do objetivo (mesma ordem de criação => mesmo índice no proto)."""
    n_prefix = len(m.proto.variables)
    for k, r in enumerate(reqs):
        if locks and r.id in locks:
            lx, ly, lw, lh = locks[r.id]
            m.add(cells[k].x == lx)
            m.add(cells[k].y == ly)
            m.add(w[k] == lw)
            m.add(h[k] == lh)
    mode = None
    if hint is not None:
        if hint["n_prefix"] == n_prefix:
            mode = "index"
            pairs = list(enumerate(hint["values"]))
        else:  # outro formato de malha (ex.: tentativa com recortes): só as variáveis com nome
            mode = "name"
            by_name = hint["names"]
            vs = m.proto.variables
            pairs = [(i, by_name[vs[i].name]) for i in range(n_prefix) if vs[i].name and vs[i].name in by_name]
        for i, value in pairs:
            var = m.get_int_var_from_proto_index(i)
            if fix_hint:
                m.add(var == value)
            else:
                m.add_hint(var, value)
        if stats is not None:
            stats["hint_mode"] = mode
            stats["hint_vars"] = len(pairs)
    if stats is not None:
        stats["n_prefix"] = n_prefix
    return n_prefix


def _exp_full_hint(m, hint, stats):
    """Dica completa: se a dica traz valores para TODAS as variáveis deste modelo, troca a dica parcial por ela."""
    if not hint or "full_values" not in hint:
        return
    vals = hint["full_values"]
    if len(vals) != len(m.proto.variables):
        if stats is not None:
            stats["full_hint"] = "size-mismatch"
        return
    m.clear_hints()
    for i, value in enumerate(vals):
        m.add_hint(m.get_int_var_from_proto_index(i), value)
    if stats is not None:
        stats["hint_mode"], stats["hint_vars"] = "full", len(vals)


def _exp_stats(stats, solver, status, cb, t_start, t_solve, m, n_prefix):
    if stats is None:
        return
    t_end = time.perf_counter()
    ok = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    stats.update(
        status=solver.status_name(status),
        build_s=t_solve - t_start,
        solve_s=t_end - t_solve,
        solver_wall_s=solver.wall_time,
        user_s=solver.user_time,
        det_time=solver.deterministic_time,
        objective=solver.objective_value if ok else None,
        bound=solver.best_objective_bound if ok else None,
        first_solution_s=cb.first_s,
        first_objective=cb.first_obj,
        n_solutions=cb.count,
        n_vars=len(m.proto.variables),
        n_constraints=len(m.proto.constraints),
    )
    if ok:
        sol = solver.response_proto.solution
        stats["full_values"] = list(sol)
        stats["prefix_values"] = list(sol)[:n_prefix]
        vs = m.proto.variables
        stats["prefix_names"] = [vs[i].name for i in range(n_prefix)]
'''


import sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "cpsat_exp.py"


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    out = src
    for old, new in PATCHES:
        assert out.count(old) == 1, old
        out = out.replace(old, new)
    out += APPENDIX
    (HERE / OUT).write_text(out, encoding="utf-8")
    diff = difflib.unified_diff(src.splitlines(True), out.splitlines(True), "cpsat.py", OUT)
    (HERE / (OUT[:-3] + ".diff")).write_text("".join(diff), encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
