"""CLI:
python -m pygridplan export-dxf PLANO.json SAIDA.dxf
python -m pygridplan generate PEDIDO.json PASTA [--k 4] [--seed 0] [--time-limit 0.5]
"""

import argparse
import io
import sys
import time
from pathlib import Path

from pydantic import ValidationError

from pygridplan.export.dxf import export_dxf
from pygridplan.export.report import write_report
from pygridplan.generators.cpsat import DEFAULT_TIME_LIMIT, GenerationError, generate_alternatives
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import load_plan, save_plan
from pygridplan.model.request import load_request
from pygridplan.validation.checks import check_recommendations, validate_geometry


def _input_error(exc: Exception) -> int:
    """Entrada inválida: mensagem em português, sem traceback."""
    if isinstance(exc, ValidationError):
        for err in exc.errors():
            where = ".".join(str(p) for p in err["loc"]) or "arquivo"
            print(f"ERRO: {where}: {err['msg']}", file=sys.stderr)
    else:
        print(f"ERRO: {exc}", file=sys.stderr)
    return 1


def _export(args: argparse.Namespace) -> int:
    try:
        plan = load_plan(args.plan)
    except (ValidationError, ValueError, OSError) as exc:
        return _input_error(exc)
    catalog = load_catalog()
    errors = validate_geometry(plan)
    for issue in errors:
        print(f"ERRO: {issue.message}", file=sys.stderr)
    if errors:
        return 1
    for issue in check_recommendations(plan, catalog):
        print(f"AVISO: {issue.message}", file=sys.stderr)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    export_dxf(plan, args.output, catalog)
    return 0


def _generate(args: argparse.Namespace) -> int:
    try:
        request = load_request(args.request)
    except (ValidationError, ValueError, OSError) as exc:
        return _input_error(exc)
    catalog = load_catalog()
    start = time.perf_counter()
    try:
        alternatives = generate_alternatives(request, catalog, k=args.k, seed=args.seed, time_limit=args.time_limit)
    except GenerationError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    args.output.mkdir(parents=True, exist_ok=True)
    for n, alt in enumerate(alternatives, 1):
        save_plan(alt.plan, args.output / f"alt-{n}.json")
        export_dxf(alt.plan, args.output / f"alt-{n}.dxf", catalog)
        print(f"alt-{n}  nota {alt.score.total:.2f}".replace(".", ",") + f"  avisos {len(alt.warnings)}")
    write_report(alternatives, catalog, args.output / "report.html")
    print(f"{len(alternatives)} alternativas em {time.perf_counter() - start:.1f} s → {args.output / 'report.html'}")
    return 0


def _positive(cast):
    def parse(text: str):
        value = cast(text)
        if value <= 0:
            raise argparse.ArgumentTypeError("precisa ser maior que zero")
        return value
    return parse


def main(argv: list[str] | None = None) -> int:
    # consoles do Windows (cp1252) não têm todos os caracteres das mensagens: substitui em vez de quebrar
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(prog="pygridplan")
    sub = parser.add_subparsers(dest="command", required=True)
    export = sub.add_parser("export-dxf", help="exporta um plano JSON para DXF")
    export.add_argument("plan", type=Path)
    export.add_argument("output", type=Path)
    gen = sub.add_parser("generate", help="gera K plantas alternativas a partir de um pedido JSON")
    gen.add_argument("request", type=Path)
    gen.add_argument("output", type=Path)
    gen.add_argument("--k", type=_positive(int), default=4)
    gen.add_argument("--seed", type=int, default=0)
    gen.add_argument("--time-limit", type=_positive(float), default=DEFAULT_TIME_LIMIT)
    args = parser.parse_args(argv)
    return _export(args) if args.command == "export-dxf" else _generate(args)


if __name__ == "__main__":
    raise SystemExit(main())
