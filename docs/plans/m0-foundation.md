# M0 — Fundação: plano de implementação

Versão: 1.0 · Criado em: 2026-11-11 · Status: **aguardando revisão do responsável**

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: usar `superpowers:subagent-driven-development` ou `superpowers:executing-plans` para executar tarefa por tarefa. Os passos usam checkbox (`- [ ]`). Seguir também `karpathy-guidelines` (CLAUDE.md).

**Objetivo:** ter o modelo central de uma planta, o catálogo de tipos de cômodo, o validador geométrico e a exportação DXF funcionando e testados, a partir de uma planta escrita à mão, sem gerador ainda.

**Arquitetura:** pacote Python em layout `src/`. Entidades em Pydantic (uma definição serve para validar e para serializar em JSON). As paredes **não são armazenadas**: são derivadas dos retângulos dos cômodos (modelo de eixos, design 6.1). O catálogo de tipos de cômodo é um YAML em `data/`, fonte única de zona, passagem e mínimos. O validador separa **erros de validade** (inegociáveis) de **avisos de recomendação** (negociáveis).

**Stack:** Python ≥ 3.13 · pydantic 2 · PyYAML · ezdxf · OR-Tools (só teste de instalação no M0) · pytest · pyright.

**Spec:** [docs/design/mvp.md](../design/mvp.md) — seções 5.1, 5.2, 5.5, 6.1, 6.2, 10, 13, 14, 15, 16 (M0), 17.

## Restrições globais

- Unidade interna: **milímetros inteiros** (`int`) em todo o modelo. Áreas em mm² (`int`); só a exibição converte para m².
- Sistema de coordenadas: origem no **canto frente-esquerda** do terreno, visto da rua. `x` cresce ao longo da frente (largura), `y` cresce da frente para o fundo (profundidade). "Esquerda" = `x = 0`; "fundo" = `y = depth_mm`.
- Espessuras de parede padrão: externa **150 mm**, interna **100 mm** (campos do `Plan`, não constantes espalhadas).
- Cômodos são retângulos **nos eixos das paredes**; tocar pela aresta é permitido e gera parede; interseção de interiores é erro.
- Dependências de execução: `pydantic>=2.14`, `pyyaml>=6.0`, `ezdxf>=1.4`, `ortools>=9.15`. Dev: `pytest>=9`. Nenhuma outra sem registro no DECISOES.md.
- Nada de rede em tempo de execução.
- Identificadores de código e nomes de arquivo em inglês; mensagens ao usuário e nomes de exibição em português. IDs de tipo de cômodo em português ASCII snake_case (`quarto`, `home_theater`).
- Layers DXF (exatamente estes 10): `A-TERRENO`, `A-PAREDES-EXT`, `A-PAREDES-INT`, `A-PORTAS`, `A-JANELAS`, `A-MOBILIARIO`, `A-COTAS`, `A-TEXTOS`, `A-AREAS`, `A-AVISOS`. Unidade do DXF: mm (`$INSUNITS = 4`).
- **Commits (DEC-0053):** cada passo "Commit" significa **propor** o commit ao responsável (mensagem + arquivos). Só commitar após confirmação. Push é do responsável.

## Foco de revisão

Casos que o spec implica e que mais provavelmente quebram algo; cada um tem teste na tarefa dona:

1. Cômodos que se tocam **só no canto** (contato de comprimento zero): não é sobreposição nem parede → Tarefa 4 (`test_corner_touch_is_not_a_wall`).
2. Cômodo encostado na divisa do terreno: o eixo cabe, mas a meia parede externa (75 mm) sai do lote → erro `outside_lot` → Tarefa 5.
3. Tipo de cômodo fora do catálogo ("quadra_de_areia"): não quebra, é atravessável e sem mínimos → Tarefa 3.
4. Lado de cômodo **parcialmente** compartilhado (parte interna, parte externa): a área útil usa a espessura externa naquele lado → Tarefa 4.
5. Planta vazia (só terreno) e IDs de cômodo duplicados: vazia é válida e exporta só o terreno; IDs duplicados são rejeitados ao carregar → Tarefas 2 e 6.

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `pyproject.toml` | pacote, dependências, config. do pytest e do pyright |
| `src/pygridplan/__init__.py` | versão do pacote |
| `src/pygridplan/__main__.py` | CLI mínima (`export-dxf`) |
| `src/pygridplan/model/plan.py` | `Rect`, `Setbacks`, `Site`, `Room`, `Plan`, `load_plan`, `save_plan` |
| `src/pygridplan/model/walls.py` | `Wall`, `derive_walls`, `useful_dims_mm`, `useful_area_mm2` |
| `src/pygridplan/model/catalog.py` | `RoomType`, `Catalog`, `load_catalog` |
| `src/pygridplan/validation/checks.py` | `Issue`, `validate_geometry`, `check_recommendations` |
| `src/pygridplan/export/dxf.py` | `LAYERS`, `export_dxf` |
| `data/room_types.yaml` | catálogo de tipos de cômodo |
| `tests/fixtures/plans/basic-house.json` | planta de referência escrita à mão |
| `tests/test_*.py` | um arquivo de teste por módulo |

