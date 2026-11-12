"""Página HTML autocontida para comparar as alternativas geradas."""

from html import escape
from pathlib import Path

from pygridplan.export.svg import plan_to_svg
from pygridplan.generators.cpsat import Alternative
from pygridplan.model.catalog import Catalog

LABELS = {
    "relations": "Relações", "area_fit": "Áreas", "compactness": "Compacidade",
    "circulation": "Circulação", "solar": "Sol (norte)", "wet_grouping": "Áreas molhadas",
}
STYLE = """
body{margin:0;background:#121211;color:#ecebe6;font:14px/1.5 system-ui,sans-serif;padding:24px}
h1{font-size:20px;margin:0 0 16px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.alt{background:#1c1c1a;border:1px solid #2f2f2a;border-radius:8px;padding:12px}
.alt h2{font-size:16px;margin:0 0 8px}.alt h2 b{color:#d97757}svg{width:100%;height:420px;background:#121211}
table{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px}td{padding:2px 4px;border-top:1px solid #2f2f2a}
td.v{text-align:right;font-family:ui-monospace,monospace}.warn{color:#d98a7a;font-size:12px}
"""


def _fmt(v: float) -> str:
    return f"{v:.2f}".replace(".", ",")


def write_report(alternatives: list[Alternative], catalog: Catalog, path: Path) -> None:
    cards = []
    for n, alt in enumerate(alternatives, 1):
        rows = "".join(
            f"<tr><td>{LABELS.get(c.name, c.name)}</td><td class='v'>{_fmt(c.value)}</td>"
            f"<td class='v'>peso {_fmt(c.weight)}</td></tr>"
            for c in alt.score.criteria
        )
        warns = "".join(f"<div class='warn'>⚠ {escape(w.message)}</div>" for w in alt.warnings)
        cards.append(
            f"<section class='alt'><h2>Alternativa {n} — nota <b>{_fmt(alt.score.total)}</b></h2>"
            f"{plan_to_svg(alt.plan, catalog)}<table>{rows}</table>{warns}</section>"
        )
    html = (
        "<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>PyGridPlan — alternativas</title><style>{STYLE}</style></head><body>"
        f"<h1>PyGridPlan — {len(alternatives)} alternativas</h1><div class='grid'>{''.join(cards)}</div></body></html>"
    )
    Path(path).write_text(html, encoding="utf-8")
