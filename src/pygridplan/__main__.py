"""CLI: python -m pygridplan export-dxf PLANO.json SAIDA.dxf"""

import argparse
from pathlib import Path

from pygridplan.export.dxf import export_dxf
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import load_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pygridplan")
    sub = parser.add_subparsers(dest="command", required=True)
    export = sub.add_parser("export-dxf", help="exporta um plano JSON para DXF")
    export.add_argument("plan", type=Path)
    export.add_argument("output", type=Path)
    args = parser.parse_args(argv)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    export_dxf(load_plan(args.plan), args.output, load_catalog())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
