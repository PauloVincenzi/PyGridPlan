# M1.2 — Dimensionamento pelo mobiliário: plano de implementação

Versão: 0.1 · Criado em: 2026-11-22 · Status: **aguarda a aprovação do design. Não executar antes.** As respostas às perguntas da seção 15 do design podem mudar as tarefas 2, 7 e 8.

> **Para agentes:** sub-skill obrigatória: superpowers:subagent-driven-development (recomendada) ou superpowers:executing-plans, tarefa por tarefa. Os passos usam checkbox (`- [ ]`).

**Objetivo:** o gerador só propõe cômodos em que o mobiliário mínimo do perfil escolhido cabe, e mostra os móveis no relatório e no DXF.

**Arquitetura:**
- `fits` é um oráculo CP-SAT pequeno por cômodo, com um laço de alcance em Python.
- A partir dele sai uma escada (largura útil → menor profundidade útil) por conjunto, que entra no modelo da planta como uma restrição `element` por cômodo.
- Cada alternativa pronta passa por uma checagem exata, que grava o arranjo em `Plan.furniture`.

**Tecnologia:** Python 3.13, OR-Tools CP-SAT, pydantic, PyYAML e ezdxf, todas já no projeto.

**Design:** [docs/design/m1-2-furniture-sizing.md](../design/m1-2-furniture-sizing.md). Cada tarefa cita a seção que implementa. Dados: [data/furniture.yaml](../../data/furniture.yaml), já promovidos e com teste (`tests/test_furniture_data.py`).

## Restrições globais

- Nenhuma dependência nova.
- Medidas em **mm inteiros**. O oráculo trabalha em unidades de **10 mm**; a grade de alcance é de **50 mm**.
- Mensagens ao usuário e documentos em português; nomes de arquivos, código e commits em inglês, com Conventional Commits (CLAUDE.md).
- Teste antes do código (TDD). Testes que rodam o gerador inteiro levam `@pytest.mark.slow`; os do oráculo são rápidos.
- Nenhum valor numérico novo em `src/`: os números de mobiliário vêm de `data/furniture.yaml`. Constantes de calibração (voltas do laço, grade) ficam no topo do módulo, com comentário.
- O oráculo é determinístico: `num_workers = 1`, semente fixa.
- Cada tarefa fecha com `.venv/Scripts/python -m pytest -m "not slow" -q` e `pyright` sem erros.
- Commits só depois do plano de commits mostrado ao responsável (CLAUDE.md). Nesta lista, "Commit" quer dizer **propor** o commit.

## Pontos para a revisão

Os cinco casos que o design implica e que nenhum teste principal cobre. Cada um tem teste na tarefa dona:

1. **Valor personalizado absurdo** (folga negativa, dimensão zero, id inexistente): erro de validação em português, nunca um modelo inviável silencioso. Tarefa 1.
2. **Lista explícita com id repetido** (`["criado_mudo", "criado_mudo"]`): duas unidades, não uma. Tarefa 2.
3. **Programa sem quarto:** leitos = 0, a sala fica com o conjunto base (4 assentos), sem erro. Tarefa 2.
4. **Alvo de área menor que o mínimo do mobiliário** (lavabo pedido com 1 m²): aviso `target_below_furniture`, e o gerador usa o mínimo. Tarefa 7.
5. **Plano JSON antigo, sem `furniture`:** carrega e exporta igual a hoje. Tarefa 6.

---

### Tarefa 1: Campos de mobiliário no pedido (design 9)

**Arquivos:** modificar `src/pygridplan/model/request.py`; testar em `tests/test_request.py`.

**Interfaces:**
- Produz:
  - `FurnitureOverrides(clearances: dict[str, int], items: dict[str, ItemSize], room_min_width: dict[str, int])`, com `ItemSize(w: int > 0, d: int > 0)`, folgas `>= 0` e larguras `> 0`;
  - `Request.furniture_profile: Literal["nbr", "mcmv", "ergonomico", "folgado"] = "ergonomico"`;
  - `Request.furniture_rule: Literal["enforce", "warn"] = "enforce"`;
  - `Request.furniture_overrides: FurnitureOverrides = FurnitureOverrides()`;
  - `RoomRequest.furniture: str | tuple[str, ...] | None = None`.