Os `__init__.py` de `model/`, `validation/` e `export/` ficam vazios.

---

### Tarefa 1: Esqueleto do pacote e testes de instalação

**Arquivos:**
- Criar: `pyproject.toml`, `src/pygridplan/__init__.py`, `tests/test_dependencies.py`
- Modificar: `README.md` (seção "Requisitos, instalação e execução")

**Interfaces:**
- Produz: pacote importável `pygridplan` com `__version__ = "0.0.1"`; ambiente `.venv` com as dependências.

- [ ] **Passo 1: Criar `pyproject.toml`**

Backend `setuptools>=69` (descobre `src/` sozinho). `requires-python = ">=3.13"`. Dependências da seção "Restrições globais"; extra `dev = ["pytest>=9"]`. `[tool.pytest.ini_options] testpaths = ["tests"]`. `[tool.pyright] venvPath = "."`, `venv = ".venv"`, `include = ["src"]`.

- [ ] **Passo 2: Criar o ambiente e instalar**

Run: `python -m venv .venv` e `.venv/Scripts/python -m pip install -e ".[dev]"`
Esperado: termina com `Successfully installed ... pygridplan-0.0.1 ...`

- [ ] **Passo 3: Escrever os testes de instalação**

```python
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
```

- [ ] **Passo 4: Rodar**

Run: `.venv/Scripts/python -m pytest tests/test_dependencies.py -v`
Esperado: primeiro FAIL em `test_package_imports` (sem `__init__.py`); depois de criar `src/pygridplan/__init__.py` com `__version__`, 3 PASS.

- [ ] **Passo 5: Documentar a instalação no README**

Substituir a seção por: requisitos (Python ≥ 3.13), os comandos do passo 2 (com a ativação `.venv\Scripts\activate` no Windows) e `pytest` para rodar os testes. Uma frase explicando que `pip install -e` instala dependências e o pacote de uma vez, em modo editável.

- [ ] **Passo 6: Commit** — `build: add package skeleton and dependency smoke tests` (`pyproject.toml`, `src/pygridplan/__init__.py`, `tests/test_dependencies.py`, `README.md`)

---

### Tarefa 2: Modelo da planta

**Arquivos:**
- Criar: `src/pygridplan/model/__init__.py`, `src/pygridplan/model/plan.py`, `tests/fixtures/plans/basic-house.json`, `tests/test_plan.py`

**Interfaces:**
- Produz (todos `pydantic.BaseModel`, `frozen=True`):
  - `Rect(x: int, y: int, w: int, h: int)` — `w`, `h` com `gt=0`. Propriedades `x2 -> int`, `y2 -> int`, `area_mm2 -> int`. Métodos `overlaps_interior(other: Rect) -> bool`, `expanded(d: int) -> Rect`, `contains(other: Rect) -> bool`.
  - `Setbacks(front: int = 0, back: int = 0, left: int = 0, right: int = 0)` — todos `ge=0`.
  - `Site(width_mm: int, depth_mm: int, setbacks: Setbacks = Setbacks(), attached_sides: frozenset[Literal["left", "right", "back"]] = frozenset())` — dimensões `gt=0`.
  - `Room(id: str, type: str, rect: Rect, floor: int = 0)` — `id` com `min_length=1`.
  - `Plan(site: Site, rooms: tuple[Room, ...] = (), wall_ext_mm: int = 150, wall_int_mm: int = 100)` — rejeita IDs de cômodo duplicados.
  - `load_plan(path: Path) -> Plan`, `save_plan(plan: Plan, path: Path) -> None` (JSON UTF-8, indentado).

- [ ] **Passo 1: Criar a fixture `basic-house.json`**

Terreno 10 000 × 25 000; recuos frente 4 000, fundo 2 000, laterais 1 500; nada encostado. Cômodos (`id`, `type`, `x`, `y`, `w`, `h`), todos na grade de 100 mm, formando um bloco de 6 800 × 10 000:

