import json

from pygridplan.__main__ import main
from pygridplan.export.report import write_report
from pygridplan.export.svg import plan_to_svg
from pygridplan.generators.cpsat import Alternative
from pygridplan.model.catalog import load_catalog
from pygridplan.model.plan import load_plan
from pygridplan.model.request import Request, RoomRequest
from pygridplan.scoring.score import score_plan
from test_request import BASIC_PROGRAM


def _alternative(plan):
    req = Request(site=plan.site, rooms=tuple(RoomRequest(id=r.id, type=r.type) for r in plan.rooms))
    return Alternative(plan=plan, score=score_plan(plan, req, load_catalog()), warnings=())


def test_svg_has_one_rect_per_room_plus_lot(basic_house):
    svg = plan_to_svg(basic_house, load_catalog())
    assert svg.startswith("<svg")
    assert svg.count("<rect") == len(basic_house.rooms) + 1
    assert "Sala de estar" in svg


def test_report_has_one_svg_per_alternative(basic_house, tmp_path):
    path = tmp_path / "report.html"
    write_report([_alternative(basic_house), _alternative(basic_house)], load_catalog(), path)
    html = path.read_text(encoding="utf-8")
    assert html.count("<svg") == 2
    assert "Compacidade" in html


def test_cli_generate_writes_files(tmp_path, capsys):
    out = tmp_path / "m1"
    assert main(["generate", str(BASIC_PROGRAM), str(out), "--k", "2", "--time-limit", "0.5"]) == 0
    for name in ("alt-1.json", "alt-1.dxf", "alt-2.json", "alt-2.dxf", "report.html"):
        assert (out / name).exists(), name
    assert len(load_plan(out / "alt-1.json").rooms) == 8
    assert "alt-1" in capsys.readouterr().out


def test_cli_generate_reports_error(tmp_path, capsys):
    request = {"site": {"width_mm": 5000, "depth_mm": 5000},
               "rooms": [{"id": "s", "type": "sala"}, {"id": "q1", "type": "quarto"}, {"id": "q2", "type": "quarto"}]}
    path = tmp_path / "big.json"
    path.write_text(json.dumps(request), encoding="utf-8")
    assert main(["generate", str(path), str(tmp_path / "o"), "--time-limit", "0.5"]) == 1
    assert "caber" in capsys.readouterr().err


def test_cli_survives_windows_cp1252_console(tmp_path):
    import os
    import subprocess
    import sys

    # o stdout é estrito no Windows (cp1252); a saída de sucesso não pode quebrar com caracteres fora dele
    request = {"site": {"width_mm": 10000, "depth_mm": 25000}, "rooms": [{"id": "s", "type": "sala"}]}
    path = tmp_path / "one.json"
    path.write_text(json.dumps(request), encoding="utf-8")
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    run = subprocess.run([sys.executable, "-m", "pygridplan", "generate", str(path), str(tmp_path / "o"),
                          "--k", "1", "--time-limit", "0.5"], capture_output=True, env=env)
    assert b"Traceback" not in run.stderr
    assert run.returncode == 0


def test_cli_invalid_request_shows_message_not_traceback(tmp_path, capsys):
    request = {"site": {"width_mm": 10000, "depth_mm": 25000}, "rooms": [{"id": "s", "type": "sala"}],
               "relations": [{"a": "s", "b": "x", "kind": "near", "intensity": 3}]}
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(request), encoding="utf-8")
    assert main(["generate", str(path), str(tmp_path / "o")]) == 1
    err = capsys.readouterr().err
    assert "ERRO" in err and "inexistente" in err


def test_cli_rejects_k_zero(tmp_path):
    import pytest

    with pytest.raises(SystemExit):
        main(["generate", str(BASIC_PROGRAM), str(tmp_path / "o"), "--k", "0"])
