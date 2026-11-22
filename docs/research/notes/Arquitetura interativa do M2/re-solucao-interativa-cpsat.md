# Re-solução interativa com OR-Tools CP-SAT (travas, hints, reuso, cancelamento, streaming, explicação de inviabilidade, latência)

> Notas de pesquisa (trilha "Arquitetura interativa do M2"). Coletadas em 2026-11-22. Versão-alvo: OR-Tools 9.15 (o branch `stable` do GitHub declara `OR_TOOLS_MAJOR=9`, `OR_TOOLS_MINOR=15` em [Version.txt](https://raw.githubusercontent.com/google/or-tools/stable/Version.txt)). Parte dos achados vem da **leitura direta do código-fonte** do branch `stable` (9.15): `sat_parameters.proto`, `cp_model_solver.cc`, `cp_model_solver_helpers.cc`, `subsolver.cc`, `python/cp_model.py`, `python/cp_model_helper.cc`. Código-fonte é evidência forte do comportamento atual, mas não é contrato documentado: pode mudar entre versões.
> Convenção: **FATO** = afirmação com fonte; **HIPÓTESE/OPINIÃO** = inferência minha, a validar no experimento medido.
> Não rodei nenhum experimento. Os números de latência citados são de artigos, não do PyGridPlan.

## 1. Fixar variáveis travadas pelo usuário: igualdade, domínio, `fix_variables_to_their_hinted_value` ou assumptions; explicar quais travas conflitam

### Takeaway
Para **resolver** com travas, fixe as variáveis direto no modelo (igualdade ou domínio). As assumptions servem para **explicar** um conflito, e só funcionam bem num solve de diagnóstico separado: 1 worker, sem objetivo e sem `interleave_search`. Nesse modo o núcleo que volta é reduzido por heurística, não é mínimo. Para um conjunto mínimo de travas em conflito, o recomendado é um objetivo que minimize a soma dos literais violados.

### Cited Findings
- **FATO:** a API Python 9.15 tem `add_assumption(lit)`, `add_assumptions(literals)` e `clear_assumptions()`, que gravam índices booleanos em `model_proto.assumptions`. `CpSolver.sufficient_assumptions_for_infeasibility()` devolve "the indices of the infeasible assumptions" — [cp_model.py (stable)](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/python/cp_model.py)
- **FATO (código 9.15):** se o modelo tem assumptions e vale `num_workers() > 1`, **ou** há objetivo, **ou** objetivo em ponto flutuante, **ou** `enumerate_all_solutions`, **ou** `interleave_search`, o solver registra "Warning: solving with assumptions was requested in a non-fully supported setting… if the model is infeasible, you will not get a useful 'sufficient_assumptions_for_infeasibility' field in the response, it will include all assumptions". Nesse caso ele fixa as assumptions como verdadeiras antes do presolve e, se der INFEASIBLE, devolve **todas** — [cp_model_solver.cc (stable), ~l. 2712–2750](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver.cc)
- **FATO (código 9.15):** com assumptions, os workers `shared_tree` não são criados (`shared->model_proto.assumptions().empty()` é uma das condições) — [cp_model_solver.cc (stable), ~l. 1814](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver.cc)
- **FATO:** Laurent Perron (mantenedor), em 2024-03-02: "parallelism is not supported" e "objective are not supported" com assumptions. Também: "The conditions to use assumptions are tricky" — [GitHub Discussion #4110](https://www.github.com/google/or-tools/discussions/4110)
- **FATO:** Perron, em 2021-03-22: o núcleo "is reduced by heuristics, and not necessary minimal… If you want a minimal set of assumptions, do not use this API, just define the objective as the sum of literals". Frederic Didier: "it will minimize the set only in a single thread and without an objective"; fora disso, "basically get all of the assumptions" — [or-tools-discuss, "SufficientAssumptionsForInfeasibility"](https://groups.google.com/g/or-tools-discuss/c/qlVv2uSq1uo)
- **Conflito de fontes:** o CP-SAT Primer descreve `sufficient_assumptions_for_infeasibility()` como devolvendo "a minimal subset" — [CP-SAT Primer, Parameters](https://d-krupke.github.io/cpsat-primer/parameters.html). Os mantenedores dizem o contrário (núcleo reduzido por heurística, não mínimo) — [or-tools-discuss](https://groups.google.com/g/or-tools-discuss/c/qlVv2uSq1uo). Vale a palavra dos mantenedores.
- **FATO (bug aberto, sem resposta visível):** em 2026-04-22, um usuário relatou que "sufficient_assumptions_for_infeasibility() returns a literal that is not in the assumption list (presolve only)", na issue #5141. O contorno dele foi desligar o presolve — [or-tools-discuss](https://groups.google.com/g/or-tools-discuss/c/Mpv0XoY7cwo)
- **FATO:** assumptions aceitam só literais booleanos. O padrão é ligar cada restrição a um literal com `only_enforce_if(b)` e passar `b` como assumption. Ressalva: "not all constraints in CP-SAT support reification" — [CP-SAT Primer, Parameters](https://d-krupke.github.io/cpsat-primer/parameters.html)
- **FATO (código 9.15):** `fix_variables_to_their_hinted_value` (campo 192, default `false`): "variables appearing in the solution hints will be fixed to their hinted value". O código chama `FixVariablesToHintValue` **antes** do presolve ("Checks for hints early in case they are forced to be hard constraints") — [sat_parameters.proto](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto); [cp_model_solver.cc ~l. 2631](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver.cc). O Primer recomenda esse parâmetro como teste confiável de viabilidade de um hint: se o status for INFEASIBLE, o hint conflita — [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html)
- **FATO:** `keep_all_feasible_solutions_in_presolve` (173, default `false`) desliga as reduções de presolve que removem soluções viáveis, por exemplo fixar uma variável sem uso num valor arbitrário — [sat_parameters.proto](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto). O Primer avisa que isso "may degrade solver performance" — [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html)

### Inferences
- **HIPÓTESE (alta confiança, sem fonte direta):** `model.add(x == v)` e o estreitamento do domínio de `x` para `{v}` dão o mesmo resultado depois do presolve: a variável fica fixa e sai do modelo. A diferença é só de API (a igualdade é uma restrição a mais no proto). No PyGridPlan, como o modelo é reconstruído a cada pedido (ver Q3), fixar pelo domínio na construção é o mais limpo.
- **OPINIÃO:** a arquitetura indicada para o M2 tem dois caminhos.
  - *Solve normal:* travas como fixações duras, com 8 workers, objetivo e o modo determinístico.
  - *Diagnóstico, só se o solve normal der INFEASIBLE:* cada trava `k` ganha um literal `t_k` (as restrições da trava com `only_enforce_if(t_k)`). Duas variantes: (a) `t_k` como assumptions, com `num_workers=1`, sem objetivo e sem `interleave_search`, para um núcleo rápido mas não mínimo; (b) maximizar `Σ t_k` (ou minimizar as travas violadas), para o **menor conjunto de travas a soltar**, que é o que o usuário quer ouvir ("solte a trava X").
  - A variante (b) é ótima e determinística com 1 worker, mas pode custar mais caro. Como o PyGridPlan tem poucas travas (dezenas), parece viável.
- **HIPÓTESE:** a issue #5141 (presolve + assumptions) recomenda validar o núcleo devolvido: conferir se cada índice está na lista de assumptions e, opcionalmente, re-resolver só com o núcleo para confirmar a inviabilidade.

### Gaps
- Não achei documentação oficial (developers.google.com) sobre os efeitos de presolve de "igualdade vs domínio". A equivalência acima é inferência.
- Não verifiquei se a 9.15 tem API Python estável para mudar o domínio de uma `IntVar` existente (há acesso ao proto, mas não confirmei um método público), nem o estado da issue #5141 em novembro de 2026.

## 2. Hints: semântica, `repair_hint`, `hint_conflict_limit`, `fix_variables_to_their_hinted_value`, `debug_crash_on_bad_hint`, hints parciais vs completos, presolve, múltiplos workers

### Takeaway
Na 9.15, um hint **completo e viável** (ainda viável depois do presolve) entra **imediatamente** no pool como solução `complete_hint`. Ou seja, há uma primeira solução sem busca nenhuma, o que é ideal para mostrar o plano anterior na hora. Um hint parcial ou inviável só guia uma busca curta (10 conflitos por padrão) em cada worker de problema completo. Desde a 9.10/9.12, o presolve preserva hints completos e viáveis.

### Cited Findings
- **FATO:** `add_hint(var, value)` acrescenta (var, valor) a `model_proto.solution_hint`. `clear_hints()` "Removes any solution hint from the model" (método `clear_hints`, não `ClearHints`) — [cp_model.py (stable)](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/python/cp_model.py)
- **FATO (parâmetros, verbatim do proto 9.15):**
  - `repair_hint` (167, default `false`): "If true, the solver tries to repair the solution given in the hint. This search terminates after the 'hint_conflict_limit' is reached and the solver switches to regular search. If false, then we do a FIXED_SEARCH using the hint until the hint_conflict_limit is reached."
  - `hint_conflict_limit` (153, default `10`): "Conflict limit used in the phase that exploit the solution hint."
  - `debug_crash_on_bad_hint` (195, default `false`): "Crash if we do not manage to complete the hint into a full solution."
  - `debug_crash_if_presolve_breaks_hint` (306, default `false`): "Crash if presolve breaks a feasible hint."
  - `use_optimization_hints` (35, default `true`): "For a variable with hint, the solver will always try to follow the hint."
  — [sat_parameters.proto (stable)](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto)
- **FATO (código 9.15):** `SolutionHintIsCompleteAndFeasible` ignora as variáveis fixas e exige que **todas** as não fixas tenham hint. Se faltar alguma, registra "The solution hint is incomplete: N out of M non fixed variables hinted". Se o hint estiver completo e viável no modelo **pós-presolve**, faz `manager->NewSolution(solution, "complete_hint", ...)` ("Add it to the pool right away!"). Se estiver completo mas inviável: "we will try to repair it". Se violar as assumptions, não é aceito — [cp_model_solver.cc ~l. 909–1016 e ~l. 3005–3025](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver.cc)
- **FATO (código 9.15):** cada `FullProblemSolver` (worker de problema completo) faz no primeiro "chunk" uma fase de hint ("Starting subsolver '%s' hint search"). Com `repair_hint` chama `MinimizeL1DistanceWithHint`; sem ele chama `QuickSolveWithHint` — [cp_model_solver.cc ~l. 1143–1152](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver.cc)
  - `QuickSolveWithHint` limita os conflitos a `hint_conflict_limit`, usa `search_branching = HINT_SEARCH`, desliga inprocessing e não roda se `optimize_with_core` estiver ativo.
  - `MinimizeL1DistanceWithHint` copia o modelo, **remove o objetivo** e cria variáveis de distância L1 até o hint, com o mesmo limite de conflitos. Não roda com `enumerate_all_solutions`.
  — [cp_model_solver_helpers.cc ~l. 1872–2010](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver_helpers.cc)
- **FATO (código 9.15):** nos fragmentos LNS, o hint vem da vizinhança. Se a busca parecer estagnada, o fragmento é resolvido sem hint. `RestrictObjectiveUsingHint` restringe o objetivo do fragmento a ≤ o do hint — [cp_model_solver.cc ~l. 1467–1505 e 862–905](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver.cc)
- **FATO (código 9.15):** `debug_crash_on_bad_hint` só dispara se já existe solução viável, se o limite de tempo não foi atingido e se `QuickSolveWithHint` não completou o hint. O comentário admite que "sometime the deterministic limit is hit before the hint can be completed" — [cp_model_solver_helpers.cc ~l. 1947–1960](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver_helpers.cc). O Primer chama o parâmetro de "unreliable": "only triggers in multi-worker mode, depends on a race condition between workers" — [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html)
- **FATO (release notes):**
  - v9.10 (2024-05-08): "Preserve hints during presolve".
  - v9.12 (2025-02-17): "Rewrote the hint transformation during presolve. Feasible and complete hints should now be preserved after presolve".
  - Nem a 9.13, nem a 9.14, nem a 9.15 citam mudanças em hints.
  — [GitHub Releases](https://github.com/google/or-tools/releases)
- **FATO:** o Primer diz que o CP-SAT "has historically struggled to preserve the feasibility of hints through presolve" e que, segundo a docstring do helper `complete_hint` do autor, "CP-SAT only benefits from complete hints (all variables hinted)". O mesmo helper resolve com as variáveis do hint parcial fixadas para completá-lo — [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html)

### Inferences
- **HIPÓTESE (forte, pelo código):** se o usuário só muda pesos ou preferências (sem trava nova), o plano anterior continua viável. Passado como hint **completo** (todas as variáveis, auxiliares incluídas), ele vira solução em t≈presolve, e o solver só busca melhorias. O tempo até a "primeira resposta" cai para o custo de construir o modelo mais o presolve.
- **HIPÓTESE:** se a trava nova invalida o plano anterior, o hint completo fica inviável e cai no reparo curto (10 conflitos por worker). Para "manter o plano parecido", o objetivo explícito de perturbação mínima (Q3) é mais controlável que `repair_hint`, porque `MinimizeL1DistanceWithHint` descarta o objetivo e para depois de `hint_conflict_limit` conflitos.
- **HIPÓTESE:** o "hint completo" exige hint de **todas** as variáveis não fixas, inclusive as auxiliares (booleanas de adjacência, distâncias etc.). No PyGridPlan, guardar o vetor completo da solução anterior (por nome ou índice no proto) é o jeito prático de garantir isso, desde que a construção do modelo seja estável (mesma ordem e mesmos nomes).
- **HIPÓTESE:** em `interleave_search`, a fase de hint de cada worker roda no primeiro chunk. O código comenta que o limite por chunk "we do not want to do that for the hint search for now", ou seja, a fase de hint não tem limite de dtime por chunk.

### Gaps
- Não achei medições publicadas do ganho de tempo de um hint completo vs nenhum hint em modelos pequenos. Isso fica para o experimento medido.
- Não confirmei se um hint completo e viável **antes** do presolve pode ser quebrado em casos de borda da 9.15. As notas da 9.12 dizem "should now be preserved" (linguagem não absoluta), e há o parâmetro de depuração `debug_crash_if_presolve_breaks_hint` para detectar isso.

## 3. Reuso entre solves: o CP-SAT não é incremental; clone, pool de soluções, LNS, perturbação mínima

### Takeaway
O CP-SAT é **sem estado entre solves**: cada `solve` relê o proto inteiro e recomeça do zero (sem cláusulas aprendidas reaproveitadas). O único "reuso" real é de **informação**: hint (solução anterior), domínios apertados e restrições extras. Modificar ou clonar o modelo é barato perto do solve. A estabilidade do plano ("mudar pouco") deve entrar como termo de objetivo, como no problema de perturbação mínima (MPP) da literatura.

### Cited Findings
- **FATO:** Perron, em 2023-05-26: "Solve is stateless." Didier, em 2023-05-25: "there is no issue modifying this [CpModel proto] in place between solves. But the gain will be minimal since the solver will still rescan the whole proto and restart from scratch each time" — [or-tools-discuss, "Reuse variables in CP-SAT solver"](https://groups.google.com/g/or-tools-discuss/c/UtMOv318dj4)
- **FATO:** o Primer diz sobre reuso de cláusulas aprendidas entre assumptions: "CP-SAT does not support this feature. Its solver is stateless and always starts from scratch" — [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html). A documentação do CPMpy diz que a representação do modelo no OR-Tools é incremental, "but its solving itself is not (yet?)", ao contrário de Gurobi, PySAT e Z3 — [CPMpy solvers](https://cpmpy.readthedocs.io/en/latest/solvers.html)
- **FATO (código 9.15):** `CpModel.clone()` cria um `CpModel` novo e faz `proto.copy_from(self.proto)`. `__copy__` e `__deepcopy__` também existem — [cp_model.py (stable) ~l. 1476–1487](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/python/cp_model.py)
- **FATO:** `solution_pool_size` (193, default `3`): "Size of the top-n different solutions kept by the solver… Currently, having this larger than one mainly impact the "base" solution chosen for a LNS/LS fragment." Não é uma API para devolver N alternativas ao usuário — [sat_parameters.proto](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto)
- **FATO:** `fill_tightened_domains_in_response` (132) devolve na resposta os domínios derivados. O Primer avisa que, com o objetivo no modelo, soluções viáveis podem ser excluídas — [sat_parameters.proto](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto); [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html)
- **FATO:** `use_lns_only` (101): "Experimental parameters to disable everything but lns". O Primer diz que ele "needs to be combined with a time limit" — [sat_parameters.proto](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto); [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html)
- **FATO (literatura MPP):** Barták, Müller e Rudová definem o MPP como achar, depois que um problema resolvido muda, "a new solution that satisfies these constraints but not being too far from the original solution". Há trabalhos de 2003 a 2005: visão formal (Neural Network World, 2003), "A New Approach to Modeling and Solving Minimal Perturbation Problems" (Springer, 2004) e aplicação em horários de cursos na Purdue (PATAT V, 2005), com busca iterativa e estatística de conflitos, buscando solução "anytime even for over-constrained problems" — [Masaryk Univ., registros 555150/555152/621512](https://is.muni.cz/publication/621512/en/Minimal-Perturbation-Problem-in-Course-Timetabling/Muller-Rudova-Bartak)
- **FATO (literatura):** El Sakkout e Wallace, "Probe Backtrack Search for Minimal Perturbation in Dynamic Scheduling", Constraints 5(4):359–388, 2000, DOI 10.1023/A:1009856210543. É uma busca completa baseada em reparo; a versão anterior saiu no ECAI 1998 ("Minimal Perturbance in Dynamic Scheduling") — [dblp](https://dblp.org/rec/journals/constraints/SakkoutW00)

### Inferences
- **OPINIÃO (desenho recomendado para o M2):** "re-solve" = reconstruir o modelo (barato) + travas fixas + hint completo do plano anterior + termo de estabilidade no objetivo.
  - O termo de estabilidade: `λ·Σ|idx_i − idx_i^prev|` sobre os índices de linha de cada cômodo, ou `Σ b_i`, onde `b_i` indica "o cômodo i mudou de célula".
  - Na fase 2 (geometria), o análogo é `λ·Σ|pos_linha − pos_linha^prev|`.
  - É o MPP formulado como otimização ponderada. O peso λ vira um controle de UI ("quanto pode mudar"). Isso segue a regra do projeto de que observação vira critério, não restrição dura.
- **HIPÓTESE:** como o PyGridPlan já separa topologia e geometria, a re-solução mais barata e frequente é **só a fase 2** (topologia fixa, 0,3 unidades determinísticas). Ela só é possível quando a mudança do usuário não exige outra topologia (por exemplo, mexer em parede ou medida). A fase 1 entra quando o usuário trava um cômodo em outra posição topológica.
- **HIPÓTESE:** para "outras alternativas parecidas", vale mais rodar solves separados com restrições de diversidade/no-good (o padrão atual de 4 alternativas) do que o `solution_pool_size`, que é interno ao LNS.

### Gaps
- Não achei declaração oficial em developers.google.com dizendo "CP-SAT não é incremental". As fontes são mantenedores no fórum, o Primer e o CPMpy.
- Não achei medições do custo de construir o modelo vs clonar o proto em Python na 9.15. A release 9.15 cita "Optimize Python layer, speed up proto generation" sem números ([Releases](https://github.com/google/or-tools/releases)). É para medir no experimento.
- Não li o texto completo dos artigos de MPP. Os detalhes de algoritmo vêm dos resumos.

## 4. Latência, comportamento anytime, streaming, cancelamento e GIL

### Takeaway
Na 9.15 o `solve` Python **libera o GIL** durante a busca, então o servidor continua respondendo. `stop_search()` é assíncrono e seguro para chamar de outra thread. Os callbacks de solução, de log e de limite reacquirem o GIL a cada chamada, então devem ser leves. Para streaming na UI, o padrão é callback de solução → fila → thread do servidor → front-end. Não há números oficiais de latência sub-segundo. A literatura de layout interativo reporta de 0,1 a 5 s.

### Cited Findings
- **FATO (código 9.15):** o binding pybind11 de `SolveWrapper.solve` executa `solve_wrapper->Solve(*model_proto)` dentro de `::py::gil_scoped_release release;`. Os callbacks de solução (`PySolutionCallback::OnSolutionCallback`), de log e de limite (`add_best_bound_callback`) fazem `::py::gil_scoped_acquire`. Uma exceção Python dentro de um callback é guardada, chama `StopSearch()` e é relançada depois do solve. Há `#if !defined(Py_GIL_DISABLED)` para Python sem GIL — [cp_model_helper.cc (stable) ~l. 75–97, 1236–1306](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/python/cp_model_helper.cc)
- **FATO (código 9.15):** `CpSolver.stop_search()`: "Stops the current search asynchronously." Usa um lock interno e só atua se houver um `SolveWrapper` ativo. `CpSolver.solve()` registra `log_callback` e `best_bound_callback` se estiverem definidos — [cp_model.py (stable) ~l. 1752–1785](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/python/cp_model.py)
- **FATO (histórico):** num fio antigo, com o wrapper SWIG, um usuário relatou que o interpretador ficava parado durante o solve e que o stop vindo de outra thread só valia na solução seguinte. Adicionar suporte a threads no SWIG resolveu — [or-tools-discuss](https://groups.google.com/g/or-tools-discuss/c/IQVyGoJTe9w). A observação não vale para a 9.15 (pybind11 com liberação explícita do GIL, ver acima).
- **FATO (release notes):**
  - v9.10: "Add best bound callback".
  - v9.11, problema conhecido: "CP-SAT callbacks in Python, Java, .NET can slow down search performance a lot".
  - v9.15 (jan/2026): "Improve support for gil-less Python 3.14", "Optimize Python layer…" e o problema conhecido "sat: `CpSolver.Solve()` callback breaking argument change" (#4988).
  — [GitHub Releases](https://github.com/google/or-tools/releases)
- **FATO:** o Primer avisa: "Be careful when using callbacks, as they can slow down the solver significantly". Há relatos de usuários com a maior parte do tempo gasta no callback Python. Também: "CP-SAT does not support adding lazy constraints from these callbacks (or at all)". Com `log_search_progress=True` e `solver.log_callback = print`, sai uma linha de log por solução ou limite novo, o que também permite parar a busca a partir do log — [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html)
- **FATO (parâmetros, proto 9.15):**
  - `stop_after_first_solution` (98, default `false`): "For an optimization problem, stop the solver as soon as we have a solution."
  - `max_time_in_seconds` (36, default `inf`): "The counter will starts at the beginning of the Solve() call."
  - `max_deterministic_time` (67, default `inf`): "The deterministic time should be correlated with the real time used by the solver, the time unit being as close as possible to a second."
  - `num_workers` (206, default `0` = todos os núcleos; `1` = sem paralelismo).
  - `log_search_progress` (41, default `false`).
  — [sat_parameters.proto](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto)
- **FATO:** o conjunto de subsolvers cresce com o número de workers (Primer, medido na 9.9):
  - 1 worker: só `default_lp`;
  - 2 workers: começam os incompletos (LNS etc.);
  - 5 workers: entra `fj_short_default`;
  - 32 workers: "all 15 full problem subsolvers are used".
  — [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/parameters.html)
- **FATO (código 9.15):** em `interleave_search`, os subsolvers `probing`, `objective_shaving`, `lb_tree_search` e `objective_lb_search` são excluídos, e o filtro de quantos subsolvers completos manter também é pulado — [cp_model_search.cc (stable) ~l. 943–997](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_search.cc)
- **FATO (literatura, latência):**
  - **GRIDS** (Dayama et al., CHI 2020; MILP no Gurobi, i7 8 núcleos): "5 well-structured layouts are produced within 2 seconds" para 5 elementos; para 12 elementos, "the first 5 solutions are generated within 5 seconds; 10–20 further solutions are generated within 30 seconds" — [arXiv 2001.02921 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2001.02921)
  - **ORCSolver** (Jiang et al., CHI 2020): tempos que "reach at most 0.1 - 0.3 seconds", descritos como "near-interactive rates", e "more than two orders of magnitude faster than Z3 with more than 100 widgets". Os autores dizem: "our current implementation does not support incremental solving" — [arXiv 2002.09925 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2002.09925)

### Inferences
- **OPINIÃO (padrão para o servidor M2):** rodar `solver.solve()` numa thread de trabalho, ou numa thread de um `ThreadPoolExecutor` com o loop asyncio. O callback de solução só copia os valores essenciais (os índices de linha, não o modelo inteiro) para uma `queue`, e o servidor empurra para a UI por SSE ou WebSocket. Um pedido novo do usuário chama `stop_search()` no solve em curso antes de disparar o próximo: padrão "último pedido vence", com debounce.
- **HIPÓTESE:** como o callback reacquire o GIL, e o servidor também usa o GIL, callbacks pesados competem com o servidor. Manter o callback em microssegundos (copiar ints) evita isso. O "problema conhecido" da 9.11 sugere testar o custo real com 8 workers.
- **HIPÓTESE:** para latência percebida, o mais eficaz é (1) hint completo do plano anterior, que dá solução imediata quando continua viável, e (2) re-solve só da fase 2 quando a topologia não muda, que já é 0,3 unidade determinística. `stop_after_first_solution` serve para "pré-visualizar já", mas com 8 workers a primeira solução vem de qualquer worker e pode ser fraca.
- **HIPÓTESE:** `max_deterministic_time` é a unidade certa para reprodutibilidade (Q5), mas não garante latência em segundos. O ideal é combinar com um teto de segurança em `max_time_in_seconds`, sabendo que, se o teto disparar, o resultado deixa de ser reprodutível.
- **OPINIÃO:** os números dos artigos (0,1–0,3 s no ORCSolver; 2–5 s para as primeiras soluções no GRIDS) sugerem um alvo realista para o PyGridPlan: pré-visualização ≤ ~0,5 s (hint/fase 2) e refinamento progressivo em segundos, com a UI mostrando "melhorando…".

### Gaps
- Não achei números oficiais ou publicados de latência sub-segundo do CP-SAT para modelos com dezenas ou centenas de variáveis, nem do overhead fixo de um solve com 8 workers (inicialização do pool de threads, presolve). Fica para o experimento medido.
- Não achei fonte primária para os limiares clássicos de interatividade (0,1 s / 1 s / 10 s). Se o relatório for citá-los, precisa de outra fonte.
- Não verifiquei o conteúdo da issue #4988 (mudança de argumento do callback na 9.15). Convém conferir antes de escrever o código do callback.

## 5. Determinismo e reprodutibilidade com múltiplos workers

### Takeaway
Oficialmente, o modo `interleave_search` é "deterministic (independently of num_workers!)", desde que o `interleave_batch_size` seja fixo e a parada seja **determinística** (dtime ou número de lotes). Já a busca paralela padrão não é determinística, e o solve com 1 worker é. A irreprodutibilidade observada no PyGridPlan (objetivos de 4,21 a 4,85) com `interleave_search=True` é anômala pela documentação e tem causas prováveis a verificar.

### Cited Findings
- **FATO (proto 9.15, verbatim):** "Experimental. If this is true, then we interleave all our major search strategy and distribute the work amongst num_workers. The search is deterministic (independently of num_workers!), and we schedule and wait for interleave_batch_size task to be completed before synchronizing and scheduling the next batch of tasks." O mesmo proto traz `max_num_deterministic_batches` (291): "Stops after that number of batches has been scheduled. This only make sense when interleave_search is true." — [sat_parameters.proto](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto)
- **FATO (código 9.15):** com `interleave_batch_size = 0`, o solver usa `num_workers * 3` (ou 1 se houver 1 worker) e registra "Setting number of tasks in each batch of interleaved search to …". O log de início diz "Starting deterministic search at …s with %i workers and batch size of %d". `DeterministicLoop` gera todas as tarefas do lote antes de executá-las ("if a task finish before we schedule everything, we will not be deterministic") e sincroniza a cada lote — [cp_model_solver.cc ~l. 806–833](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver.cc); [subsolver.cc ~l. 130–170](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/subsolver.cc)
- **FATO (consequência do default):** como o tamanho de lote padrão depende de `num_workers` (×3), o resultado "independente de num_workers" só vale com `interleave_batch_size` explícito. Didier: "For a fixed batch size, the result should be deterministic, independently of the number of workers"; "you usually want the batch size to be around twice the number of workers" — [or-tools-discuss, "Seeding CP-SAT solver" (2023-10-25)](https://groups.google.com/g/or-tools-discuss/c/lPb1FzhTMt0)
- **FATO:** Perron, em 2023-10-24, sugeriu `interleave_search:true, share_binary_clause:false, num_workers:16`, que "Will start a deterministic search with 16 workers" e é "usually way slower than the non deterministic version". Também: "Single thread solve is already deterministic". No mesmo fio, um usuário com interleave e batch fixo relatou "I'm not getting deterministic solutions yet", sem resolução visível — [or-tools-discuss](https://groups.google.com/g/or-tools-discuss/c/lPb1FzhTMt0)
- **FATO:** Perron, em 2018-11-28: "parallel search is not deterministic" (modo padrão) — [or-tools-discuss](https://groups.google.com/g/or-tools-discuss/c/i3TF_Szuz_k)
- **FATO (proto 9.15):** `share_binary_clauses` (203) tem default `true` e `share_glue_clauses` (285) também (este fica desligado implicitamente se o primeiro for `false`). `share_linear2_bounds` (326, default `false`) traz "Warning: This currently non-deterministic." `random_seed` (31, default `1`): "If you change the random seed, the solver may make different choices" — [sat_parameters.proto](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto)
- **FATO (código 9.15):** um comentário em `FullProblemSolver::Synchronize` diz: "A few of the information sharing we do between threads does not happen here (bound sharing, RINS neighborhood, objective). Fix that so we can have a deterministic parallel mode." — [cp_model_solver.cc ~l. 1189–1191](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/cp_model_solver.cc)

### Inferences
- **HIPÓTESES para a irreprodutibilidade observada (4,21–4,85), em ordem de suspeita:**
  1. Há um limite em **segundos** ativo (`max_time_in_seconds`, ou um `stop_search` por relógio ou timeout no código). Qualquer parada por wall-clock quebra o determinismo.
  2. O log não mostra "Starting deterministic search", ou seja, o `interleave_search` não está chegando ao solver em alguma das fases (por exemplo, parâmetros recriados na fase 1, 2 ou nas alternativas).
  3. O compartilhamento de cláusulas está ativo (`share_binary_clauses=true` por padrão), e Perron o desliga explicitamente na receita determinística.
  4. Callbacks Python chamam `stop_search` com base em tempo.
  5. Diferenças na construção do modelo entre execuções: ordem de iteração de `set`/`dict` com hash aleatório gera um proto diferente. Esse ponto **não é do solver**, mas causa exatamente esse sintoma.
- **OPINIÃO:** teste barato para o experimento: mesmo proto serializado (`model.proto` salvo em disco) → 5 execuções com `interleave_search=True`, `interleave_batch_size=16` explícito, `share_binary_clauses=False`, só `max_deterministic_time`, `log_search_progress=True`. Se ficar determinístico, a causa está nos itens 1–5; se não, é bug a reportar.
- **OPINIÃO:** se o modo determinístico for lento demais para a UI, o compromisso é usar o modo paralelo não determinístico para o interativo e o modo determinístico (ou 1 worker) para testes e fixtures.

### Gaps
- Não encontrei declaração oficial dizendo se o compartilhamento de cláusulas é ou não determinístico no `interleave_search` da 9.15. O comentário do código é ambíguo.
- Não há fonte sobre a reprodutibilidade entre máquinas ou versões diferentes no modo interleave.

## 6. Literatura de ferramentas interativas de layout baseadas em restrições/otimização (travas, latência, controle do usuário)

### Takeaway
As ferramentas de layout interativo convergem em três pontos: o usuário **trava** elementos e o otimizador preenche o resto; o sistema mostra **várias sugestões** em vez de uma; e a latência fica entre décimos de segundo e poucos segundos, com resultados aparecendo progressivamente. Para plantas baixas, a separação topologia → geometria do PyGridPlan tem precedente direto em Medjdoub e Yannou (2000).

### Cited Findings
- **FATO:** GRIDS (Dayama, Todi, Saarelainen e Oulasvirta, CHI 2020) é um MILP para grades de layout de UI. Tem "lock button to fix canvas elements" e preferências de posição por menu. Em desenhos parciais, os elementos colocados ficam e o otimizador busca posições para o resto. O tamanho do problema é O(n²) no número de elementos e independe do tamanho do canvas (cerca de 110 variáveis discretas e 20 contínuas para 5 elementos). O gerador de soluções relaxa o alinhamento progressivamente para obter mais alternativas. Não há números de tempo para o caso com travas — [arXiv 2001.02921 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2001.02921); [página do projeto](https://userinterfaces.aalto.fi/grids)
- **FATO:** ORCSolver (Jiang, Stuerzlinger, Zwicker e Lutteroth, CHI 2020) usa branch-and-bound com pré-processamento heurístico para restrições OR em GUIs adaptativas, com 0,1–0,3 s. Quando as restrições OR são eliminadas, pode delegar a um resolvedor linear como Cassowary ou OSQP. Não tem resolução incremental nem warm start (deixados como trabalho futuro), e "pinning" não é tratado — [arXiv 2002.09925 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2002.09925)
- **FATO:** Cassowary (Badros, Borning e Stuckey; UW TR 98-06-04, versão em ACM TOCHI) é "an incremental algorithm based on the dual simplex method" para igualdades e desigualdades lineares em UIs. Usa hierarquia de restrições (obrigatórias vs preferências com força) e deriva do trabalho de UIST 1997 (Borning, Marriott, Stuckey e Xiao), que também descreve o QOCA (mínimos quadrados) — [Cassowary TR](https://constraints.cs.washington.edu/solvers/cassowary-tr.html); [Wikipedia](https://en.wikipedia.org/wiki/Cassowary_(software))
- **FATO:** Medjdoub e Yannou, "Separating Topology and Geometry in Space Planning", Computer-Aided Design 32(1):39–61, 2000, DOI 10.1016/S0010-4485(99)00084-6. Uma heurística de enumeração gera um conjunto completo de "topological solutions", sem dimensões, que o arquiteto explora ("this topological solution space, which is of rather small size") antes de escolher algumas para estudo geométrico detalhado. O artigo de continuação (AI in Engineering, 2001) acrescenta ordenação dinâmica de espaços e refinamento geométrico por custo (área útil, comprimento de parede) — [arXiv 1303.4017 / resumo](https://arxiv.org/pdf/1303.4017); [NTU repositório](https://irep.ntu.ac.uk/id/eprint/30855/)
- **FATO:** o MPP (Barták, Müller e Rudová) e o "probe backtracking" (El Sakkout e Wallace) formalizam a re-solução estável depois de mudanças. Ver Q3 — [Masaryk Univ.](https://is.muni.cz/publication/621512/en/Minimal-Perturbation-Problem-in-Course-Timetabling/Muller-Rudova-Bartak); [dblp](https://dblp.org/rec/journals/constraints/SakkoutW00)

### Inferences
- **OPINIÃO:** o padrão de interação do GRIDS (cadeado por elemento, preferências por menu, galeria de alternativas atualizada a cada mudança) mapeia direto para o M2 do PyGridPlan: cadeado por cômodo ou parede, pesos de critérios e 4 alternativas. A diferença é que o GRIDS não precisa explicar inviabilidade, porque grades de UI raramente ficam inviáveis. Plantas com travas conflitantes ficam, daí a Q1.
- **OPINIÃO:** Cassowary e QOCA mostram o padrão "travas = restrições obrigatórias, desejos = preferências com peso", que combina com a regra do projeto (norma é referência, não teto). Mas são resolvedores lineares contínuos: não servem para a fase 1 (combinatória). No máximo inspiram a fase 2 (mover linhas com topologia fixa).
- **HIPÓTESE:** Medjdoub e Yannou sugerem que, se o espaço topológico for pequeno, **enumerar ou guardar em cache** as topologias viáveis permite que a re-solução interativa mais comum (mexer em medidas ou paredes) rode só na geometria. Isso reforça a estratégia de re-solve da fase 2 da Q3/Q4.

### Gaps
- Não achei trabalho recente (2023–2026) sobre ferramentas de planta baixa interativas com CP-SAT especificamente, com latência medida e travas. Os exemplos encontrados são de layout de UI (GRIDS, ORCSolver, Cassowary) ou de planejamento espacial clássico (Medjdoub e Yannou).
- Não li os textos completos do Cassowary (restrições "edit"/"stay" e tempos por re-solve) nem do Medjdoub e Yannou (aspecto interativo e tempos). O que está acima vem de resumos e páginas de registro.
- Não pesquisei a fundo DesignScape, Sketchplore, "mixed-initiative" em geral nem "Layout as a Service". Ficam como pendência se o relatório precisar de mais exemplos.
