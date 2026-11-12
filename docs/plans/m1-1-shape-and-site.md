# M1.1 — Forma e implantação: plano de implementação

Versão: 1.0 · Criado em: 2026-11-12 · Status: **aguardando revisão do responsável**

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: `superpowers:subagent-driven-development` ou `superpowers:executing-plans`, tarefa por tarefa. Passos em checkbox (`- [ ]`). Seguir `superpowers:test-driven-development` e `karpathy-guidelines` (CLAUDE.md).

**Objetivo:** fazer o gerador produzir plantas que pareçam plantas: bloco cheio sem vazios fechados, paredes alinhadas, posição previsível no lote, encosto automático na divisa em lote pequeno, muro em todo o perímetro e 4 categorias de cor (interna seca, interna molhada, externa construída, externa verde).

**Arquitetura:** os novos parâmetros físicos (espessura do muro, distância mínima de janela à divisa, permeabilidade de referência) entram como **dados com fonte** (`data/site_defaults.yaml`). A forma melhora por dois caminhos:
- **restrições** de implantação no CP-SAT (frente e centro);
- **critérios** com o mesmo peso no solver e na nota (`compactness` reforçado pela área vazia, `alignment` novo).

Vazio fechado vira **erro de validade**: o laço de alternativas do M1 já rejeita e tenta de novo. Muro, área verde e cores são **representação** (DXF, SVG), derivadas do modelo.

**Stack:** sem dependências novas.

**Spec:** [docs/design/mvp.md](../design/mvp.md), seção 20.1 (aprovada, DEC-0082), e seções 5.1, 6.2 e 13.

## Restrições globais

- Tudo do M0 e do M1 continua valendo: mm inteiros, grade de 100 mm, reprodutibilidade por semente (`interleave_search` e tempo determinístico), `MIN_PASSAGE_MM` de 900 mm, lado mínimo de 1,10 m, vão de 0 ou ≥ 900 mm.
- **Dado novo sempre com fonte** em `data/sources.yaml`. Lei municipal nunca vira restrição nacional; a permeabilidade de 25% (Curitiba) é só **aviso** com a cidade citada.
- Critérios novos ou alterados usam **os mesmos pesos** no solver e na nota (`WEIGHTS`).
- **Implantação padrão** (seção 20.1, item 4): frente da casa na linha do recuo frontal; centralizada na largura (diferença entre folgas esquerda e direita ≤ 100 mm). Com lado encostado, a casa encosta nesse lado.
- **Encosto automático** (item 5): só quando o pedido não traz `attached_sides` e não coube; a sequência é `("left",)`, depois `("left", "right")`, depois `("left", "right", "back")`.
- Meta de desempenho: continua ~5 s por alternativa (8 cômodos, máquina livre). Medir e registrar; se piorar, ajustar pesos ou modelo e registrar a decisão.
- **Commits:** o responsável aprova o plano de commits antes (DEC-0053). O push é dele.

## Foco de revisão

1. Lote pequeno demais mesmo encostando nas 3 divisas → `GenerationError` clara → Tarefa 4 (`test_too_small_even_attached_raises`).
2. Pedido que já traz `attached_sides` → o gerador respeita e **não** testa outras combinações → Tarefa 4 (`test_explicit_attached_sides_are_kept`).
3. Pátio pedido pelo usuário (cômodo tipo `patio`) cercado de cômodos → **não** é vazio fechado → Tarefa 2 (`test_requested_patio_is_not_a_void`).
4. Programa de 1 cômodo (sem pares) → critério `alignment` inativo, sem erro → Tarefa 3 (`test_alignment_inactive_without_pairs`).
5. Lado encostado + centralização → a casa encosta no lado pedido e não é "puxada" para o centro → Tarefa 3 (`test_attached_left_touches_left_bound`).

## Mapa de arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `data/site_defaults.yaml`, `data/sources.yaml` | muro, distância de janela, permeabilidade de referência (com fonte) | 1 |
| `src/pygridplan/model/site_defaults.py` | `SiteDefaults`, `load_site_defaults` | 1 |
| `data/room_types.yaml`, `model/catalog.py` | tipo `patio`; `RoomType.category` | 1, 5 |
| `src/pygridplan/validation/checks.py` | erro `enclosed_void` | 2 |
| `src/pygridplan/generators/cpsat.py`, `scoring/score.py` | implantação, área vazia, alinhamento, encosto automático | 3, 4 |
| `src/pygridplan/model/walls.py` | `exterior_sides` | 4 |
| `src/pygridplan/validation/site.py` | `check_site`: "sem janela" e permeabilidade | 4, 5 |
| `src/pygridplan/export/dxf.py`, `svg.py`, `report.py` | muro, 4 cores, área verde, legenda | 5 |

