# M1 — Gerador CP-SAT: plano de implementação

Versão: 1.0 · Criado em: 2026-11-11 · Status: **aguardando revisão do responsável**

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: usar `superpowers:subagent-driven-development` ou `superpowers:executing-plans` para executar tarefa por tarefa. Os passos usam checkbox (`- [ ]`). Seguir também `karpathy-guidelines` e `superpowers:test-driven-development` (CLAUDE.md).

**Objetivo:** a partir de um **pedido** (terreno + programa de cômodos + relações), gerar **K plantas alternativas, válidas e diferentes entre si**, cada uma com uma nota decomposta por critério, e entregá-las em JSON, DXF e numa página HTML de comparação, tudo pela linha de comando.

**Arquitetura:** o CP-SAT resolve a etapa 1 (posição e tamanho dos retângulos na grade de 100 mm). Cada solução passa pelo validador do M0 e por uma checagem de acesso; soluções rejeitadas ou repetidas são proibidas e o solver roda de novo. A diversidade é garantida **por construção**: cada nova solução precisa diferir das anteriores no padrão de posições relativas entre cômodos. A nota é calculada em Python, separada do solver, com os **mesmos pesos** usados na função objetivo.

**Stack:** o do M0 (pydantic, PyYAML, ezdxf, OR-Tools CP-SAT, pytest). Nenhuma dependência nova.

**Spec:** [docs/design/mvp.md](../design/mvp.md) — seções 4.4, 5.1–5.6, 6.1, 6.2, 8, 9, 10, 16.

## Restrições globais

- Tudo do M0 continua valendo (mm inteiros, origem no canto frente-esquerda, espessuras 150/100 mm, layers do DXF).
- Grade do solver: **100 mm**. Todas as coordenadas e dimensões geradas são múltiplas de 100.
- **Recuos e mínimos são restrições rígidas** no solver até existir a negociação (design 5.2, M6).
- Passagem mínima entre dois cômodos para contar como acesso ou adjacência: **900 mm** de parede compartilhada (`MIN_PASSAGE_MM`, definido uma única vez em `validation/access.py`).
- K padrão: **4** (design 4.4). Diversidade mínima padrão: as alternativas diferem em pelo menos **15 %** dos pares de cômodos (arredondado para cima, mínimo 1).
- **Reprodutível:** mesmo pedido + mesma semente = mesmas plantas. Usar limite de **tempo determinístico** do CP-SAT (`max_deterministic_time`), nunca tempo de relógio.
- Meta de desempenho (design 8): 8–12 cômodos → até ~5 s por alternativa e ~20 s para K = 4 no hardware de referência. Medir e relatar; o teste não depende do relógio.
- Mensagens ao usuário em português; código em inglês.
- **Commits:** autorizados pelo responsável durante a execução (DEC-0053 com a autorização da S03); o push é do responsável.

## Foco de revisão

1. Programa que **não cabe** no terreno com os recuos → erro claro (`GenerationError`) em segundos, sem travar → Tarefa 6.
2. Relação citando cômodo inexistente, ou um cômodo com ele mesmo → erro ao carregar o pedido → Tarefa 2.
3. Programa **sem cômodo atravessável** (ex.: só quartos) → erro claro "falta um cômodo para a entrada" → Tarefa 6.
4. Programa pequeno em que **não existem K alternativas diferentes** → devolve menos de K, sem erro → Tarefa 6.
5. Mesmo pedido e mesma semente rodados duas vezes → plantas idênticas → Tarefa 6.

