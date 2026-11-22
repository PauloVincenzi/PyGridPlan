# Experimento medido: travar cômodos e re-resolver no gerador CP-SAT

> Notas de pesquisa (trilha "Arquitetura interativa do M2"). Criado em 2026-11-22 · versão 1.
> Experimento **só de medição**: nada em `src/`, `tests/` ou `data/` foi alterado, e nada foi commitado. O código do experimento fica no scratchpad da sessão do agente (fora do git; uma limpeza do sistema pode apagá-lo). Os caminhos estão na seção 4.
> Convenção: **FATO** = medido neste experimento (número tirado dos arquivos de resultado); **HIPÓTESE** = interpretação minha, a confirmar.
> Complementa [re-solucao-interativa-cpsat.md](re-solucao-interativa-cpsat.md), que reuniu fontes sem rodar nada.

## 1. Objetivo

Medir, no gerador real (`src/pygridplan/generators/cpsat.py`, commit `672af29`), quanto custa a ação "travar 1 a 3 cômodos e re-resolver" depois que o usuário muda algo no pedido. As perguntas são:

1. Qual a latência da re-solução, e quanto as travas reduzem a busca.
2. Se uma dica (`AddHint`) montada com a planta anterior ajuda.
3. Se um limite curto (`max_deterministic_time = 2`) dá latência interativa, e com que perda de qualidade.
4. Quanto o resultado varia de uma rodada para outra.

## 2. Ambiente

| Item | Valor |
|---|---|
| SO | Windows 11 Home Single Language 10.0.26300 |
| CPU | 13th Gen Intel Core i5-1335U: 10 núcleos físicos e 12 lógicos (WMI) |
| Python | 3.13.14 (`.venv` do projeto) |
| OR-Tools | 9.15.6755 |
| Solver | configuração do repositório: `num_workers=8`, `interleave_search=True`, `random_seed=0`, fase 1 com `DEFAULT_TIME_LIMIT=20` unidades determinísticas (dt), fase 2 com `POLISH_TIME=0,3` |
| Data | 2026-11-22, das 09:01 às 09:27 |

**Carga da máquina (FATO).** Antes das medições, a CPU total oscilava entre 18 % e 76 % (amostras do WMI, sem processos meus). Os maiores consumidores eram o VS Code e o WmiPrvSE.

- **Primeira tentativa, descartada.** Outro agente rodava ao mesmo tempo um benchmark CP-SAT (`repro.py`, três processos de 8 workers cada). A planta-base do `basic-program` levou 64 s de relógio contra 27,6 s depois. Os dados dessa tentativa estão em `contaminated/` e não entram nas tabelas.
- **Rodada válida.** Dois processos `python` alheios (PIDs 27892 e 12408, de identidade não registrada) estavam ativos durante as plantas-base e as primeiras 49 das 115 execuções. Cada linha dos resultados guarda os PIDs alheios vistos antes e depois da execução, e a coluna "conc." das tabelas marca essas linhas.
- **Efeito medido da concorrência.** O tempo determinístico não muda, mas o tempo de relógio cresce cerca de 60 %:
  - `small-lot` k=0: 13,46 dt nos dois casos; 16,2 s com concorrência e 9,7 s sem;
  - `basic-program` k=0 com limite curto: 8,07 dt sempre; 12,7 s com concorrência e 7,8 a 8,0 s sem.
- No fim, `tasklist` não mostrou nenhum `python.exe` meu nem alheio, e a CPU estava entre 12 % e 29 %.

## 3. Método

### 3.1 Código do experimento × código do repositório

`make_exp_module.py` lê `cpsat.py` e grava `cpsat_exp_v2.py`, com substituições textuais verificadas (cada trecho-âncora precisa aparecer exatamente uma vez). O diff completo está em `cpsat_exp_v2.diff`. As diferenças são:

1. `_phase` ganhou os parâmetros `locks`, `hint`, `fix_hint` e `stats`. Sem eles, o modelo é idêntico ao do repositório.
2. Logo antes do bloco `# objetivo`, uma chamada aplica as travas e a dica parcial (prefixo).
3. Logo antes de criar o `CpSolver`, uma chamada aplica a dica completa (só quando a dica traz um valor para **todas** as variáveis do modelo).
4. `solver.solve(m)` passou a ser `solver.solve(m, callback)`. O callback anota o instante e o objetivo da 1.ª solução e conta as soluções, e as estatísticas são copiadas para `stats`. **Ressalva:** o callback pode mudar um pouco o tempo de relógio. Não medi esse efeito.
5. `solve_x` (em `relock_experiment.py`) repete `cpsat._solve`: tenta os `SHAPE_ATTEMPTS` em ordem e polir na fase 2, passando as travas às duas fases. A dica só vai para a fase 1, porque a fase 2 já recebe a topologia fixa.
6. A planta-base repete `cpsat._attach_if_needed`: se o pedido não coube e não tinha lado encostado, tenta encostar nas divisas. O `small-lot` só coube **encostado à esquerda**, e todas as re-soluções dele usam o pedido encostado.
7. `min_diff` foi calculado como em `generate_alternatives`, mas não tem efeito, porque não há padrões proibidos.

**Conferência (FATO).** `solve_layout` do repositório devolveu os mesmos retângulos da planta-base do experimento em `one-bedroom` e `small-lot` (encostado), que são os dois pedidos com ótimo provado. Nos pedidos que param no limite de tempo, essa conferência não tem sentido, porque o próprio gerador não é reprodutível nesse caso (ver 5.3).

### 3.2 Planta-base

É a 1.ª solução que `generate_alternatives` obteria: `_solve` com semente 0 e limite de 20 dt. Para cada pedido guardei os retângulos (x, y, w, h em unidades de 100 mm) e os valores de todas as variáveis da fase 2 polida.

### 3.3 Travas

