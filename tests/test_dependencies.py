def test_package_imports():
    import pygridplan

    assert pygridplan.__version__ == "0.0.1"


def test_cpsat_solves_two_boxes_without_overlap():
    # dois retângulos 2x2 numa faixa 4x2: só cabem lado a lado
    from ortools.sat.python import cp_model

    m = cp_model.CpModel()
    xs = [m.new_int_var(0, 2, f"x{i}") for i in range(2)]
    xi = [m.new_fixed_size_interval_var(x, 2, f"ix{i}") for i, x in enumerate(xs)]
    yi = [m.new_fixed_size_interval_var(0, 2, f"iy{i}") for i in range(2)]
    m.add_no_overlap_2d(xi, yi)
    solver = cp_model.CpSolver()
    assert solver.solve(m) in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    assert abs(solver.value(xs[0]) - solver.value(xs[1])) == 2


def test_ezdxf_roundtrip(tmp_path):
    import ezdxf

    doc = ezdxf.new("R2010")
    doc.layers.add("A-TESTE")
    doc.modelspace().add_line((0, 0), (1000, 0), dxfattribs={"layer": "A-TESTE"})
    doc.saveas(tmp_path / "t.dxf")
    lines = ezdxf.readfile(tmp_path / "t.dxf").modelspace().query("LINE[layer=='A-TESTE']")
    assert len(lines) == 1