## Mapa de arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `src/pygridplan/__main__.py` | CLI: `export-dxf` valida; novo `generate` | 1, 7 |
| `src/pygridplan/model/catalog.py`, `data/room_types.yaml` | IDs duplicados; atributos `suite_access`, `wet`, `sun` | 1, 3, 4 |
| `src/pygridplan/model/plan.py` | `Site.north` | 2 |
| `src/pygridplan/model/request.py` | pedido: `RoomRequest`, `Relation`, `Request`, `load_request` | 2 |
| `src/pygridplan/validation/access.py` | entrada e alcançabilidade potencial | 3 |
| `src/pygridplan/scoring/score.py` | critérios, pesos, nota decomposta | 4 |
| `src/pygridplan/scoring/diversity.py` | padrão relativo e distância entre plantas | 4 |
| `src/pygridplan/generators/cpsat.py` | modelo CP-SAT, laço de alternativas | 5, 6 |
| `src/pygridplan/export/svg.py`, `export/report.py` | SVG de uma planta e página de comparação | 7 |
| `tests/fixtures/requests/basic-program.json` | pedido de referência | 2 |

---

### Tarefa 1: Pendências do M0

**Arquivos:** modificar `src/pygridplan/__main__.py`, `src/pygridplan/model/catalog.py`; testes em `tests/test_dxf.py`, `tests/test_catalog.py`, `tests/test_plan.py`.

**Interfaces:**
- `export-dxf`: roda `validate_geometry` e `check_recommendations`. Com **erros**, imprime cada um em `stderr` (`ERRO: <mensagem>`), **não** gera o arquivo e devolve 1. Com só **avisos**, imprime `AVISO: <mensagem>`, gera o arquivo e devolve 0.
- `load_catalog` levanta `ValueError("ID de tipo duplicado no catálogo: <id>")`.

- [ ] **Passo 1: Testes** — `test_cli_rejects_invalid_plan` (plano com dois cômodos sobrepostos em `tmp_path` → `main(...) == 1`, arquivo não existe, `"ERRO"` em `capsys.readouterr().err`), `test_cli_prints_warnings` (plano com quarto de 2 300 mm → `0`, arquivo existe, `"AVISO"` no `stderr`), `test_duplicate_catalog_ids_rejected` (`pytest.raises(ValueError)`), `test_duplicate_room_ids_rejected_on_load` (JSON com dois `"id": "a"` → `load_plan` levanta `ValidationError`).
- [ ] **Passo 2: Rodar** → os três primeiros FAIL; o quarto já passa (o comportamento existe, o teste só fixa o caminho pelo arquivo — registrar no ledger).
- [ ] **Passo 3: Implementar.** **Passo 4: Rodar** `pytest -q` → tudo passa.
- [ ] **Passo 5: Commit** — `fix: validate plans in CLI export and reject duplicate catalog ids`

---

### Tarefa 2: Pedido (programa de necessidades)

**Arquivos:** criar `src/pygridplan/model/request.py`, `tests/fixtures/requests/basic-program.json`, `tests/test_request.py`; modificar `src/pygridplan/model/plan.py`.

**Interfaces** (todos com `frozen=True, extra="forbid"`, como no M0):
- `Site.north: Literal["front", "back", "left", "right"] | None = None` — qual lado do **terreno** fica voltado para o norte. `None` desliga o critério solar.
- `RoomRequest(id: str, type: str, target_area_m2: float | None = None)` — `id` com `min_length=1`; `target_area_m2 > 0` quando informado.
- `Relation(a: str, b: str, kind: Literal["near", "far"], intensity: int)` — `intensity` de 1 a 5 (design 5.3: aproximar/afastar, 1–5).
- `Request(site: Site, rooms: tuple[RoomRequest, ...], relations: tuple[Relation, ...] = ())` — pelo menos 1 cômodo; IDs únicos; toda relação cita IDs existentes; `a != b`; no máximo uma relação por par (sem ordem).
- `load_request(path: Path) -> Request`.

Fixture `basic-program.json`: terreno igual ao `basic-house` (10 000 × 25 000, recuos 4 000 / 2 000 / 1 500 / 1 500), `north: "back"`, 8 cômodos: `sala` (sala, 16), `cozinha` (cozinha, 10), `lavanderia` (lavanderia), `circulacao` (circulacao), `quarto1` (quarto, 12), `quarto2` (quarto, 10), `banheiro` (banheiro), `closet` (closet). Relações: cozinha–sala near 4; lavanderia–cozinha near 4; closet–quarto1 near 5; banheiro–circulacao near 3; sala–quarto2 far 2.