- [ ] **Teste que falha:**
  - `test_request_furniture_defaults`: os padrões acima;
  - `test_room_furniture_accepts_set_id_list_or_empty`: `"quarto_duplo"`, `["cama_king", "criado_mudo"]` e `[]` passam;
  - `test_furniture_overrides_reject_non_positive_sizes`: `{"items": {"cama_casal": {"w": 0, "d": 1900}}}` e `{"clearances": {"lateral_cama": -1}}` levantam `ValidationError`.
- [ ] **Rodar** `.venv/Scripts/python -m pytest tests/test_request.py -q`. Esperado: FALHA.
- [ ] **Implementar** os modelos pydantic congelados, no padrão `_Frozen` do arquivo. A existência dos ids é checada na tarefa 2, que conhece os dados.
- [ ] **Rodar de novo.** Esperado: PASSA; suíte rápida verde.
- [ ] **Commit:** `feat: add furniture profile, rule and overrides to the request`.

### Tarefa 2: Modelo de mobiliário: perfis, personalização e conjunto de cada cômodo (design 4, 6, 9)

**Arquivos:** criar `src/pygridplan/model/furniture.py`; testar em `tests/test_furniture_model.py`.

**Interfaces:**
- Consome: `Request` e `RoomRequest` (tarefa 1); `load_sources`, `check_sourced` e `DATA_DIR` (`model/sources.py`).
- Produz:
  - `ItemSpec(id, name, w, d, wall: bool, zones: dict[str, int], side_zone: int | None, nightstand: bool, short_side_on_wall: bool, sleeps: int, seats: int)`. As folgas já vêm resolvidas em mm; o lado `side` fica em `side_zone`, e uma folga ausente na cadeia de perfis não entra no dicionário;
  - `RoomSpec(items: tuple[ItemSpec, ...], min_width: int | None, door_width: int, door_depth: int, circulation: int, free_zones: tuple[FreeZone, ...])`, hashável (chave do cache da tarefa 5), com `FreeZone(w: int, d: int)` e o círculo convertido no quadrado do diâmetro;
  - `load_furniture(path=DATA_DIR / "furniture.yaml") -> FurnitureData`;
  - `room_specs(request: Request, data: FurnitureData) -> dict[str, RoomSpec]`, só para os cômodos com conjunto ou com lista explícita não vazia;
  - `profile_label(request, data) -> str`, ex.: `"ergonômico · impor · 2 valores personalizados"`.

- [ ] **Testes que falham:**
  - `test_profile_fallback_resolves_missing_values`: no `ergonomico`, `frente_pia` = 850 (vem do `nbr`) e `lateral_cama` = 600; no `folgado`, `entre_camas` = 600 (vem do `ergonomico`);
  - `test_missing_clearance_means_no_zone`: no `nbr`, o box não tem zona `front`;
  - `test_mcmv_profile_uses_its_own_sizes_and_free_zones`: cama de solteiro com `w == 900`; banheiro com `min_width == 1500` e um `FreeZone(1500, 1500)`; quarto com `FreeZone(1200, 1500)`; varanda sem módulo;
  - `test_door_zone_depth_uses_door_front_or_circulation`: `mcmv` 1200, `ergonomico` 600, `nbr` 500; `door_width == 800`;
  - `test_overrides_replace_profile_values`: `lateral_cama: 700` e `guarda_roupa_casal: {w: 2100, d: 600}` aparecem no `RoomSpec` do quarto;
  - `test_unknown_ids_raise_portuguese_error`: folga, item ou conjunto inexistente levanta `ValueError` com o id na mensagem;
  - `test_explicit_list_counts_repeats` (revisão 2): `["criado_mudo", "criado_mudo", "cama_casal"]` dá 3 itens;
  - `test_empty_list_skips_the_room`: `[]` tira o cômodo do resultado;
  - `test_seats_follow_beds`: 3 quartos de casal (6 leitos) dão sofá de 3 + poltrona + sofá de 2; 2 quartos (4 leitos) dão o conjunto base;
  - `test_program_without_bedrooms_keeps_base_living_set` (revisão 3);
  - `test_dining_table_goes_to_living_room_without_dining_room`: a mesa de 4 está na sala sem `sala_jantar`/`copa` e não está quando há um dos dois;
  - `test_types_without_set_are_not_checked`: escritório sem lista não aparece; com `["mesa_4"]`, aparece.