---

### Tarefa 1: Dados de implantação e tipo pátio

**Arquivos:** criar `data/site_defaults.yaml`, `src/pygridplan/model/site_defaults.py`, `tests/test_site_defaults.py`; modificar `data/sources.yaml`, `data/room_types.yaml`, `tests/test_catalog.py`.

**Interfaces:**
- `SiteDefaults(fence_thickness_mm: int, window_min_distance_mm: int, permeability_min: float, sources: dict[str, str])` (frozen, `extra="forbid"`).
- `DEFAULT_SITE_DEFAULTS_PATH = DATA_DIR / "site_defaults.yaml"`; `load_site_defaults(path: Path = DEFAULT_SITE_DEFAULTS_PATH) -> SiteDefaults`. Recusa campo numérico sem fonte, ou com fonte não registrada (mesma regra e mesmas mensagens do `load_catalog`).
- Valores: `fence_thickness_mm: 150` (fonte `agente`); `window_min_distance_mm: 1500` (fonte `codigo-civil`, art. 1.301); `permeability_min: 0.25` (nova fonte `curitiba-15511-2019`, `kind: L-mun`, URL `https://www.migalhas.com.br/arquivos/2020/7/29773EB9160F0E_PDF_Apresentacao.pdf`, nota "referência municipal; só aviso").
- Catálogo: tipo `patio` ("Pátio / jardim de inverno"; `zone: social`; `passage: traversable`; `exterior: true`; sem números).

- [ ] **Passo 1: Testes** — `test_site_defaults_load` (`fence_thickness_mm == 150`, `window_min_distance_mm == 1500`, `permeability_min == 0.25`), `test_site_default_without_source_rejected` (YAML em `tmp_path` → `ValueError` com "sem fonte"), `test_patio_is_exterior` (`load_catalog().get("patio").exterior`). O `test_every_citation_in_data_is_registered` já cobre o arquivo novo.
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4:** `pytest -q` → tudo passa.
- [ ] **Passo 5: Commit** — `feat: add sourced site defaults and patio room type`

---

### Tarefa 2: Vazio fechado é inválido

**Arquivos:** modificar `src/pygridplan/validation/checks.py`; testes em `tests/test_checks.py`.

**Interfaces:**
- `enclosed_void_area_mm2(plan: Plan) -> int`: área de regiões **não cobertas** por cômodos, dentro da caixa envolvente, **sem ligação com a borda** da caixa.
- `validate_geometry` passa a emitir `Issue(code="enclosed_void", message="vazio fechado de X,XX m² dentro da casa (peça um pátio se for intencional)")` quando a área > 0.

Algoritmo (o teste não determina): compressão de coordenadas. As linhas de corte são todos os `x`, `x2`, `y` e `y2` dos cômodos; as células entre cortes consecutivos ficam marcadas como cobertas se estiverem dentro de algum cômodo. Um *flood fill* parte das células descobertas na borda da caixa; as descobertas que sobram, sem alcance da borda, somam a área. Funciona com qualquer coordenada (não depende da grade).

- [ ] **Passo 1: Testes** — `test_ring_with_hole_is_enclosed_void` (8 cômodos 1 000 × 1 000 em anel 3 × 3 com o centro vazio → `enclosed_void` e `enclosed_void_area_mm2 == 1_000_000`), `test_notch_open_to_border_is_not_a_void` (forma em U → `0`), `test_requested_patio_is_not_a_void` (o mesmo anel com um cômodo `patio` no centro → sem `enclosed_void`), `test_basic_house_has_no_void`.
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4:** `pytest -q` → tudo passa. Com isso, o gerador já rejeita vazios, porque o laço do M1 usa `validate_geometry`.
- [ ] **Passo 5: Commit** — `feat: reject enclosed voids inside the house`

---

### Tarefa 3: Forma no solver e na nota

**Arquivos:** modificar `src/pygridplan/generators/cpsat.py`, `src/pygridplan/scoring/score.py`; testes em `tests/test_cpsat.py`, `tests/test_score.py`.

**Interfaces:**
- `WEIGHTS["compactness"]`: 1,0 → **3,0**; novo `WEIGHTS["alignment"] = 1.0`.
- Nota, `compactness` (sem mudança de definição): soma das áreas dos retângulos ÷ área da caixa envolvente.
- Nota, `alignment` (novo):
  - **pares candidatos** = pares adjacentes (passagem ≥ `MIN_PASSAGE_MM`) + pares do mesmo tipo de cômodo;
  - **acerto** = par adjacente lado a lado com `y` igual ou `y2` igual; par adjacente frente/fundo com `x` igual ou `x2` igual; par do mesmo tipo com as mesmas dimensões (`w`, `h`), ou as mesmas trocadas;
  - `value` = acertos ÷ candidatos;
  - inativo sem candidatos.