- [ ] **Passo 1: Testes** — `test_load_basic_program` (8 cômodos, 5 relações, `site.north == "back"`), `test_relation_to_unknown_room_rejected`, `test_self_relation_rejected`, `test_duplicate_pair_rejected` (`a–b` e `b–a`), `test_intensity_out_of_range_rejected` (0 e 6), `test_basic_house_still_loads` (fixture do M0, sem `north`, continua carregando).
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4: Rodar** `pytest -q` → tudo passa.
- [ ] **Passo 5: Commit** — `feat: add room program request model`

---

### Tarefa 3: Acesso (entrada e alcançabilidade potencial)

**Arquivos:** criar `src/pygridplan/validation/access.py`, `tests/test_access.py`; modificar `catalog.py` e `data/room_types.yaml`.

**Interfaces:**
- `RoomType.suite_access: tuple[str, ...] = ()` — tipos privativos que se alcançam **através** deste tipo (design 5.5). Dados: `quarto: [closet, banheiro]`, `closet: [banheiro]`.
- `MIN_PASSAGE_MM = 900`
- `passages(plan: Plan) -> dict[tuple[str, str], int]` — para cada par (na ordem de `plan.rooms`) com parede interna compartilhada, a soma dos comprimentos; usa `derive_walls`.
- `check_access(plan: Plan, catalog: Catalog) -> list[Issue]`. Regras:
  - **frente da casa** = menor `rect.y` entre os cômodos; um cômodo **atravessável** com `rect.y` igual a ela é uma entrada possível. Nenhum → `Issue(code="no_entrance")`;
  - busca em largura a partir das entradas, por pares com passagem ≥ `MIN_PASSAGE_MM`. Pode-se **entrar** em qualquer cômodo vizinho; **sair** de um cômodo só se ele for atravessável, ou, se for privativo, apenas para tipos listados no seu `suite_access`;
  - cada cômodo não alcançado → `Issue(code="unreachable", room_ids=(id,))`.

- [ ] **Passo 1: Testes** — `test_basic_house_access_ok` (`[]`), `test_room_only_reachable_through_bedroom_is_unreachable` (quarto B só encosta no quarto A → `unreachable` para B), `test_suite_bathroom_is_reachable` (banheiro só encosta num quarto alcançável → `[]`), `test_no_traversable_room_on_front` (só quartos → `no_entrance`), `test_short_shared_wall_is_not_a_passage` (vizinhos com 800 mm em comum → `unreachable`).
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4: Rodar** `pytest -q` → tudo passa.
- [ ] **Passo 5: Commit** — `feat: check entrance and potential reachability between rooms`

---

### Tarefa 4: Nota e diversidade

**Arquivos:** criar `src/pygridplan/scoring/__init__.py`, `scoring/score.py`, `scoring/diversity.py`, `tests/test_score.py`, `tests/test_diversity.py`; modificar `catalog.py` e `data/room_types.yaml`.

**Interfaces:**
- `RoomType.wet: bool = False` (dados: cozinha, banheiro, lavabo, lavanderia) e `RoomType.sun: bool = False` (dados: sala, quarto).
- `DEFAULT_TARGET_FACTOR = 1.25` — sem `target_area_m2`, a área-alvo é `min_area_m2 × 1,25`; circulação tem alvo 0 (design 5.4: corredor mínimo). **[decisão do Agente]**
- `WEIGHTS = {"relations": 3.0, "area_fit": 2.0, "compactness": 1.0, "circulation": 1.0, "solar": 1.0, "wet_grouping": 0.5}` — fonte única dos pesos; o solver (Tarefa 5) importa daqui.
- `Criterion(name: str, value: float, weight: float)` (`value` em [0, 1]); `Score(total: float, criteria: tuple[Criterion, ...])`, com `total = Σ value·weight / Σ weight dos critérios ativos`.
- `room_target_m2(room: RoomRequest, catalog: Catalog) -> float`
- `score_plan(plan: Plan, request: Request, catalog: Catalog) -> Score`. Critérios (design 5.3–5.4), "adjacente" = passagem ≥ `MIN_PASSAGE_MM`:
  - `relations`: média ponderada por intensidade; `near` vale 1 se adjacentes; `far` vale a distância de Manhattan entre centros ÷ (largura + profundidade do terreno), limitada a 1. Inativo sem relações;
  - `area_fit`: 1 − média de |área útil − alvo| ÷ alvo, limitada a [0, 1], só nos cômodos com alvo > 0;
  - `compactness`: soma das áreas dos retângulos ÷ área da caixa envolvente;
  - `circulation`: 1 − área útil de circulação ÷ área útil total;
  - `solar`: fração dos cômodos `sun` com um lado na fachada norte da caixa envolvente; inativo se `site.north is None` ou não houver cômodo `sun`;
  - `wet_grouping`: fração dos cômodos `wet` adjacentes a outro `wet`; inativo com menos de 2.