**Travar um cômodo** = quatro igualdades no modelo de malha: `x == x0`, `y == y0`, `w == w0` e `h == h0`, sobre as variáveis reais do cômodo (`cells[k].x`, `cells[k].y`, `w[k]`, `h[k]`), com os valores da planta-base. Valem nas duas fases.

**Por que não fixar os índices da malha.** Fixar `c1/c2/r1/r2` amarra a numeração das linhas, e a mesma planta pode ter outra numeração depois da perturbação. As igualdades em x/y/w/h fixam só o que o usuário vê, e o solver continua livre para reorganizar a malha em volta. A posição das linhas que passam pelo cômodo travado sai como consequência.

**Resultado (FATO):** nas 115 execuções, os cômodos travados terminaram exatamente onde estavam. O script verifica isso com `assert` em cada execução.

**Regra de escolha:** ordenar os cômodos pela área-alvo efetiva (`room_target_m2`) decrescente, desempatando pela ordem do pedido. Cômodos sem alvo (circulação) vão para o fim. Com k travas, travam-se os k primeiros.

### 3.4 Perturbação

É a mesma para todo k: a área-alvo do **4.º cômodo da ordem** (que nunca é travado com k ≤ 3) sobe 25 % (`target_area_m2 = 1,25 × alvo efetivo`). k = 0 é a perturbação sem travas, usada como referência.

| Pedido | Cômodos | Travas (ordem) | Perturbado (alvo antigo → novo) |
|---|---|---|---|
| one-bedroom | 4 | sala, quarto, cozinha | banheiro (2,40 → 3,00 m²) |
| small-lot (encostado à esq.) | 6 | sala, quarto1, quarto2 | cozinha (3,60 → 4,50 m²) |
| basic-program | 8 | sala, quarto1, cozinha | quarto2 (10,00 → 12,50 m²) |
| three-bedroom | 9 | sala, suite, cozinha | quarto2 (10,00 → 12,50 m²) |
| large-house | 12 | sala, suite, jantar | cozinha (12,00 → 15,00 m²) |

### 3.5 Dicas

- **Prefixo** (`fast_partial`): os valores da planta-base para todas as variáveis criadas **antes** do bloco do objetivo. A ordem de criação é a mesma nos dois modelos, então o índice no proto também é: 167 a 596 variáveis, conforme o pedido. As auxiliares do objetivo (janelas de área, |dx|, `reached` etc.) ficam sem dica, e por isso essa dica é **incompleta**.
- **Completa** (`hinted`, `fast_hint`): o modelo perturbado, com as travas, é resolvido uma vez com o prefixo **fixado** (`fix_hint=True`, cerca de 20 ms). Se der viável, essa solução dá valor a **todas** as variáveis, inclusive as do objetivo, e vira a dica. Se der inviável, a planta-base não satisfaz o modelo perturbado, e a variante cai para a dica de prefixo (marcada "dica inviável → prefixo" nas tabelas). O tempo dessa conclusão entra no total da variante.
- **Viabilidade da dica (FATO):** a dica foi viável nos k = 0 a 3 de quatro pedidos. No `large-house` foi **inviável em todos os k**: o retângulo da cozinha (10,44 m² brutos) fica abaixo do novo piso de 0,7 × 15 m² de área útil.

### 3.6 Variantes

| Variante | Dica | Limite da fase 1 | Quais k |
|---|---|---|---|
| `cold` | nenhuma | 20 dt (padrão) | 0, 1, 2, 3 |
| `hinted` | completa | 20 dt | 0, 1, 2, 3 |
| `fast_cold` | nenhuma | 2 dt | 0, 1, 2, 3 |
| `fast_partial` | prefixo | 2 dt | 0, 1, 2, 3 |
| `fast_hint` | completa | 2 dt | 0, 1, 2, 3 |

**Métricas.** Os tempos de relógio são medidos com `perf_counter` por fase. "F1 (s)" soma a montagem do modelo e o `solve` de **todas** as tentativas de formato. "Total" inclui a fase 2 e, nas variantes com dica completa, o tempo de completá-la. Também registro, por execução:

- o tempo determinístico (`deterministic_time`, somado nas tentativas);
- o status, o objetivo e o limite superior (gap = |limite − obj| / |limite|);
- o instante da 1.ª solução. Ele é medido a partir do início da tentativa de formato que deu certo; no `small-lot`, isso exclui a prova de inviabilidade do retângulo cheio.

O objetivo da fase 2 só é comparável **dentro** de um pedido, porque o modelo perturbado é o mesmo para todas as variantes daquele pedido. A "nota" é `score_plan(plan, pedido perturbado).total`. "Mudaram" conta quantos cômodos têm retângulo diferente do da planta-base.

### 3.7 Extras

- **Repetições:** 3 rodadas a mais, todas com semente 0, de cinco casos (seção 5.3).
- **Diagnóstico do limite curto:** um log do CP-SAT (`diag_dt.py`) e quatro execuções variando o limite e o `interleave_search` (`diag_limit.py`). Esse diagnóstico usa uma configuração diferente da do repositório e serve só para explicar o que foi medido.

## 4. Arquivos (scratchpad, fora do git)