- Solver:
  - **implantação:** `by1 == yr[0]`. Sem `left` nem `right` em `attached_sides`: `|(bx1 − xr[0]) − (xr[1] − bx2)| ≤ 1`. Com só `left`: `bx1 == xr[0]`. Com só `right`: `bx2 == xr[1]`. Com os dois, nada a mais;
  - **área vazia:** `void = (bx2 − bx1)·(by2 − by1) − Σ wᵢ·hᵢ` (unidades²; `add_multiplication_equality` para a caixa e para cada cômodo). Termo `−WEIGHTS["compactness"] · void ÷ (área-alvo total em unidades²)`. **Substitui** o termo de perímetro;
  - **alinhamento:** para cada par, um booleano `a ⇒ adj(i, j)` e `a ⇒ OR(yᵢ = yⱼ, y2ᵢ = y2ⱼ, xᵢ = xⱼ, x2ᵢ = x2ⱼ)`; para cada par do mesmo tipo, um booleano `e ⇒ (wᵢ = wⱼ ∧ hᵢ = hⱼ)`. Recompensa `WEIGHTS["alignment"] ÷ nº de candidatos` por booleano verdadeiro.

- [ ] **Passo 1: Testes** (gerador com `time_limit=0.5`):
  - `test_house_on_front_setback_and_centered`: `basic-program` → `min(y) == 4100`; folgas esquerda e direita (até a linha de recuo + 75 mm) com diferença ≤ 100;
  - `test_attached_left_touches_left_bound`: mesmo pedido com `attached_sides: ["left"]` → `min(x) == 100`;
  - `test_generated_house_is_compact`: `compactness ≥ 0.95` e nenhum `enclosed_void`;
  - `test_alignment_value_on_hand_plan`: 3 quartos 3 000 × 4 000 lado a lado, alinhados → `alignment == 1.0`; o mesmo com um quarto deslocado 500 mm → `< 1.0`;
  - `test_alignment_inactive_without_pairs`: 1 cômodo → sem `alignment` nos critérios;
  - `test_three_bedrooms_tend_to_match`: pedido com sala, cozinha, banheiro, circulação e 3 quartos sem alvo → pelo menos 2 quartos com as mesmas dimensões.
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4:** `pytest -q` → tudo passa.
- [ ] **Passo 5: Medir** — `generate` do `basic-program`: tempo de cada resolução e nota. Se uma resolução passar de ~5 s (com a máquina livre) ou a compacidade ficar abaixo de 0,95, ajustar e registrar no ledger.
- [ ] **Passo 6: Commit** — `feat: favor compact aligned footprints placed on the front setback`
- [ ] **Passo 7: Revisão intermediária independente** (como no M1, depois da tarefa mais arriscada).

---

### Tarefa 4: Lote pequeno, encosto automático e "sem janela"

**Arquivos:** modificar `src/pygridplan/generators/cpsat.py`, `src/pygridplan/model/walls.py`; criar `src/pygridplan/validation/site.py`; testes em `tests/test_generate.py`, `tests/test_site.py`.

**Interfaces:**
- `exterior_sides(room: Room, plan: Plan) -> set[Literal["left", "right", "front", "back"]]` em `walls.py`: lados com algum trecho de parede externa (reaproveita `_exterior_parts`). `bottom` → `front`; `top` → `back`.
- `check_site(plan: Plan, catalog: Catalog, defaults: SiteDefaults) -> list[Issue]` em `validation/site.py`. Nesta tarefa, só o código `no_window`: para cada cômodo e lado externo, distância da **face externa** da parede (eixo ± `wall_ext_mm // 2`) até a divisa daquele lado < `window_min_distance_mm` → `Issue(code="no_window", room_ids=(id,), recommended=1500, actual=dist)`, com a mensagem "quarto1: lado esquerdo a 0,03 m da divisa — sem janela (Código Civil, art. 1.301)".
- `generate_alternatives`:
  - sem `attached_sides` no pedido e com a primeira resolução `None`, tenta a sequência das restrições globais com `request.site.model_copy(update={"attached_sides": frozenset(lados)})`;
  - a primeira que resolve vira o pedido efetivo, e cada alternativa ganha um aviso `Issue(code="attached", message="casa encostada na divisa esquerda: não coube com os afastamentos")`;
  - todas as alternativas passam a incluir `check_site` nos avisos;
  - nada resolveu → `GenerationError` atual (mensagem de não coube).