- `Pattern = dict[tuple[str, str], tuple[bool, bool, bool, bool]]`
- `relative_pattern(plan: Plan) -> Pattern` — para cada par (i, j) na ordem de `plan.rooms`: (i à esquerda de j: `i.x2 <= j.x`, à direita: `j.x2 <= i.x`, abaixo/à frente: `i.y2 <= j.y`, acima/atrás: `j.y2 <= i.y`).
- `plan_distance(a: Plan, b: Plan) -> float` — fração de pares com padrão diferente (mesmos IDs; senão `ValueError`).

- [ ] **Passo 1: Testes** (os testes de nota montam um `Request` com os mesmos IDs e tipos do `basic-house`, num helper do próprio arquivo de teste) — `test_basic_house_compactness_is_one` (a casa preenche a caixa → `1.0`), `test_basic_house_circulation_value` (`1 − área útil da circulação ÷ área útil total`, conferido contra `useful_area_mm2`), `test_near_relation_satisfied` (sala–cozinha near → `relations == 1.0`), `test_solar_inactive_without_north`, `test_total_is_weighted_mean_of_active`, `test_pattern_of_two_rooms` (a à esquerda de b → `(True, False, False, False)`), `test_distance_zero_for_same_plan`, `test_mirrored_plan_differs` (espelhar no eixo x → distância > 0).
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4: Rodar** `pytest -q` → tudo passa.
- [ ] **Passo 5: Commit** — `feat: add decomposed plan score and layout diversity metric`

---

### Tarefa 5: Modelo CP-SAT da etapa 1

**Arquivos:** criar `src/pygridplan/generators/__init__.py`, `generators/cpsat.py`, `tests/test_cpsat.py`.

**Interfaces:**
- `solve_layout(request: Request, catalog: Catalog, *, seed: int = 0, time_limit: float = 5.0, forbidden: Sequence[Pattern] = (), min_diff: int = 1) -> Plan | None` — uma solução ótima/viável, ou `None` se inviável ou sem solução no tempo. `time_limit` é tempo **determinístico**.