| id | type | x | y | w | h |
|---|---|---|---|---|---|
| sala | sala | 1600 | 4100 | 4000 | 4000 |
| cozinha | cozinha | 5600 | 4100 | 2800 | 4000 |
| circulacao | circulacao | 1600 | 8100 | 6800 | 1000 |
| quarto1 | quarto | 1600 | 9100 | 2700 | 5000 |
| banheiro | banheiro | 4300 | 9100 | 1400 | 2500 |
| closet | closet | 4300 | 11600 | 1400 | 2500 |
| quarto2 | quarto | 5700 | 9100 | 2700 | 5000 |

Essa planta é **válida e sem avisos** (as tarefas 4 a 6 dependem disso).

- [ ] **Passo 2: Escrever os testes**

`test_rect_overlap_rules` (interseção de interior → `True`; tocar pela aresta → `False`; tocar pelo canto → `False`), `test_rect_expanded` (`Rect(0,0,10,10).expanded(5) == Rect(-5,-5,20,20)`), `test_rect_rejects_non_positive_size` (`ValidationError` para `w=0`), `test_plan_rejects_duplicate_room_ids`, `test_load_basic_house` (7 cômodos; `site.width_mm == 10000`), `test_save_load_roundtrip` (`load_plan(save) == original`), `test_empty_plan_is_allowed` (`Plan(site=...)` sem cômodos).

- [ ] **Passo 3: Rodar** — `pytest tests/test_plan.py -v` → FAIL (módulo inexistente).
- [ ] **Passo 4: Implementar `plan.py`** com as interfaces acima.
- [ ] **Passo 5: Rodar** — `pytest tests/test_plan.py -v` → 7 PASS.
- [ ] **Passo 6: Commit** — `feat: add plan data model with JSON persistence`

---

### Tarefa 3: Catálogo de tipos de cômodo

**Arquivos:**
- Criar: `data/room_types.yaml`, `src/pygridplan/model/catalog.py`, `tests/test_catalog.py`

**Interfaces:**
- Produz:
  - `RoomType(id: str, name: str, zone: Literal["social", "intima", "servico"], passage: Literal["private", "traversable"], min_width_mm: int | None = None, min_area_m2: float | None = None, source: str)`
  - `Catalog(version: str, updated: str, types: dict[str, RoomType])` com `get(type_id: str) -> RoomType`. Tipo desconhecido devolve `RoomType(id=type_id, name=type_id, zone="social", passage="traversable", source="tipo personalizado")` (design 5.5).
  - `DEFAULT_CATALOG_PATH: Path` = `<raiz do repo>/data/room_types.yaml`; `load_catalog(path: Path = DEFAULT_CATALOG_PATH) -> Catalog`.

- [ ] **Passo 1: Criar `data/room_types.yaml`**

Cabeçalho `version: "0.1"`, `updated: "2026-11-11"`; lista `types`. Todos com `source: "provisório, sem fonte"` (design 5.2):

| id | name | zone | passage | min_width_mm | min_area_m2 |
|---|---|---|---|---|---|
| sala | Sala | social | traversable | 2700 | 10.0 |
| cozinha | Cozinha | servico | traversable | 1800 | 5.0 |
| quarto | Quarto | intima | private | 2400 | 8.0 |
| banheiro | Banheiro | intima | private | 1200 | 2.5 |
| lavabo | Lavabo | social | private | 900 | 1.5 |
| closet | Closet | intima | private | 1000 | 2.0 |
| lavanderia | Lavanderia | servico | traversable | 1200 | 3.0 |
| garagem | Garagem | servico | traversable | 2500 | 12.5 |
| circulacao | Circulação | social | traversable | 900 | — |
| escritorio | Escritório | social | traversable | 2200 | 6.0 |
| varanda | Varanda | social | traversable | 1200 | 3.0 |
| home_theater | Home theater | social | traversable | 3000 | 12.0 |

- [ ] **Passo 2: Escrever os testes**

`test_default_catalog_loads` (12 tipos; `version == "0.1"`), `test_private_types` (`{t.id for t in types if passage == "private"} == {"quarto", "banheiro", "lavabo", "closet"}`), `test_unknown_type_is_traversable_without_minimums` (`get("quadra_de_areia")`: `passage == "traversable"`, `min_width_mm is None`, `min_area_m2 is None`), `test_every_type_has_source`, `test_invalid_zone_is_rejected` (YAML em `tmp_path` com `zone: "x"` → `ValidationError`).

