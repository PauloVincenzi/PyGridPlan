# PyGridPlan

Gerador inteligente de **plantas baixas residenciais**, que roda **offline**. Você informa o terreno, os cômodos e as preferências (em campos ou em texto livre), e o sistema constrói a planta 2D **ao vivo**, etapa por etapa, propondo alternativas que você aprova ou ajusta. O resultado sai em **DXF**, editável no AutoCAD.

## Destaques planejados

- Entrada mista: campos essenciais, campos opcionais e texto livre, interpretado por um LLM local.
- Grafo de relações entre ambientes (social, íntimo, serviço).
- Vários métodos de geração comparáveis lado a lado: árvore de subdivisão, crescimento em grade, otimização por restrições e recozimento simulado.
- Interface escura e minimalista, com a planta ocupando a tela e um console que mostra cada comando do motor.
- Exportação DXF com layers organizados.

## Estado atual

🧭 **Design aprovado; plano do M0 escrito.** Ainda não há código. Design: [docs/design/mvp.md](docs/design/mvp.md) · Plano: [docs/plans/m0-foundation.md](docs/plans/m0-foundation.md).
Histórico completo de decisões: [DECISOES.md](DECISOES.md).

## Stack prevista

Python (motor) · HTML/CSS/TypeScript (interface web local) · ezdxf (DXF). As demais bibliotecas serão escolhidas com testes.

## Estrutura do projeto

✅ existe · 🔜 nasce no marco indicado (pastas são criadas com o primeiro arquivo)

```
PyGridPlan/
├── README.md · CLAUDE.md · DECISOES.md · .gitignore      ✅ governança
├── pyproject.toml                                          🔜 M0  dependências e config. de testes
│
├── src/pygridplan/          SOFTWARE — motor Python         🔜 M0
│   ├── model/               entidades, paredes, catálogo
│   ├── validation/          validade geométrica e recomendações
│   ├── export/              DXF
│   ├── generators/          CP-SAT, subdivisão             🔜 M1/M7
│   ├── pipeline/            etapas e árvore de estados     🔜 M1
│   ├── scoring/             critérios e diversidade        🔜 M1
│   ├── interpret/           regras + LLM local             🔜 M5
│   └── server/              comandos e eventos             🔜 M2
├── web/                     SOFTWARE — interface TypeScript 🔜 M2
│
├── data/                    DADOS — referência curada       🔜 M0
├── tests/                   testes                          🔜 M0
│   └── fixtures/            DADOS — casos de teste
├── out/                     DADOS — gerados (fora do git)
│
└── docs/
    ├── design/              design do MVP + mockups         ✅
    ├── plans/               um plano por marco              ✅
    └── theory/              fundamentação teórica          🔜
```

### Os dados do projeto

| Tipo | Onde | Origem | Vai para o git? |
|---|---|---|---|
| Referência | `data/` | literatura, normas, manuais, convenção de mercado; cada valor com fonte, versão e data | sim |
| Casos de teste | `tests/fixtures/` | escritos por nós; também servem de entrada para benchmarks | sim |
| Gerados | `out/` | produzidos pelo app (DXF, projetos); recriáveis a partir de entrada + semente | não |
| Resultados de análise | 🔜 decidir quando houver benchmark | resumo de comparações entre geradores | só o resumo |
| Do usuário | 🔜 decidir no M2 | projetos salvos e histórico de escolhas (aprendizado de pesos) | não |

## Requisitos, instalação e execução

**Requisitos:** Python ≥ 3.13.

**Instalação** (uma vez, na raiz do projeto):

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -e ".[dev]"
```

O `pip install -e` instala as dependências e o próprio pacote de uma vez, em modo editável: mudanças no código valem sem reinstalar. O código fica em `src/`, então os testes sempre rodam contra o pacote instalado.

**Testes:**

```bash
pytest
```

## Aviso

Ferramenta de estudo e projeto preliminar. Uma construção real exige profissionais habilitados e aprovação municipal.
