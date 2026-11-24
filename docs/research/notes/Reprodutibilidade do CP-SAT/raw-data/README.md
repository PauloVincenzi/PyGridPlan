# Dados brutos da investigação de reprodutibilidade do CP-SAT

Criado em: 2026-11-24 · Sessão S08 · Origem: scratchpad da conversa `fix/cpsat-reproducibility` (S07), copiado sem alteração.

Não há relatório de pesquisa próprio: as conclusões estão na DEC-0123 do [DECISOES.md](../../../../../DECISOES.md), na seção 22.5 do [design](../../../../design/mvp.md) e na seção de reprodutibilidade de [docs/theory/cpsat-generator.md](../../../../theory/cpsat-generator.md).

- `bench.py`, `compare.py`, `costs.ps1`: bancada, comparação do vetor de solução entre processos e medição de tempo.
- `bNN-*`: bancada antes da correção; `cNN-*`: configurações A/B/C; `dNN-*`: correção em processos simultâneos.
- `e01-*`, `e02-*`, `e03-*`: isolamento da causa (R0 base, R1–R4 trocas entre threads, R5 sem LNS, R6 pool 1, R8 sequencial, R9 sem LNS e sem cláusulas binárias, R10 sem LNS com parada por tempo determinístico); `-pN` = processo N de 3 simultâneos; `.err` = log do solver.
- `fNN-*`: lotes alternativos (4 e 5).

Medido no OR-Tools 9.15.6755. Os caminhos dentro dos scripts apontam para o scratchpad original.