- [ ] **Passo 3: Rodar** → FAIL. **Passo 4: Implementar** `catalog.py` (`yaml.safe_load` + validação Pydantic). **Passo 5: Rodar** → 5 PASS.
- [ ] **Passo 6: Commit** — `feat: add room type catalog as single source of room data`

---

### Tarefa 4: Paredes derivadas e área útil

**Arquivos:**
- Criar: `src/pygridplan/model/walls.py`, `tests/test_walls.py`

**Interfaces:**
- Consome: `Plan`, `Room`, `Rect` (Tarefa 2).
- Produz:
  - `Wall(x1: int, y1: int, x2: int, y2: int, thickness_mm: int, kind: Literal["ext", "int"], room_ids: tuple[str, ...])` — segmento de eixo, horizontal ou vertical, `frozen`.
  - `derive_walls(plan: Plan) -> list[Wall]`
  - `useful_dims_mm(room: Room, plan: Plan) -> tuple[int, int]` (largura útil, profundidade útil)
  - `useful_area_mm2(room: Room, plan: Plan) -> int`

Regras (design 6.1):
- Para cada par de cômodos, o trecho de aresta colinear em comum com **comprimento > 0** é uma parede `int` (`room_ids` com os dois, em ordem de `plan.rooms`). Cada trecho aparece uma vez.
- Para cada lado de cada cômodo, os trechos **não cobertos** por vizinhos são paredes `ext` (`room_ids` com um).
- No M0, segmentos colineares contíguos **não** são fundidos.
- Área útil: cada lado desconta metade da espessura; se **qualquer** trecho do lado for externo, usa a espessura externa naquele lado (conservador).

- [ ] **Passo 1: Escrever os testes**

`test_basic_house_wall_counts` (`basic-house`: 11 `int`, 11 `ext`), `test_shared_wall_between_sala_and_cozinha` (existe `Wall(5600, 4100, 5600, 8100, 100, "int", ("sala", "cozinha"))`), `test_corner_touch_is_not_a_wall` (`Rect(0,0,1000,1000)` e `Rect(1000,1000,1000,1000)`: 0 paredes `int`, 8 `ext`), `test_useful_area_sala` (`useful_dims_mm == (3875, 3875)`; área `15_015_625`), `test_useful_dims_banheiro_all_interior` (`(1300, 2400)`), `test_partially_shared_side_uses_external_thickness` (cômodo A `Rect(0,0,2000,2000)` e B `Rect(2000,0,2000,1000)`: lado direito de A é parcialmente externo → largura útil de A = `2000 - 75 - 75 = 1850`).

- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar** `walls.py` (operações de intervalo 1D sobre cada lado; nenhuma biblioteca de geometria). **Passo 4: Rodar** → 6 PASS.
- [ ] **Passo 5: Commit** — `feat: derive walls and useful area from room rectangles`

---

### Tarefa 5: Validador

**Arquivos:**
- Criar: `src/pygridplan/validation/__init__.py`, `src/pygridplan/validation/checks.py`, `tests/test_checks.py`

**Interfaces:**
- Consome: `Plan`, `Rect` (T2), `Catalog` (T3), `useful_dims_mm`, `useful_area_mm2` (T4).
- Produz:
  - `Issue(code: str, message: str, room_ids: tuple[str, ...] = (), recommended: float | None = None, actual: float | None = None)`, `frozen`.
  - `validate_geometry(plan: Plan) -> list[Issue]` — **erros** (design 5.1). Códigos: `overlap` (um por par com interiores sobrepostos), `outside_lot` (cômodo cujo `rect.expanded(wall_ext_mm // 2)` não cabe em `Rect(0, 0, width, depth)`).
  - `check_recommendations(plan: Plan, catalog: Catalog) -> list[Issue]` — **avisos** (design 5.2). Códigos: `setback` (o retângulo expandido invade o recuo de um lado não listado em `attached_sides`; a frente sempre tem recuo), `min_width` (menor dimensão útil < `min_width_mm`), `min_area` (área útil < `min_area_m2`). `recommended` e `actual` em mm ou m², conforme o código.
- Mensagens em português, citando o cômodo e os dois valores (ex.: `"quarto2: largura útil 2 275 mm < 2 400 mm recomendados"`).

- [ ] **Passo 1: Escrever os testes**

`test_basic_house_is_valid_and_clean` (as duas funções devolvem `[]`), `test_overlap_detected` (dois cômodos sobrepostos → um `Issue` `overlap` com os dois IDs), `test_room_on_lot_edge_is_outside` (cômodo em `x=0` → `outside_lot`), `test_setback_warning_unless_attached` (casa a 75 mm da divisa esquerda → `setback`; com `attached_sides={"left"}` → nenhum `setback`), `test_min_width_warning` (quarto com 2 300 mm de largura de eixo → `min_width` com `recommended == 2400`), `test_unknown_type_has_no_minimum_warnings`.

- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar** `checks.py`. **Passo 4: Rodar** → 6 PASS.
- [ ] **Passo 5: Commit** — `feat: add geometric validator and recommendation checks`

---

### Tarefa 6: Exportador DXF e CLI

**Arquivos:**
- Criar: `src/pygridplan/export/__init__.py`, `src/pygridplan/export/dxf.py`, `src/pygridplan/__main__.py`, `tests/test_dxf.py`

**Interfaces:**
- Consome: `Plan`, `load_plan` (T2), `Catalog`, `load_catalog` (T3), `derive_walls`, `useful_area_mm2` (T4).
- Produz:
  - `LAYERS: tuple[str, ...]` — os 10 layers das restrições globais, nessa ordem.
  - `export_dxf(plan: Plan, path: Path, catalog: Catalog) -> None` — DXF R2010, `$INSUNITS = 4`; cria todos os `LAYERS`.
  - `main(argv: list[str] | None = None) -> int` em `__main__.py`: `python -m pygridplan export-dxf PLANO.json SAIDA.dxf`; cria a pasta da saída; devolve 0.

Conteúdo do DXF:
- `A-TERRENO`: uma `LWPOLYLINE` fechada com os 4 cantos do lote.
- `A-PAREDES-EXT` / `A-PAREDES-INT`: uma `LWPOLYLINE` fechada por `Wall` — faixa de largura `thickness_mm` centrada no eixo.
- `A-AREAS`: uma `LWPOLYLINE` fechada por cômodo (retângulo de eixo).
- `A-TEXTOS`: um `TEXT` por cômodo, no centro, altura 200, conteúdo `f"{nome} {área útil em m², 2 casas, vírgula decimal} m²"` (ex.: `"Sala 15,02 m²"`).
- `A-COTAS`: duas cotas lineares do terreno (design 11, DEC-0044): largura ao longo da frente (deslocada 1 000 mm para fora, em `y < 0`) e profundidade ao longo do lado esquerdo (deslocada 1 000 mm, em `x < 0`).
- Demais layers ficam vazios no M0.

- [ ] **Passo 1: Escrever os testes** (exportar `basic-house` em `tmp_path` e reler com `ezdxf.readfile`)

`test_all_layers_exist`, `test_units_are_mm` (`doc.header["$INSUNITS"] == 4`), `test_lot_outline` (1 polilinha fechada em `A-TERRENO` com os vértices `(0,0)`, `(10000,0)`, `(10000,25000)`, `(0,25000)`), `test_wall_entities_per_layer` (11 em cada layer de parede), `test_room_texts` (7 `TEXT`; um é `"Sala 15,02 m²"`), `test_lot_dimensions` (2 `DIMENSION` em `A-COTAS`; medidas `{10000, 25000}`), `test_empty_plan_exports_lot_only` (0 entidades nos layers de parede e texto), `test_cli_exports_file` (`main(["export-dxf", fixture, tmp_path/"x"/"p.dxf"]) == 0` e o arquivo existe).

- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar** `dxf.py` (`msp.add_lwpolyline(..., close=True)`, `msp.add_text`, `msp.add_linear_dim(...).render()`) e `__main__.py` (`argparse`). **Passo 4: Rodar** → 8 PASS.
- [ ] **Passo 5: Verificação final do M0**

Run: `.venv/Scripts/python -m pytest -v` → todos os testes passam (3 + 7 + 5 + 6 + 6 + 8 = 35).
Run: `pyright` → `0 errors`.
Run: `.venv/Scripts/python -m pygridplan export-dxf tests/fixtures/plans/basic-house.json out/basic-house.dxf` → abrir o arquivo num visualizador DXF e conferir com o responsável (o screenshot é a evidência visual do M0).

- [ ] **Passo 6: Commit** — `feat: export plans to DXF with organized layers and CLI`
- [ ] **Passo 7: Fechamento** — atualizar o README (estado atual; pastas ✅), registrar no DECISOES.md e propor o commit `docs: close M0`.

---

## Fora do escopo do M0

Gerador, pontuação, árvore de estados (M1); portas, janelas e alcançabilidade (M4); fusão de segmentos de parede colineares e limpeza dos cantos das faixas de parede no DXF (estética; quando o DXF for avaliado no M2); geometria em polígono genérico (quando terrenos irregulares entrarem — no M0 o `Room` guarda um `Rect`).