Pasta: `C:\Users\paulo\AppData\Local\Temp\claude\d0e1a6539163643b\be01e520-0af3-4256-97cf-65e37e9d9285\scratchpad\m2-relock\`

| Arquivo | Conteúdo |
|---|---|
| `...\m2-relock\make_exp_module.py` | gera a cópia instrumentada do gerador |
| `...\m2-relock\cpsat_exp_v2.py` e `...\m2-relock\cpsat_exp_v2.diff` | cópia instrumentada e o diff contra `cpsat.py` |
| `...\m2-relock\relock_experiment.py` | experimento (`baseline`, `runs A/B/C`, `repeat`) |
| `...\m2-relock\baseline.json` | plantas-base, ordem de travas, dicas |
| `...\m2-relock\results.jsonl` | **resultados brutos** (115 execuções e 20 checagens de dica, uma linha por execução) |
| `...\m2-relock\summarize.py`, `...\m2-relock\compact.py`, `...\m2-relock\tables.md`, `...\m2-relock\tables_compact.md` | geração das tabelas |
| `...\m2-relock\diag_dt.py`, `...\m2-relock\diag_basic_k0_dt2.log`, `...\m2-relock\diag_limit.py`, `...\m2-relock\diag_limit.jsonl` | diagnóstico do limite curto |
| `...\m2-relock\run_main.log`, `...\m2-relock\run_c.log` | saída das execuções |
| `...\m2-relock\contaminated\` | tentativa descartada (concorrência pesada) |

## 5. Resultados

### 5.1 Plantas-base

| Pedido | Formato | Total (s) | F1 status | F1 dt | F1 gap | 1.ª sol. (s) | F2 (s) | Nota |
|---|---|---|---|---|---|---|---|---|
| one-bedroom | 0 (retângulo) | 0,61 | OPTIMAL | 0,08 | 0 % | 0,17 | 0,25 | 0,913 |
| small-lot | 1 (retângulo, teto 2,0), encostado à esq. | 15,8 (+14,0 da tentativa sem encostar, provada inviável) | INFEASIBLE → OPTIMAL | 6,79 + 6,95 | 0 % | 0,38 | 0,06 | 0,919 |
| basic-program | 0 | 27,6 | FEASIBLE (parou no limite) | 25,6 | 6,6 % | 0,75 | 1,25 | 0,923 |
| three-bedroom | 0 | 38,2 | FEASIBLE | 27,3 | 6,6 % | 0,67 | 2,86 | 0,955 |
| large-house | 0 | 36,8 | FEASIBLE | 20,1 | 15,7 % | 1,19 | 3,41 | 0,887 |

Todas foram medidas com dois processos alheios ativos (seção 2).

### 5.2 Re-solução por pedido × k × variante (rodada 0)

Total = F1 + F2 (+ conclusão da dica, cerca de 0,02 s). Gap da fase 1 em %. A F2 deu OPTIMAL em todas as execuções. Nenhuma planta teve erro de geometria (`validate_geometry`) nem de acesso (`check_access`).

#### one-bedroom

| k | variante | total (s) | F1 (s) | F1 dt | F1 status | F1 gap % | 1.ª sol. (s) | F2 obj | nota | mudaram | conc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | cold | 0.68 | 0.53 | 0.21 | OPTIMAL | 0.0 | 0.14 | 1.346 | 0.925 | 4 | não |
| 0 | hinted | 0.26 | 0.15 | 0.03 | OPTIMAL | 0.0 | 0.04 | 1.346 | 0.925 | 4 | não |
| 0 | fast_cold | 0.60 | 0.45 | 0.21 | OPTIMAL | 0.0 | 0.08 | 1.346 | 0.925 | 4 | sim |
| 0 | fast_partial | 0.51 | 0.36 | 0.11 | OPTIMAL | 0.0 | 0.09 | 1.346 | 0.925 | 4 | sim |
| 0 | fast_hint | 0.49 | 0.27 | 0.03 | OPTIMAL | 0.0 | 0.12 | 1.346 | 0.925 | 4 | sim |
| 1 | cold | 0.11 | 0.10 | 0.02 | OPTIMAL | 0.0 | 0.08 | 1.313 | 0.925 | 0 | sim |
| 1 | hinted | 0.17 | 0.14 | 0.01 | OPTIMAL | 0.0 | 0.07 | 1.313 | 0.925 | 0 | sim |
| 1 | fast_cold | 0.16 | 0.14 | 0.02 | OPTIMAL | 0.0 | 0.11 | 1.313 | 0.925 | 0 | sim |
| 1 | fast_partial | 0.23 | 0.21 | 0.02 | OPTIMAL | 0.0 | 0.09 | 1.313 | 0.925 | 0 | sim |
| 1 | fast_hint | 0.17 | 0.15 | 0.01 | OPTIMAL | 0.0 | 0.06 | 1.313 | 0.925 | 0 | sim |
| 2 | cold | 0.12 | 0.09 | 0.00 | OPTIMAL | 0.0 | 0.07 | 1.313 | 0.927 | 2 | sim |
| 2 | hinted | 0.08 | 0.06 | 0.00 | OPTIMAL | 0.0 | 0.03 | 1.313 | 0.925 | 0 | sim |
| 2 | fast_cold | 0.10 | 0.06 | 0.00 | OPTIMAL | 0.0 | 0.05 | 1.313 | 0.927 | 2 | sim |
| 2 | fast_partial | 0.03 | 0.02 | 0.00 | OPTIMAL | 0.0 | 0.02 | 1.313 | 0.925 | 0 | sim |
| 2 | fast_hint | 0.07 | 0.06 | 0.00 | OPTIMAL | 0.0 | 0.03 | 1.313 | 0.925 | 0 | sim |
| 3 | cold | 0.03 | 0.02 | 0.00 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | 0 | sim |
| 3 | hinted | 0.09 | 0.05 | 0.00 | OPTIMAL | 0.0 | 0.03 | 1.313 | 0.925 | 0 | sim |
| 3 | fast_cold | 0.09 | 0.05 | 0.00 | OPTIMAL | 0.0 | 0.03 | 1.313 | 0.925 | 0 | sim |
| 3 | fast_partial | 0.05 | 0.03 | 0.00 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | 0 | sim |
| 3 | fast_hint | 0.10 | 0.08 | 0.00 | OPTIMAL | 0.0 | 0.03 | 1.313 | 0.925 | 0 | sim |

#### small-lot (encostado à esquerda; cada re-solução prova de novo que o formato 0 é inviável e acha a solução no formato 1)

| k | variante | total (s) | F1 (s) | F1 dt | F1 status | F1 gap % | 1.ª sol. (s) | F2 obj | nota | mudaram | conc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | cold | 9.72 | 9.63 | 13.46 | OPTIMAL | 0.0 | 0.21 | 3.661 | 0.928 | 2 | não |
| 0 | hinted | 10.83 | 10.75 | 13.94 | OPTIMAL | 0.0 | 0.11 | 3.661 | 0.928 | 0 | não |
| 0 | fast_cold | 16.16 | 16.04 | 13.46 | OPTIMAL | 0.0 | 0.34 | 3.661 | 0.928 | 2 | sim |
| 0 | fast_partial | 17.38 | 17.20 | 13.85 | OPTIMAL | 0.0 | 0.33 | 3.661 | 0.928 | 2 | sim |
| 0 | fast_hint | 17.85 | 17.77 | 13.96 | OPTIMAL | 0.0 | 0.09 | 3.661 | 0.928 | 0 | sim |
| 1 | cold | 11.93 | 11.90 | 6.38 | OPTIMAL | 0.0 | 0.36 | 3.661 | 0.928 | 0 | sim |
| 1 | hinted | 11.84 | 11.81 | 5.62 | OPTIMAL | 0.0 | 0.12 | 3.661 | 0.928 | 0 | sim |
| 1 | fast_cold | 12.16 | 12.12 | 6.38 | OPTIMAL | 0.0 | 0.23 | 3.661 | 0.928 | 0 | sim |
| 1 | fast_partial | 10.25 | 10.21 | 5.75 | OPTIMAL | 0.0 | 0.09 | 3.661 | 0.928 | 0 | sim |
| 1 | fast_hint | 10.43 | 10.42 | 5.63 | OPTIMAL | 0.0 | 0.23 | 3.661 | 0.928 | 0 | sim |
| 2 | cold | 2.01 | 1.98 | 0.65 | OPTIMAL | 0.0 | 0.23 | 3.661 | 0.928 | 0 | sim |
| 2 | hinted | 1.47 | 1.44 | 0.57 | OPTIMAL | 0.0 | 0.12 | 3.661 | 0.928 | 0 | sim |
| 2 | fast_cold | 2.76 | 2.71 | 0.65 | OPTIMAL | 0.0 | 0.33 | 3.661 | 0.928 | 0 | sim |
| 2 | fast_partial | 1.93 | 1.91 | 0.63 | OPTIMAL | 0.0 | 0.23 | 3.661 | 0.928 | 0 | sim |
| 2 | fast_hint | 1.52 | 1.50 | 0.57 | OPTIMAL | 0.0 | 0.13 | 3.661 | 0.928 | 0 | sim |
| 3 | cold | 0.18 | 0.16 | 0.01 | OPTIMAL | 0.0 | 0.08 | 3.661 | 0.928 | 0 | sim |
| 3 | hinted | 0.22 | 0.18 | 0.01 | OPTIMAL | 0.0 | 0.07 | 3.661 | 0.928 | 0 | sim |
| 3 | fast_cold | 0.30 | 0.27 | 0.01 | OPTIMAL | 0.0 | 0.14 | 3.661 | 0.928 | 0 | sim |
| 3 | fast_partial | 0.11 | 0.10 | 0.01 | OPTIMAL | 0.0 | 0.05 | 3.661 | 0.928 | 0 | sim |
| 3 | fast_hint | 0.25 | 0.24 | 0.01 | OPTIMAL | 0.0 | 0.10 | 3.661 | 0.928 | 0 | sim |

#### basic-program

| k | variante | total (s) | F1 (s) | F1 dt | F1 status | F1 gap % | 1.ª sol. (s) | F2 obj | nota | mudaram | conc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | cold | 22.79 | 21.81 | 25.68 | OPTIMAL | 0.0 | 0.22 | 5.763 | 0.907 | 8 | não |
| 0 | hinted | 19.61 | 18.62 | 23.48 | OPTIMAL | 0.0 | 0.14 | 5.763 | 0.907 | 8 | não |
| 0 | fast_cold | 12.72 | 11.40 | 8.07 | FEASIBLE | 5.9 | 0.47 | 5.763 | 0.907 | 8 | sim |
| 0 | fast_partial | 14.48 | 13.08 | 8.30 | FEASIBLE | 5.9 | 0.25 | 5.763 | 0.907 | 8 | sim |
| 0 | fast_hint | 13.99 | 11.39 | 8.47 | FEASIBLE | 8.6 | 0.22 | 5.763 | 0.907 | 8 | sim |
| 1 | cold | 6.34 | 6.31 | 5.89 | OPTIMAL | 0.0 | 0.22 | 5.689 | 0.917 | 6 | sim |
| 1 | hinted | 3.72 | 3.70 | 4.82 | OPTIMAL | 0.0 | 0.12 | 5.689 | 0.917 | 6 | não |
| 1 | fast_cold | 7.36 | 7.32 | 5.89 | OPTIMAL | 0.0 | 0.26 | 5.689 | 0.917 | 6 | sim |
| 1 | fast_partial | 9.90 | 9.80 | 4.96 | OPTIMAL | 0.0 | 0.40 | 5.689 | 0.917 | 6 | sim |
| 1 | fast_hint | 6.25 | 6.21 | 4.83 | OPTIMAL | 0.0 | 0.12 | 5.689 | 0.917 | 6 | sim |
| 2 | cold | 2.66 | 2.62 | 3.06 | OPTIMAL | 0.0 | 0.35 | 5.770 | 0.919 | 0 | não |
| 2 | hinted | 1.27 | 1.25 | 0.86 | OPTIMAL | 0.0 | 0.13 | 5.770 | 0.919 | 0 | não |
| 2 | fast_cold | 4.91 | 4.88 | 3.06 | OPTIMAL | 0.0 | 0.70 | 5.770 | 0.919 | 0 | sim |
| 2 | fast_partial | 4.67 | 4.64 | 2.16 | OPTIMAL | 0.0 | 0.27 | 5.770 | 0.919 | 0 | sim |
| 2 | fast_hint | 3.10 | 3.03 | 0.86 | OPTIMAL | 0.0 | 0.32 | 5.770 | 0.919 | 0 | sim |
| 3 | cold | 0.44 | 0.41 | 0.12 | OPTIMAL | 0.0 | 0.17 | 5.770 | 0.919 | 0 | não |
| 3 | hinted | 0.31 | 0.29 | 0.07 | OPTIMAL | 0.0 | 0.09 | 5.770 | 0.919 | 0 | não |
| 3 | fast_cold | 0.41 | 0.39 | 0.12 | OPTIMAL | 0.0 | 0.17 | 5.770 | 0.919 | 0 | sim |
| 3 | fast_partial | 0.68 | 0.65 | 0.09 | OPTIMAL | 0.0 | 0.28 | 5.770 | 0.919 | 0 | sim |
| 3 | fast_hint | 0.36 | 0.33 | 0.07 | OPTIMAL | 0.0 | 0.10 | 5.770 | 0.919 | 0 | sim |

#### three-bedroom

| k | variante | total (s) | F1 (s) | F1 dt | F1 status | F1 gap % | 1.ª sol. (s) | F2 obj | nota | mudaram | conc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | cold | 22.57 | 21.21 | 26.73 | FEASIBLE | 5.9 | 0.40 | 7.129 | 0.952 | 9 | não |
| 0 | hinted | 24.19 | 22.76 | 27.35 | FEASIBLE | 5.2 | 0.19 | 7.129 | 0.952 | 9 | não |
| 0 | fast_cold | 8.07 | 6.93 | 8.09 | FEASIBLE | 10.6 | 0.39 | 7.036 | 0.951 | 9 | não |
| 0 | fast_partial | 9.07 | 7.56 | 8.35 | FEASIBLE | 6.3 | 0.21 | 7.129 | 0.952 | 9 | não |
| 0 | fast_hint | 9.59 | 8.04 | 8.60 | FEASIBLE | 6.3 | 0.19 | 7.129 | 0.952 | 9 | não |
| 1 | cold | 7.10 | 6.40 | 7.17 | OPTIMAL | 0.0 | 0.58 | 7.021 | 0.952 | 0 | não |
| 1 | hinted | 7.30 | 6.23 | 7.05 | OPTIMAL | 0.0 | 0.16 | 7.021 | 0.952 | 0 | não |
| 1 | fast_cold | 7.37 | 6.72 | 7.17 | OPTIMAL | 0.0 | 0.71 | 7.021 | 0.952 | 0 | não |
| 1 | fast_partial | 6.64 | 5.68 | 6.91 | OPTIMAL | 0.0 | 0.20 | 7.021 | 0.952 | 2 | não |
| 1 | fast_hint | 7.43 | 6.41 | 7.06 | OPTIMAL | 0.0 | 0.16 | 7.021 | 0.952 | 0 | não |
| 2 | cold | 3.52 | 3.48 | 3.87 | OPTIMAL | 0.0 | 0.38 | 7.021 | 0.952 | 2 | não |
| 2 | hinted | 2.14 | 2.11 | 1.83 | OPTIMAL | 0.0 | 0.15 | 7.021 | 0.952 | 0 | não |
| 2 | fast_cold | 3.45 | 3.42 | 3.87 | OPTIMAL | 0.0 | 0.35 | 7.021 | 0.952 | 2 | não |
| 2 | fast_partial | 3.46 | 3.42 | 2.90 | OPTIMAL | 0.0 | 0.19 | 7.021 | 0.952 | 4 | não |
| 2 | fast_hint | 2.07 | 2.03 | 1.83 | OPTIMAL | 0.0 | 0.16 | 7.021 | 0.952 | 0 | não |
| 3 | cold | 2.86 | 2.84 | 1.54 | OPTIMAL | 0.0 | 0.29 | 7.021 | 0.952 | 0 | não |
| 3 | hinted | 0.77 | 0.74 | 0.43 | OPTIMAL | 0.0 | 0.13 | 7.021 | 0.952 | 0 | não |
| 3 | fast_cold | 2.93 | 2.90 | 1.54 | OPTIMAL | 0.0 | 0.27 | 7.021 | 0.952 | 0 | não |
| 3 | fast_partial | 2.93 | 2.91 | 1.60 | OPTIMAL | 0.0 | 0.17 | 7.021 | 0.952 | 0 | não |
| 3 | fast_hint | 0.76 | 0.73 | 0.42 | OPTIMAL | 0.0 | 0.14 | 7.021 | 0.952 | 0 | não |

#### large-house (dica completa inviável em todos os k: as variantes "hinted" usaram só o prefixo)

| k | variante | total (s) | F1 (s) | F1 dt | F1 status | F1 gap % | 1.ª sol. (s) | F2 obj | nota | mudaram | conc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | cold | 25.57 | 24.10 | 20.33 | FEASIBLE | 14.3 | 1.50 | 6.379 | 0.907 | 12 | não |
| 0 | hinted (dica inviável → prefixo) | 23.86 | 22.47 | 20.52 | FEASIBLE | 13.6 | 1.58 | 6.679 | 0.926 | 12 | não |
| 0 | fast_cold | 9.90 | 8.53 | 8.09 | FEASIBLE | 34.3 | 1.49 | 5.163 | 0.814 | 12 | não |
| 0 | fast_partial | 10.62 | 9.17 | 8.43 | FEASIBLE | 15.7 | 1.53 | 6.372 | 0.906 | 12 | não |
| 0 | fast_hint (dica inviável → prefixo) | 10.54 | 9.27 | 8.43 | FEASIBLE | 15.7 | 1.59 | 6.372 | 0.906 | 12 | não |
| 1 | cold | 26.60 | 25.92 | 25.34 | FEASIBLE | 26.6 | 0.62 | 5.605 | 0.849 | 11 | não |
| 1 | hinted (dica inviável → prefixo) | 27.24 | 26.67 | 25.47 | FEASIBLE | 17.9 | 5.47 | 6.271 | 0.886 | 11 | não |
| 1 | fast_cold | 8.34 | 8.30 | 8.11 | FEASIBLE | 34.7 | 0.65 | 5.033 | 0.814 | 11 | não |
| 1 | fast_partial | 10.85 | 8.84 | 8.41 | FEASIBLE | 33.5 | 5.56 | 4.901 | 0.808 | 11 | não |
| 1 | fast_hint (dica inviável → prefixo) | 10.52 | 8.52 | 8.41 | FEASIBLE | 33.5 | 5.17 | 4.901 | 0.808 | 11 | não |
| 2 | cold | 7.14 | 7.10 | 7.73 | OPTIMAL | 0.0 | 1.01 | 6.429 | 0.883 | 6 | não |
| 2 | hinted (dica inviável → prefixo) | 9.11 | 9.07 | 8.52 | OPTIMAL | 0.0 | 2.52 | 6.429 | 0.883 | 4 | não |
| 2 | fast_cold | 7.18 | 7.14 | 7.73 | OPTIMAL | 0.0 | 0.94 | 6.429 | 0.883 | 6 | não |
| 2 | fast_partial | 8.80 | 8.76 | 8.26 | OPTIMAL | 0.0 | 2.39 | 6.429 | 0.883 | 4 | não |
| 2 | fast_hint (dica inviável → prefixo) | 8.77 | 8.73 | 8.26 | OPTIMAL | 0.0 | 2.35 | 6.429 | 0.883 | 4 | não |
| 3 | cold | 4.04 | 4.01 | 4.23 | OPTIMAL | 0.0 | 0.60 | 4.879 | 0.845 | 6 | não |
| 3 | hinted (dica inviável → prefixo) | 4.67 | 4.62 | 4.57 | OPTIMAL | 0.0 | 1.05 | 4.879 | 0.845 | 6 | não |
| 3 | fast_cold | 4.10 | 4.06 | 4.23 | OPTIMAL | 0.0 | 0.59 | 4.879 | 0.845 | 6 | não |
| 3 | fast_partial | 4.90 | 4.87 | 4.57 | OPTIMAL | 0.0 | 1.20 | 4.879 | 0.845 | 6 | não |
| 3 | fast_hint (dica inviável → prefixo) | 4.70 | 4.66 | 4.57 | OPTIMAL | 0.0 | 1.15 | 4.879 | 0.845 | 6 | não |

### 5.3 Variação entre rodadas (semente 0; rodada 0 + 3 repetições)

| Pedido | k | Variante | Total (s) por rodada | F1 dt por rodada | F2 obj por rodada | Nota por rodada | Plantas distintas |
|---|---|---|---|---|---|---|---|
| basic-program | 0 | fast_cold | 12.72*, 8.01, 7.84, 7.93 | 8.07 × 4 | 5.763 × 4 | 0.907 × 4 | 1 |
| basic-program | 1 | hinted | 3.72, 3.60, 3.57, 3.53 | 4.82, 4.82, 4.84, 4.84 | 5.689 × 4 | 0.917 × 4 | 1 |
| three-bedroom | 2 | hinted | 2.14, 2.13, 2.08, 2.09 | 1.83 × 4 | 7.021 × 4 | 0.952 × 4 | 1 |
| large-house | 0 | fast_cold | 9.90, 10.14, 9.96, 9.80 | 8.09 × 4 | 5.163 × 4 | 0.814 × 4 | 1 |
| large-house | 1 | cold | 26.60, 26.92, 27.61, 27.17 | 25.34, 25.97, 26.64, 27.09 | 5.605, 6.411, 5.605, 5.873 | 0.849, 0.888, 0.849, 0.872 | **3** |

\* com concorrência (2 processos alheios).

### 5.4 Diagnóstico do limite curto (`diag_limit.jsonl`, `diag_basic_k0_dt2.log`)

| Caso | Limite | interleave | F1 (s) | dt informado | F1 obj (melhor conhecido) |
|---|---|---|---|---|---|
| basic-program k=0 | 2 | sim (repo) | 6,8 a 11,4 | 8,07 | 6,965 (6,965) |
| basic-program k=0 | 0,5 | sim | 3,53 | 3,74 | 6,795 |
| basic-program k=0 | 2 | não | 11,04 | 13,43 | 6,965 |
| basic-program k=0 | 0,5 | não | 3,05 | 3,36 | 6,912 |
| large-house k=1 | 2 | não | 12,66 | 13,68 | 7,449 (7,428 com 20 dt) |

No log com limite 2 e `interleave_search`, cada um dos 8 subsolvers completos rodou 2 tarefas, uma de cerca de 2,5 ms e outra de cerca de 1,0 dt (bloco "Task timing"). Somadas, dão os ≈ 8 dt informados.

## 6. Observações

### FATOS (medidos)

1. **As travas valem sempre.** Em 115 de 115 execuções, os cômodos travados terminaram exatamente na posição e no tamanho da planta-base. Nenhuma planta teve erro de geometria ou de acesso, e a fase 2 provou o ótimo em todas.
2. **As travas encolhem muito a busca.** Com k ≥ 2, a fase 1 provou o ótimo em todos os pedidos. Os tempos de relógio, sem os casos com concorrência, foram:
   - k = 3: de 0,03 s (`one-bedroom`) a 4,0–4,7 s (`large-house`); 0,3–0,4 s (`basic-program`); 0,8–2,9 s (`three-bedroom`);
   - k = 2: 1,3–2,7 s (`basic-program`), 2,1–3,5 s (`three-bedroom`), 7,1–9,1 s (`large-house`);
   - k = 1: 3,7–6,3 s (`basic-program`) e cerca de 7 s (`three-bedroom`), ambos com ótimo provado; o `large-house` **ainda para no limite** (≈ 27 s, FEASIBLE, gap de 18 a 27 %);
   - k = 0: 20 a 26 s nos três pedidos médios e grandes, iguais a uma geração do zero.
3. **A 1.ª solução chega rápido.** Sem dica, a 1.ª solução da fase 1 apareceu entre 0,01 e 1,5 s em todos os casos. Com dica completa e viável, entre 0,03 e 0,3 s, e ela é a própria planta anterior: o objetivo da 1.ª solução é igual ao da dica (ex.: 6,616 no `basic-program` k ≥ 1). Mas a 1.ª solução sem dica é ruim. No `three-bedroom` k=1 `cold`, a 1.ª teve objetivo 2,39 e a final 8,09. No `large-house` com k = 0, 1 e 3, a 1.ª ficou entre 0,7 e 1,6, e a final entre 5,8 e 7,5.
4. **A dica completa e viável reduz o tempo para provar o ótimo, mas não sempre.** Em dt:
   - `basic-program`: k=1 de 5,89 para 4,82; k=2 de 3,06 para 0,86; k=3 de 0,12 para 0,07; k=0 de 25,7 para 23,5;
   - `three-bedroom`: k=1 de 7,17 para 7,05; k=2 de 3,87 para 1,83; k=3 de 1,54 para 0,43;
   - `small-lot`: de 6,38 para 5,62 (k=1);
   - o `small-lot` k=0 (13,46 para 13,94) e o `three-bedroom` k=0 (26,7 para 27,4) não melhoraram.

   Quando as duas variantes provam o ótimo, chegam ao mesmo objetivo. Às vezes a planta é diferente, mas de mesmo objetivo (empate): "mudaram" vai a 0 com dica e a 2 sem dica no `one-bedroom` k=2 e no `three-bedroom` k=2.
5. **A dica de prefixo (incompleta) ou inviável pode atrasar.** No `large-house`, onde a dica completa era inviável:
   - a 1.ª solução passou de 0,62 s (`cold`) para 5,2 a 5,6 s (k=1), e de 1,0 para 2,4–2,5 s (k=2);
   - o tempo determinístico subiu de 7 a 10 % em k = 2 e 3.

   Com o limite de 20 dt, o objetivo final melhorou (k=0: de 6,38 para 6,68; k=1: de 5,61 para 6,27). Mas a variação entre rodadas do `cold` k=1 vai de 5,61 a 6,41, e a melhora fica dentro dela.
6. **O limite curto de 2 dt não é respeitado.** Com `interleave_search=True`, a fase 1 terminou sempre por volta de 8 dt (7,7 a 8,6), ou 7 a 11 s de relógio nos pedidos médios e grandes com k ≤ 1. Com o limite de 20 dt, terminou entre 20 e 27 dt. Sem `interleave_search`, o limite 2 informou 13,4 dt. Com limite 0,5, a fase 1 durou cerca de 3 s nos dois modos.
7. **O limite curto custa qualidade nos pedidos grandes.** No `large-house` k=0, o objetivo da fase 2 caiu de 6,38 para 5,16, e a nota de 0,907 para 0,814. No `basic-program` (5,763) e no `three-bedroom` (7,04 contra 7,13), a perda foi quase nula. Quando as travas levam ao ótimo provado, o limite não importa: a busca termina antes dele.
8. **Reprodutibilidade:**
   - os casos que provam o ótimo deram a mesma planta e o mesmo dt nas 4 rodadas;
   - os que param no limite curto também foram idênticos nas 4 rodadas (dt 8,07 e 8,09 exatos);
   - os que param no limite de 20 dt não foram: o `large-house` k=1 `cold` deu 3 plantas distintas em 4 rodadas, com notas de 0,849 a 0,888 e dt de 25,3 a 27,1.
9. **As tentativas de formato custam caro em toda re-solução.** O `small-lot` (encostado) prova de novo, a cada re-solução, que o retângulo cheio com teto 1,5 é inviável. Isso custa 3 a 7 dt (4,5 a 8 s) com k ≤ 1, antes de achar a solução no formato 1.
10. **Montar o modelo é barato:** de 3 a 80 ms por fase. Completar a dica (o solve com o prefixo fixado) levou de 9 a 80 ms.
11. **A perturbação quase sempre é absorvida.** Com k ≥ 1, o cômodo perturbado manteve a área nos pedidos `one-bedroom`, `small-lot` e `three-bedroom` (e no `basic-program` com k ≥ 2). No `small-lot`, nem com k=0 ele cresceu. No `large-house`, ele cresceu demais nas soluções paradas pelo limite: cozinha com alvo de 15 m² chegou a 21,8 m² de retângulo no `cold` k=1.

### HIPÓTESES (interpretação)

- **H1.** Com `interleave_search`, o CP-SAT só confere o limite entre lotes de tarefas, e cada tarefa de subsolver completo roda cerca de 1 dt. Com 8 workers, o 1.º lote já soma ≈ 8 dt, e esse passa a ser o piso efetivo do limite. O log com limite 2 mostra 2 tarefas por subsolver, e a soma de dtime bate com os 8,07 dt informados. Com limite 0,5, o tamanho do lote parece encolher (3,7 dt). Não li o código para confirmar a regra exata.
- **H2.** O "deterministic_time" informado com vários workers parece agregar o dt de todos eles, e não o de um só. Isso explica os 13,4 dt sem `interleave_search` com limite 2. Comparar dt entre modos de busca diferentes exige cuidado.
- **H3.** A dica de prefixo atrasa a 1.ª solução porque tem valores para as variáveis estruturais mas não para as auxiliares do objetivo. O solver gasta a busca curta de reparo (10 conflitos por worker, segundo a nota de pesquisa) e depois cai na busca normal com a polaridade desviada. Quando a dica é completa e viável, ela entra direto como solução (o objetivo da 1.ª solução é igual ao da dica), coerente com a seção 2 de [re-solucao-interativa-cpsat.md](re-solucao-interativa-cpsat.md).
- **H4.** A latência da re-solução depende mais de **quantos cômodos ficam livres** do que de quantos estão travados. Com 5 ou mais cômodos livres num pedido de 9 ou mais cômodos (`large-house` k ≤ 1, pedidos médios com k = 0), a re-solução vira uma geração do zero e para no limite.
- **H5.** O piso de 0,7 × alvo transforma uma mudança de alvo em restrição dura. Por isso a planta anterior pode ficar inviável (o `large-house`) e a dica completa se perde. Uma perturbação "para baixo" (alvo −25 %) provavelmente manteria a dica viável. Não testei.

## 7. Limitações

- Uma máquina só (notebook, sem controle de turbo ou temperatura), e parte das execuções com concorrência (marcada nas tabelas). Os números em dt são mais confiáveis que os de relógio. Com a máquina livre, a razão foi de 0,8 a 1,2 s de relógio por dt nas execuções longas. Nas curtas, chegou a cerca de 1,8 s por dt, por causa do custo fixo.
- Uma semente, um tipo de perturbação (+25 % no 4.º maior alvo) e uma regra de escolha de travas (os maiores primeiro). Travar cômodos pequenos ou espalhados pode dar outro resultado.
- Poucas repetições: 4 rodadas em 5 casos, e só uma re-solução por pedido × k × variante nos demais.
- A dica completa vem da planta-base **polida** (fase 2), e não da solução da fase 1. É o que um app teria (a planta mostrada), mas não é a única opção.
- O instante da 1.ª solução é medido a partir da tentativa de formato que deu certo. No `small-lot`, falta somar a prova de inviabilidade do formato 0, que foi de 0,1 a 8 s.
- O callback de solução e as chamadas de `tasklist` (fora da região cronometrada) podem ter um efeito pequeno no relógio, que não medi.
- Não testei os parâmetros `fix_variables_to_their_hinted_value`, `repair_hint`, `interleave_batch_size` nem um limite de relógio (`max_time_in_seconds`). Também não testei uma fase 2 com dica.

## 8. Sugestões para o design do M2

1. **Travar com igualdades em x/y/w/h, e não pelos índices da malha.** Funcionou em 100 % dos casos e deixa o solver livre para reorganizar a malha. O custo de montagem é desprezível (ms).
2. **Tratar "travar e re-resolver" como tarefa assíncrona com resultados parciais, e não como chamada síncrona.** A latência medida varia de 0,03 s a cerca de 27 s conforme o pedido e o número de cômodos livres.
   - *Interativo de verdade* (≤ 1 s): só `one-bedroom`, `small-lot` com k=3 e `basic-program` com k=3.
   - *Aceitável com indicador de progresso* (1 a 10 s): a maioria dos casos com k ≥ 2.
   - *Lento* (≥ 20 s): k ≤ 1 nos pedidos grandes.
   - A interface deve mostrar a planta anterior de imediato (a dica completa já dá isso em ≤ 0,3 s), atualizar quando chegar solução melhor e permitir cancelar.
3. **Usar a dica completa só quando ela for viável.** Antes de re-resolver, checar a viabilidade com o solve do prefixo fixado (cerca de 20 ms; ou com `fix_variables_to_their_hinted_value`, a testar). Se for viável, passar a dica completa. Se não for, passar **nenhuma**, em vez do prefixo: no `large-house`, o prefixo atrasou a 1.ª solução de 0,6 para 5,5 s sem ganho fora da variação entre rodadas. A planta anterior inviável também é uma informação para o usuário ("a mudança tornou a planta anterior inválida porque…").
4. **Não contar com um `max_deterministic_time` pequeno para baixar a latência.** Com `interleave_search`, o piso medido foi ≈ 8 dt (7 a 11 s). Há dois caminhos possíveis:
   - (a) aceitar o piso e mostrar o progresso;
   - (b) testar `interleave_batch_size` ou outro arranjo de workers para baixar o piso.

   Em qualquer caso, medir de novo a reprodutibilidade (decisão do M1.1: mesma semente, mesma planta). Um limite de relógio quebraria a reprodutibilidade, que hoje vale nos casos com ótimo provado e nos parados no limite curto.
5. **Começar a re-solução pelo formato que deu certo antes (proposta, a validar).** Re-provar a inviabilidade do formato 0 custou de 4,5 a 8 s por re-solução no `small-lot`. Pular essa prova só é seguro se a mudança apenas acrescenta restrições (travas). Uma mudança de alvo mexe no piso e no teto de área e pode tornar viável um formato que antes não era. Alternativa: guardar a prova de inviabilidade por "formato × conjunto de restrições".
6. **Avisar o usuário quando a mudança for absorvida.** Com travas, a perturbação muitas vezes não muda nada: o cômodo perturbado manteve a área em 3 dos 5 pedidos. A interface deve mostrar alvo × obtido do cômodo alterado e explicar o que o impediu (travas, terreno). Isso liga com a explicação de inviabilidade da nota de pesquisa.
7. **Escolher o limite padrão da re-solução por tamanho.** Com k ≥ 2, os pedidos de até 12 cômodos provaram o ótimo em ≤ 9 dt, e manter o limite de 20 dt não custa nada. Com k ≤ 1 em pedidos de 9 ou mais cômodos, a re-solução não converge em 20 dt e varia de rodada para rodada. Nesses casos, oferecer "melhorar mais" (re-solver a partir da melhor planta, com dica completa) é mais honesto do que esperar.
8. **Próximos experimentos, se o M2 for por esse caminho:**
   - perturbação para baixo (−25 %) e perturbação de relação;
   - travas em cômodos pequenos;
   - `interleave_batch_size` e `fix_variables_to_their_hinted_value`;
   - re-solução encadeada (várias edições seguidas, cada uma com dica da anterior);
   - medir de novo com a máquina livre, sem concorrência.