- [ ] **Rodar** `.venv/Scripts/python -m pytest tests/test_furniture_model.py -q`. Esperado: FALHA.
- [ ] **Implementar.**
  - `load_furniture` valida com pydantic e chama `check_sourced` em cada medida.
  - O fallback segue `profiles.<p>.fallback`.
  - Os assentos seguem a ordem do design 6.1: sofá de 3 + poltrona, depois sofá de 2, depois poltronas.
  - Os leitos somam `sleeps` dos conjuntos **resolvidos** de todos os cômodos, inclusive das listas explícitas.
  - O `paired_side` vira `side_zone = max(lateral, entre_camas)` quando o conjunto tem 2 ou mais camas de solteiro.
- [ ] **Rodar de novo.** Esperado: PASSA.
- [ ] **Commit:** `feat: resolve furniture profiles, overrides and room sets`.

### Tarefa 3: Oráculo `fits`, sem o alcance (design 5, regras 1–5 e 7–9; design 7.2)

**Arquivos:** criar `src/pygridplan/validation/furniture.py`; testar em `tests/test_fits.py`.

**Interfaces:**
- Consome: `RoomSpec` e `ItemSpec` (tarefa 2); `Rect` (`model/plan.py`).
- Produz:
  - `Placed(item: str, body: Rect, rotation: int, zones: tuple[Rect, ...])`, em coordenadas locais do cômodo, origem no canto inferior esquerdo;
  - `fits(spec: RoomSpec, width: int, depth: int, door_walls: Sequence[Segment] | None = None) -> tuple[Placed, ...] | None`, onde `Segment = tuple[str, int, int]` é (lado `"left" | "right" | "bottom" | "top"`, início, fim) em mm locais; `None` libera qualquer parede;
  - `arrangement_errors(spec, width, depth, placed) -> list[str]`, conferência independente das regras, sem CP-SAT.

- [ ] **Testes que falham** (casos do design 5, conferidos à mão):
  - `test_double_bedroom_nbr_fits_240_by_290`;
  - `test_double_bedroom_nbr_does_not_fit_240_by_280`;
  - `test_double_bedroom_nbr_needs_240_width`: 2300 × 3500 dá `None`;
  - `test_arrangement_respects_rules`: para cada caso que cabe, `arrangement_errors(...) == []`;
  - `test_nightstand_may_sit_in_bed_side_zone`: casal `nbr` em 2400 × 2900 cabe **só** com essa regra: com `nightstand=False`, dá `None`;
  - `test_table_short_side_may_touch_wall`: `RoomSpec` só com `mesa_4` no `nbr` cabe em 1950 × 2300 (1200 + 750 por 800 + 2 × 750); com `short_side_on_wall=False`, dá `None` (precisaria de 2700);
  - `test_twin_beds_mcmv_width_at_least_260`: `quarto_duplo` no `mcmv` dá `None` com largura 2500, qualquer profundidade;
  - `test_free_zone_blocks_bodies_not_zones`: no banheiro `mcmv`, o quadrado de 1500 não cruza corpo nenhum;
  - `test_door_zone_restricted_to_given_walls`: com `door_walls=[("left", 0, 900)]`, a zona da porta fica nesse trecho; com um trecho de 700 mm, dá `None`;
  - `test_fits_is_deterministic`: duas chamadas devolvem o mesmo arranjo.
- [ ] **Rodar.** Esperado: FALHA.
- [ ] **Implementar** com `cp_model` em unidades de 10 mm, `num_workers = 1` e `random_seed = 0`.
  - Cada móvel tem giro em 4 valores e, por giro, intervalos opcionais (`new_optional_interval_var`).
  - Corpos não se sobrepõem entre si (`add_no_overlap_2d`). Corpos também não cruzam zonas, módulos nem a zona da porta: use booleanos de separação por par, porque zona pode sobrepor zona.
  - O encosto (`wall`) liga o lado de trás a uma das 4 paredes.
  - A largura mínima do cômodo vale para o lado menor: `min(width, depth) >= spec.min_width`.
- [ ] **Rodar de novo.** Esperado: PASSA, e o arquivo de teste inteiro em menos de 10 s.
- [ ] **Commit:** `feat: add furniture fit oracle with composition rules`.