Modelo (o que os testes não determinam sozinhos):
- variáveis em unidades de grade (100 mm): `x, y, w, h` por cômodo; `rect` em mm = unidade × 100;
- **dentro do terreno e dos recuos:** com `e = wall_ext_mm // 2`, `x ≥ left + e` (ou `e` se `left` em `attached_sides`), `x2 ≤ largura − right − e` (idem), `y ≥ front + e`, `y2 ≤ profundidade − back − e` (idem `back`), arredondando para a grade **para dentro**;
- **mínimos (conservadores):** `w, h ≥ min_width_mm + wall_ext_mm` e `(w − wall_ext_mm)·(h − wall_ext_mm) ≥ min_area` em mm² (`add_multiplication_equality` com variáveis em mm);
- **sem sobreposição:** `add_no_overlap_2d`;
- **posições relativas reificadas:** por par, 4 booleanos `left/right/below/above` com `b ⇔ desigualdade` (`only_enforce_if` nos dois sentidos) — esse é o `Pattern` da Tarefa 4;
- **vão entre paredes (design 5.1):** quando `left` (idem nos outros 3), o vão `x_j − x2_i` é 0 **ou** ≥ `wall_ext_mm` (booleano auxiliar);
- **adjacência** `adj_ij` (com passagem ≥ `MIN_PASSAGE_MM`) para os pares que precisam dela: `adj ⇔ OR` de 4 sub-booleanos, por exemplo "j à direita colado": `x2_i = x_j ∧ y_i + L ≤ y2_j ∧ y_j + L ≤ y2_i`, com L = 900 mm;
- **acesso local** (condição necessária; a global vem da Tarefa 3): todo privativo é adjacente a um atravessável ou a um tipo cujo `suite_access` o contém; todo atravessável é adjacente a outro atravessável **ou** toca a frente da casa (`y = min y`); pelo menos um atravessável toca a frente;
- **diversidade:** para cada padrão em `forbidden`, Σ (par difere) ≥ `min_diff`, com "par difere" = booleano auxiliar ≥ cada |b − b_proibido|;
- **objetivo** (maximizar; pesos de `WEIGHTS`, coeficientes float, ou ×1000 arredondados se o CP-SAT recusar float — registrar a escolha no ledger): + relações `near` (`adj`) e `far` (distância de Manhattan entre centros), pela intensidade; − |área útil aproximada − alvo| ÷ alvo; − perímetro da caixa envolvente ÷ (largura + profundidade); − área da circulação ÷ área-alvo total; + cômodos `sun` na fachada norte; + pares `wet` adjacentes;
- parâmetros: `random_seed = seed`, `max_deterministic_time = time_limit`, `num_workers = 8` com `interleave_search = True` se for preciso para reprodutibilidade (ver Tarefa 6, `test_same_seed_same_plans`; registrar no ledger o que passou).

- [ ] **Passo 1: Testes** (`time_limit=2.0` para os testes serem rápidos) — `test_solution_is_valid` (`basic-program` → `validate_geometry == []`), `test_respects_setbacks_and_grid` (`check_recommendations` sem `setback`; todas as coordenadas `% 100 == 0`), `test_respects_minimums` (sem `min_width`/`min_area`), `test_forbidden_pattern_is_avoided` (resolver, proibir o padrão com `min_diff=3`, resolver de novo → `plan_distance ≥ 3 / nº de pares`), `test_infeasible_returns_none` (cômodo de 300 m² num terreno 10×25 → `None`).
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4: Rodar** `pytest -q` → tudo passa.
- [ ] **Passo 5: Commit** — `feat: add CP-SAT layout model for room placement`

---

### Tarefa 6: Laço de alternativas

**Arquivos:** modificar `generators/cpsat.py`; criar `tests/test_generate.py`.

**Interfaces:**
- `class GenerationError(Exception)`
- `Alternative(plan: Plan, score: Score, warnings: tuple[Issue, ...])` (pydantic, frozen)
- `generate_alternatives(request: Request, catalog: Catalog, *, k: int = 4, seed: int = 0, time_limit: float = 5.0, max_attempts: int = 20) -> list[Alternative]`

Algoritmo:
1. sem nenhum cômodo atravessável → `GenerationError("O programa precisa de ao menos um cômodo atravessável (ex.: sala) para a entrada.")`;
2. `min_diff = max(1, ceil(0.15 × nº de pares))`; laço até ter `k` aceitas ou `max_attempts` resoluções: `solve_layout(..., forbidden=padrões_já_vistos, seed=seed + tentativa)`;
3. `None` na **primeira** resolução → `GenerationError` explicando que o programa não coube no terreno com os recuos e mínimos (citar a área mínima somada vs. a área edificável); `None` depois → fim do laço (não há mais alternativas diferentes);
4. cada solução passa por `validate_geometry` e `check_access`: com erro, entra em `forbidden` e não é aceita; sem erro, vira `Alternative` (com `score_plan` e os avisos de `check_recommendations`) e seu padrão entra em `forbidden`;
5. devolver na ordem de geração.

