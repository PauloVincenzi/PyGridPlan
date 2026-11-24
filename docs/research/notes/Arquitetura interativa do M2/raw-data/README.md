# Dados brutos do experimento de re-solução do M2

Criado em: 2026-11-24 · Sessão S08 · Origem: scratchpad da conversa da pesquisa do M2 (S07), copiado sem alteração.

Experimento descrito no relatório [Arquitetura interativa do M2](../../../Arquitetura%20interativa%20do%20M2.md), seção do experimento: travar de 1 a 3 cômodos e re-resolver nos 5 pedidos da bancada.

- `relock_experiment.py`: script do experimento; `make_exp_module.py` gera a cópia instrumentada do gerador (`cpsat_exp_v2.py`, com diff em `cpsat_exp_v2.diff`).
- `results.jsonl`: 135 linhas (115 execuções + 20 checagens de dica); `baseline.json`: plantas-base.
- `diag_limit.*`, `diag_dt.py`, `diag_basic_k0_dt2.log`: diagnóstico do limite de tempo determinístico.
- `tables*.md`: tabelas geradas por `summarize.py` e `compact.py`.
- `contaminated/`: rodada descartada (processos alheios na máquina); `smoke/`: rodada de teste.

Atenção: os números foram medidos **antes** da DEC-0123 (reprodutibilidade). Os caminhos dentro dos scripts apontam para o scratchpad original e precisam ser ajustados para rodar de novo.
