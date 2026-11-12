"""CLI: python -m pygridplan export-dxf PLANO.json SAIDA.dxf"""

import argparse
import sys
from pathlib import Path

from pygridplan.export.dxf import export_dxf
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import load_plan
from pygridplan.validation.checks import check_recommendations, validate_geometry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pygridplan")
    sub = parser.add_subparsers(dest="command", required=True)
    export = sub.add_parser("export-dxf", help="exporta um plano JSON para DXF")
    export.add_argument("plan", type=Path)
    export.add_argument("output", type=Path)
    args = parser.parse_args(argv)

    plan, catalog = load_plan(args.plan), load_catalog()
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


if __name__ == "__main__":
    raise SystemExit(main())