- [ ] **Passo 1: Testes** — `test_four_valid_diverse_alternatives` (`basic-program`, k=4 → 4; todas sem erros de geometria e acesso; `plan_distance` entre cada par ≥ `min_diff / nº de pares`), `test_program_too_big_raises` (`GenerationError`), `test_no_traversable_room_raises` (só quartos → `GenerationError` com "atravessável" na mensagem), `test_small_program_returns_fewer` (sala + cozinha, k=4 → entre 1 e 3 alternativas, sem erro), `test_same_seed_same_plans` (duas execuções → listas de `plan` iguais).
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4: Rodar** `pytest -q` → tudo passa.
- [ ] **Passo 5: Commit** — `feat: generate diverse validated layout alternatives`

---

### Tarefa 7: CLI `generate` e página de comparação

**Arquivos:** criar `src/pygridplan/export/svg.py`, `export/report.py`, `tests/test_report.py`; modificar `__main__.py`, `README.md`.

**Interfaces:**
- `plan_to_svg(plan: Plan, catalog: Catalog) -> str` — SVG autocontido: terreno, retângulos dos cômodos com cor por zona (social, íntima, serviço), nome e área útil; `y` invertido para a frente ficar embaixo, como no DXF.
- `write_report(alternatives: list[Alternative], catalog: Catalog, path: Path) -> None` — um HTML autocontido (sem dependências externas), tema escuro, com uma coluna por alternativa: o SVG, a nota total, a tabela de critérios (nome, valor, peso) e os avisos.
- CLI: `python -m pygridplan generate PEDIDO.json PASTA [--k 4] [--seed 0] [--time-limit 5]` → grava `PASTA/alt-N.json` (`save_plan`), `PASTA/alt-N.dxf` (`export_dxf`) e `PASTA/report.html`; imprime uma linha por alternativa (`alt-1  nota 0,82  4,1 s`) e devolve 0. `GenerationError` → mensagem em `stderr`, devolve 1.

- [ ] **Passo 1: Testes** — `test_svg_has_one_rect_per_room_plus_lot`, `test_report_has_one_svg_per_alternative`, `test_cli_generate_writes_files` (k=2, `time_limit=2` → `alt-1.json`, `alt-1.dxf`, `alt-2.*`, `report.html`; `load_plan(alt-1.json)` funciona), `test_cli_generate_reports_error` (pedido grande demais → 1, mensagem no `stderr`).
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4: Rodar** `pytest -q` → tudo passa.
- [ ] **Passo 5: Verificação final do M1**
  - `pytest -q` → tudo passa; `pyright` → `0 errors`;
  - `python -m pygridplan generate tests/fixtures/requests/basic-program.json out/m1` → 4 alternativas; **registrar o tempo de cada uma** e comparar com a meta (design 8);
  - abrir `out/m1/report.html` e um `alt-N.dxf` com o responsável (**conferência visual**, DEC-0069).
- [ ] **Passo 6: Commit** — `feat: add generate command with HTML comparison report`
- [ ] **Passo 7: Fechamento** — revisão final independente; README (uso do `generate`, estado, estrutura com ✅); DECISOES.md com a declaração de encerramento (DEC-0069); commit `docs: close M1`.

---

## Fora do escopo do M1 (com o porquê)

- **Árvore de estados (design 4.4)** → **M2**. Com uma única etapa gerada (cômodos), não há o que navegar; a árvore só ganha função quando a interface permitir escolher, voltar e expandir. **[proposta do Agente: mover do M1 para o M2]**
- **Pergunta de implantação (design 6.2)** → M2: é um fluxo de interface. O solver do M1 já respeita `attached_sides`.
- **Retornos decrescentes e Choquet (design 5.6)** → depois; o M1 usa média ponderada linear.
- **Área verde mínima (design 5.4)** → M2, junto com a pergunta sobre quintal; no M1 os recuos e a compacidade já deixam área livre.
- **Curadoria das medidas mínimas com fontes** → trilha de dados **D1**, paralela ao M1 (DEC-0072). O gerador só lê o catálogo, então valores melhores entram sem mudar código.
- **Gerador por subdivisão** → M7.