### Tarefa 4: Alcance no oráculo (design 5, regra 6; design 7.2)

**Arquivos:** modificar `src/pygridplan/validation/furniture.py`; testar em `tests/test_fits.py`.

**Interfaces:**
- Consome: `fits` e `Placed` (tarefa 3).
- Produz:
  - `reachable(width, depth, placed, door: Rect, circulation: int) -> bool`;
  - constantes `REACH_GRID_MM = 50` e `MAX_REACH_ROUNDS = 30`;
  - `fits` passa a garantir o alcance.

- [ ] **Testes que falham:**
  - `test_reachable_false_when_body_splits_room`: um corpo de parede a parede separa uma zona da porta;
  - `test_reachable_respects_circulation_width`: uma passagem de 450 mm falha com `circulation=500` e passa com 400;
  - `test_fits_rejects_layout_without_reach`: um conjunto montado para que o único arranjo sem sobreposição deixe uma zona isolada dá `None`;
  - `test_round_limit_returns_none`: com `MAX_REACH_ROUNDS` reduzido a 0 por monkeypatch e um caso que precisa de corte, dá `None`.
- [ ] **Rodar.** Esperado: FALHA.
- [ ] **Implementar.**
  - Rasterizar em 50 mm.
  - Erodir o espaço livre por `circulation // 2` e fazer o flood fill a partir da zona da porta. Toda zona de uso precisa tocar uma célula alcançada.
  - Laço: resolver → conferir → somar um corte. O corte é a cláusula que proíbe a combinação atual dos booleanos de giro, de lado e de separação; ele proíbe a configuração, não as coordenadas.
- [ ] **Rodar de novo.** Esperado: PASSA, incluindo os testes da tarefa 3.
- [ ] **Commit:** `feat: require reachable use zones in the fit oracle`.

### Tarefa 5: Escada, medição de custo e `furniture-minimums` (design 7.3, 7.5, 7.6)

**Arquivos:**
- modificar `src/pygridplan/validation/furniture.py` e `src/pygridplan/__main__.py`;
- testar em `tests/test_staircase.py`;
- relatório em `docs/plans/m1-2-furniture-sizing.md`, seção "Medições".

**Interfaces:**
- Consome: `fits` e `RoomSpec`.
- Produz:
  - `Staircase(min_depth: dict[int, int])`, de largura útil (mm) para a menor profundidade útil (mm), na grade `100k − wall_ext`;
  - `staircase(spec: RoomSpec, grid: int, wall_ext: int, max_side: int) -> Staircase`, com `@lru_cache`;
  - propriedades `Staircase.min_side` e `Staircase.min_area_mm2`;
  - CLI `python -m pygridplan furniture-minimums [--profile P]`, que imprime `tipo  conjunto  largura mín.  área mín.`.

- [ ] **Testes que falham:**
  - `test_staircase_is_monotone_and_symmetric`;
  - `test_staircase_matches_exhaustive_search`: num conjunto de 2 itens, compara com `fits` em toda a grade de 1,0 a 3,0 m;
  - `test_override_grows_double_bedroom`: com `lateral_cama: 900`, o casal `nbr` tem `min_area_mm2` estritamente maior e `min_side` maior ou igual ao da escada sem personalização. Só monotonia: com a cabeceira na parede longa, o menor lado é cama + pé, e não 0,90 + 1,40 + 0,90;
  - `test_cli_furniture_minimums_lists_types`: a saída tem `quarto`, `banheiro` e `cozinha`, com números positivos.
- [ ] **Rodar.** Esperado: FALHA.
- [ ] **Implementar** a varredura em escada (design 7.3), só na metade largura ≤ profundidade, espelhando o resto.
- [ ] **Rodar de novo.** Esperado: PASSA.
- [ ] **Medir** com um script no scratchpad os 9 conjuntos padrão × 4 perfis: tempo por escada, nº de chamadas a `fits` e voltas do laço de alcance. Registrar a tabela na seção "Medições" deste plano.
  - **Portão:** se alguma escada passar de 2 s, parar e aplicar a saída da tabela 7.6 do design (grade de 20 mm ou cache em disco) antes da tarefa 7.
- [ ] **Commit:** `feat: derive minimum room sizes from furniture (staircase and CLI)`.