- [ ] **Passo 1: Testes** — lote 7 000 × 15 000 com recuos 4 000 / 2 000 / 1 500 / 1 500 e programa sala, cozinha, banheiro, circulação, 2 quartos (profundidade útil de 8,85 m: os 6 cômodos não cabem empilhados numa coluna de 3,85 m; se ainda couberem, o executor ajusta o lote e registra):
  - `test_small_lot_attaches_automatically`: alternativas com aviso `attached`, `plan.site.attached_sides == {"left"}` e algum cômodo em `x == 100`;
  - `test_no_window_on_attached_side`: aviso `no_window` para os cômodos em `x == 100`;
  - `test_explicit_attached_sides_are_kept`: pedido com `["right"]` → nenhum aviso `attached`; o lado efetivo continua `{"right"}`;
  - `test_too_small_even_attached_raises`: lote 3 000 × 8 000 → `GenerationError`;
  - `test_exterior_sides_of_basic_house`: `sala` → `{"left", "front"}`.
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4:** `pytest -q` → tudo passa.
- [ ] **Passo 5: Commit** — `feat: attach the house to lot boundaries on small lots and flag window-free sides`

---

### Tarefa 5: Muro, áreas externas e 4 cores

**Arquivos:** modificar `model/catalog.py`, `validation/site.py`, `export/dxf.py`, `export/svg.py`, `export/report.py`, `__main__.py`; testes em `tests/test_site.py`, `tests/test_dxf.py`, `tests/test_report.py`.

**Interfaces:**
- `RoomType.category -> Literal["dry", "wet", "built"]` (propriedade): `exterior` → `built`; `wet` → `wet`; senão `dry`.
- `CATEGORY_STYLE = {"dry": ("#d97757", 30), "wet": ("#5fa8d3", 150), "built": ("#8a8a80", 8), "green": ("#6fae7a", 3)}` (cor do SVG, cor ACI do DXF) em `export/svg.py`. É a **fonte única** das cores; `dxf.py` importa daqui.
- `green_area_mm2(plan: Plan, defaults: SiteDefaults) -> int` em `validation/site.py`: área do lote − faixa do muro − soma das áreas dos retângulos dos cômodos (todos, inclusive os `built`).
- `check_site` ganha o código `permeability` quando `green ÷ área do lote < permeability_min`, com a mensagem "área verde 18 % < 25 % (referência de Curitiba, Lei 15.511/2019; confira a lei do seu município)".
- DXF: novo layer `A-MURO` (cor 8), com 4 hachuras: faixas de `fence_thickness_mm` por dentro da divisa, cobrindo os cantos. O contorno de `A-AREAS` de cada cômodo recebe a cor ACI da categoria.
- SVG: o lote fica pintado de verde (`green`) por dentro do muro; o muro é desenhado; cada cômodo leva a cor da categoria. O `report.html` ganha uma legenda das 4 categorias.
- `export_dxf` e `plan_to_svg` passam a receber `defaults: SiteDefaults`; a CLI carrega com `load_site_defaults()`.

- [ ] **Passo 1: Testes** — `test_room_categories` (`sala` dry, `banheiro` wet, `varanda` built), `test_green_area_and_permeability_warning` (casa ocupando quase todo o lote → `permeability`; `basic_house` no lote 10 × 25 → sem aviso), `test_dxf_has_fence_layer_with_four_bands`, `test_svg_paints_lot_green_and_draws_fence`, `test_report_has_category_legend`.
- [ ] **Passo 2: Rodar** → FAIL. **Passo 3: Implementar.** **Passo 4:** `pytest -q` → tudo passa; `pyright` → `0 errors`.
- [ ] **Passo 5: Commit** — `feat: draw lot fence, outdoor areas and four-category color scheme`

---

### Tarefa 6: Verificação e fechamento

- [ ] `python -m pygridplan generate tests/fixtures/requests/basic-program.json out/m1-1` e um pedido de lote pequeno (o da Tarefa 4, como fixture `tests/fixtures/requests/small-lot.json`). Tempos registrados.
- [ ] **Conferência visual** do `report.html` e de um DXF (screenshot do agente + aprovação do responsável, DEC-0069).
- [ ] Revisão final independente; correções importantes com teste vermelho → verde.
- [ ] README (estado, uso), DECISOES.md (declaração de encerramento), título e texto do PR.

## Fora do escopo do M1.1

- **Mobiliário e "cabe?"**: M1.2.
- **Portão do muro, portas e janelas**: M4. O "sem janela" daqui é só a marcação que o M4 vai respeitar.
- **Perfis municipais completos** (recuos, taxa de ocupação, coeficiente por cidade): trilha de dados futura; o M1.1 só usa a permeabilidade de referência como aviso.
- **Calçadas, deck e piscina**: externa construída desenhada só quando houver cômodo `exterior` no pedido. Os caminhos e calçadas automáticos ficam para depois.
