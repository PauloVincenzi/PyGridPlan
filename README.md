# PyGridPlan

Gerador inteligente de **plantas baixas residenciais**, que roda **offline**. Você informa o terreno, os cômodos e as preferências (em campos ou em texto livre), e o sistema constrói a planta 2D **ao vivo**, etapa por etapa, propondo alternativas que você aprova ou ajusta. O resultado sai em **DXF**, editável no AutoCAD.

## Destaques planejados

- Entrada mista: campos essenciais, campos opcionais e texto livre, interpretado por um LLM local.
- Grafo de relações entre ambientes (social, íntimo, serviço).
- Vários métodos de geração comparáveis lado a lado: árvore de subdivisão, crescimento em grade, otimização por restrições e recozimento simulado.
- Interface escura e minimalista, com a planta ocupando a tela e um console que mostra cada comando do motor.
- Exportação DXF com layers organizados.

## Estado atual

🧭 **Fase de concepção.** Escopo e arquitetura em definição. Ainda não há código.
Histórico completo de decisões: [DECISOES.md](DECISOES.md).

## Stack prevista

Python (motor) · HTML/CSS/TypeScript (interface web local) · ezdxf (DXF). As demais bibliotecas serão escolhidas com testes.

## Estrutura

```
CLAUDE.md          regras do agente de IA (inclui as skills usadas)
DECISOES.md        registro cronológico append-only de decisões
README.md          este arquivo
docs/design/       documento de design do MVP (mvp.md) e mockups aprovados
```

Estrutura-alvo, criada conforme o código nasce: `src/pygridplan/` (motor), `web/` (interface), `data/` (dados de referência), `tests/`, `docs/plans/`, `docs/theory/`. Detalhes na seção 17 de [docs/design/mvp.md](docs/design/mvp.md).

## Requisitos, instalação e execução

A definir quando houver código.

## Aviso

Ferramenta de estudo e projeto preliminar. Uma construção real exige profissionais habilitados e aprovação municipal.