### Tarefa 6: Arranjo no `Plan` e checagem exata (design 7.4, 8.1)

**Arquivos:**
- modificar `src/pygridplan/model/plan.py` e `src/pygridplan/validation/furniture.py`;
- testar em `tests/test_plan.py` e `tests/test_fits.py`.

**Interfaces:**
- Consome: `fits` (tarefas 3 e 4); `useful_bounds` (`model/walls.py`); `passages` (`validation/access.py`).
- Produz:
  - `PlacedItem(room_id: str, item: str, rect: Rect, rotation: Literal[0, 90, 180, 270], zones: tuple[Rect, ...] = ())`, em mm absolutos;
  - `Plan.furniture: tuple[PlacedItem, ...] = ()`;
  - `door_walls(plan, room_id, catalog) -> list[Segment]`;
  - `check_furniture(plan, specs: dict[str, RoomSpec], catalog) -> tuple[Plan, list[Issue]]`, que devolve o plano com `furniture` preenchido e um `Issue(code="furniture_no_fit", ...)` por cômodo que não cabe, com `recommended` e `actual` em mm.

- [ ] **Testes que falham:**
  - `test_old_plan_json_without_furniture_loads` (revisão 5): `tests/fixtures/plans/basic-house.json` carrega com `furniture == ()`;
  - `test_door_walls_follow_access_rules`: o quarto recebe só os trechos compartilhados com a circulação (≥ 900 mm), e não a parede com outro quarto;
  - `test_check_furniture_fills_plan`: numa planta à mão com quarto de 2,60 × 3,10 útil, os itens ficam dentro de `useful_bounds`;
  - `test_check_furniture_reports_no_fit_with_sizes`: um quarto de 2,20 m dá `furniture_no_fit`, com o mínimo na mensagem.
- [ ] **Rodar.** Esperado: FALHA.
- [ ] **Implementar.** `door_walls` reaproveita a regra de vizinhança do `check_access` (atravessável, ou `suite_access` para privativo) e soma os trechos de fachada do cômodo de entrada.
- [ ] **Rodar de novo.** Esperado: PASSA.
- [ ] **Commit:** `feat: store furniture arrangement in the plan and check it exactly`.

### Tarefa 7: Gerador: restrição, checagem e mensagens (design 7.3–7.5)

**Arquivos:**
- modificar `src/pygridplan/generators/cpsat.py`, `src/pygridplan/__main__.py` e `data/room_types.yaml` (só se a pergunta 2 for aprovada; versão 0.4);
- testar em `tests/test_cpsat.py` e `tests/test_generate.py`.

**Interfaces:**
- Consome:
  - `room_specs` e `load_furniture` (tarefa 2);
  - `staircase` (tarefa 5);
  - `check_furniture` (tarefa 6).
- Produz:
  - `generate_alternatives(..., furniture: FurnitureData | None = None)`, que carrega o padrão quando `None`;
  - `Alternative.plan.furniture` preenchido;
  - avisos `furniture_no_fit` (modo `warn`) e `target_below_furniture`.

- [ ] **Testes que falham:**
  - rápidos:
    - `test_empty_staircase_raises_named_error`: `cama_king` + guarda-roupa de 4000 mm num lote de 6 m levanta `GenerationError` com o id do cômodo;
    - `test_target_below_furniture_warns` (revisão 4): um lavabo com alvo de 1 m² dá o aviso, e o retângulo resolvido tem área ≥ a mínima da escada;
  - lentos:
    - `test_benchmark_rooms_hold_their_furniture`: nos 5 pedidos, `ergonomico`, todo cômodo com conjunto tem itens em `plan.furniture` e nenhum `furniture_no_fit`;
    - `test_nbr_allows_narrower_bathroom_than_mcmv`: o menor lado útil do banheiro em `one-bedroom` é menor com `nbr` que com `mcmv`;
    - `test_warn_rule_never_rejects_for_furniture`.
