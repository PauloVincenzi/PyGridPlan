# Dados brutos da bancada do gerador (S08)

Criado em: 2026-11-24 · Sessão S08 · Origem: scratchpad da conversa `fix/generator-adjustments`, copiado sem alteração de conteúdo. Três arquivos trocaram de nome: `hi.py` → `high_priority.py`, `hi.jsonl` → `high-priority-probe.jsonl` e `run2.sh` → `run.sh` (que ainda chama `hi.py`).

Compara o gerador antes (`old`, commit `8c6dd64`) e depois (`new`) da DEC-0126: 5 pedidos × 4 alternativas, semente 0, OR-Tools 9.15.6755, i5-1335U, Windows 11. Conclusões na DEC-0149 do [DECISOES.md](../../../../../DECISOES.md).

- `bench.py`: gera as alternativas e grava uma linha JSON por pedido (tempo de relógio e de CPU, nota, área, hash das plantas, cada resolução do CP-SAT).
- `high_priority.py`: roda o `bench.py` em prioridade alta e sem economia de energia (EcoQoS).
- `run.sh`: ordem das execuções, com antes e depois trocados a cada par. Os caminhos apontam para o scratchpad.
- `bench.jsonl`: **a bancada que vale**. `load.log`: carga da CPU, processos Python e memória livre antes de cada execução.
- `bench-throttled.jsonl`: 1ª tentativa, **descartada para tempo**: sem `high_priority.py`, o Windows rebaixou o processo lançado em segundo plano (os 3 quartos levaram 605 e 696 s, contra 117 e 120 s). As plantas são as mesmas.
- `high-priority-probe.jsonl`: o teste que sustenta essa causa (2 pedidos, só o código novo). Prioridade e EcoQoS mudaram juntos, então ele não separa uma da outra.

**Limites:** outros programas do responsável seguiram abertos (carga de 3 a 45 % antes das execuções, memória livre de 472 a 914 MB de 8 GB). O lote pequeno tem 3 execuções por lado; os outros pedidos, 1. A variação de −2 a +3 % neles é ruído: o código faz exatamente as mesmas resoluções.