- [ ] **Rodar.** Esperado: FALHA.
- [ ] **Implementar.**
  - Em `_phase`, por cômodo com escada:
    - `min_side` vem de `Staircase.min_side`;
    - `smallest` vem de `min_area_mm2`;
    - `hk >= hmin[wk]` via `m.add_element(wk - min_side_k, table, hmin)`, com o valor acima do domínio nas larguras inviáveis.
  - Em `generate_alternatives`:
    - `check_furniture` logo depois de `check_access`;
    - no modo `enforce`, falha = `continue`, como hoje;
    - no modo `warn`, falha = aviso.
  - `_no_fit_message` soma as áreas mínimas derivadas.
- [ ] **Rodar de novo.** Esperado: PASSA.
  - **Medir** as 4 alternativas nos 5 pedidos (tempo e rejeições) e registrar em "Medições".
  - **Portão** da tabela 7.6: ≤ +20 % de tempo e ≤ 1 rejeição em 4.
- [ ] **Commit:** `feat: generate only rooms that hold their minimum furniture`.

### Tarefa 8: Relatório HTML e SVG (design 8.2)

**Arquivos:** modificar `src/pygridplan/export/svg.py` e `src/pygridplan/export/report.py`; testar em `tests/test_report.py`.

**Interfaces:**
- Consome: `Plan.furniture`, `profile_label` (tarefa 2) e os avisos da tarefa 7.
- Produz: `write_report(alternatives, catalog, path, furniture_label: str = "")`.

- [ ] **Testes que falham:**
  - `test_report_shows_profile_and_furniture_table`: o HTML tem `Perfil de mobiliário:` e uma linha `cabe` por cômodo com itens;
  - `test_svg_draws_furniture_with_titles`: um `<rect>` por `PlacedItem`, com `<title>` igual ao nome do item; zonas com `stroke-dasharray`;
  - `test_report_without_furniture_is_unchanged`: um plano sem móveis não ganha a seção.
- [ ] **Rodar.** Esperado: FALHA.
- [ ] **Implementar** seguindo o estilo de cores e fontes de `STYLE` e `CATEGORY_STYLE`; nada de JavaScript.
- [ ] **Rodar de novo.** Esperado: PASSA.
- [ ] **Commit:** `feat: show furniture, clearances and profile in the HTML report`.

### Tarefa 9: DXF (design 8.3)

**Arquivos:** modificar `src/pygridplan/export/dxf.py`; testar em `tests/test_dxf.py`.

**Interfaces:**
- Consome: `Plan.furniture` e `load_furniture` (para o nome do item).
- Produz: o layer `A-MOBILIARIO-FOLGAS` em `LAYERS`; blocos `MOB-<item>-<w>x<d>`.

- [ ] **Testes que falham:**
  - `test_dxf_furniture_blocks_on_mobiliario_layer`: um `INSERT` por `PlacedItem` no `A-MOBILIARIO`, com a rotação certa;
  - `test_dxf_clearances_on_non_plot_layer`: as zonas são `LWPOLYLINE` no `A-MOBILIARIO-FOLGAS`, e o layer tem `plot == 0`;
  - `test_dxf_without_furniture_has_no_blocks`.
- [ ] **Rodar.** Esperado: FALHA.
- [ ] **Implementar.**
- [ ] **Rodar de novo.** Esperado: PASSA.
- [ ] **Commit:** `feat: export furniture blocks and clearances to DXF`.

### Tarefa 10: Fechamento do marco

**Arquivos:**
- modificar `README.md`, `data/README.md`, `docs/design/mvp.md` (seção 20.2: só a referência às decisões aprovadas) e `DECISOES.md`;
- gerar `out/m1-2/<pedido>/` (fora do git).

- [ ] **Suíte completa:** `.venv/Scripts/python -m pytest -q` e `pyright`. Esperado: 0 falhas, 0 erros.
- [ ] **Gerar** os 5 pedidos nos perfis `ergonomico` e `nbr` em `out/m1-2/` e montar a tabela de notas, áreas, tempos e rejeições em "Medições".
- [ ] **Revisão final independente** (superpowers:requesting-code-review) e correção dos achados críticos e importantes.
- [ ] **Conferência visual** pelo responsável (`out/m1-2/*/report.html`).
- [ ] **Documentação e registro.** Atualizar README e `data/README.md` (o validador "cabe?" deixa de ser "M8" e passa a ser o M1.2) e registrar no DECISOES.md.
- [ ] **Commit:** `docs: record M1.2 results, measurements and decisions`.

## Medições

(Preenchida nas tarefas 5, 7 e 10.)
