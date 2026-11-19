# PyGridPlan

Gerador inteligente de **plantas baixas residenciais**, que roda **offline**. Você informa o terreno, os cômodos e as preferências (em campos ou em texto livre), e o sistema constrói a planta 2D **ao vivo**, etapa por etapa, propondo alternativas que você aprova ou ajusta. O resultado sai em **DXF**, editável no AutoCAD.

## Destaques planejados

- Entrada mista: campos essenciais, campos opcionais e texto livre, interpretado por um LLM local.
- Grafo de relações entre ambientes (social, íntimo, serviço).
- Vários métodos de geração comparáveis lado a lado: árvore de subdivisão, crescimento em grade, otimização por restrições e recozimento simulado.
- Interface escura e minimalista, com a planta ocupando a tela e um console que mostra cada comando do motor.
- Exportação DXF com layers organizados.

## Estado atual

✅ **M0 (fundação)** · ✅ **D1 (dados de referência)** · ✅ **M1 (gerador CP-SAT): gera K plantas válidas e diferentes, com nota por critério, em JSON, DXF e HTML (103 testes).** ✅ **M1.1 (forma e implantação):** casa no recuo frontal e centralizada, encosto automático em lote pequeno com marcação "sem janela", muro, 4 cores (interna seca/molhada, externa construída/verde), vazio fechado proibido. **Calibração do M1.1:** o gerador passou a usar uma malha de linhas de parede resolvida em duas fases (topologia, depois medidas); a casa sai em **bloco cheio** nos 5 pedidos de referência e a **circulação tem função** (quartos e banheiro abrem para ela). Relatório: [docs/plans/m1-1-calibration.md](docs/plans/m1-1-calibration.md). Próximo: M1.2 (mobiliário). Design: [docs/design/mvp.md](docs/design/mvp.md) · Planos: [docs/plans/](docs/plans/) · Pesquisa: [docs/research/](docs/research/) · Dados: [data/README.md](data/README.md).
Histórico completo de decisões: [DECISOES.md](DECISOES.md).

## Stack prevista

Python (motor) · HTML/CSS/TypeScript (interface web local) · ezdxf (DXF). As demais bibliotecas serão escolhidas com testes.

## Estrutura do projeto

✅ existe · 🔜 nasce no marco indicado (pastas são criadas com o primeiro arquivo)

```
PyGridPlan/
├── README.md · CLAUDE.md · DECISOES.md · .gitignore      ✅ governança
├── pyproject.toml                                          ✅ M0  dependências e config. de testes
│
├── src/pygridplan/          SOFTWARE — motor Python         ✅ M0
│   ├── model/               entidades, paredes, catálogo   ✅
│   ├── validation/          validade geométrica e recomendações ✅
│   ├── export/              DXF                            ✅
│   ├── generators/          CP-SAT ✅ · subdivisão 🔜 M7
│   ├── pipeline/            etapas e árvore de estados     🔜 M2
│   ├── scoring/             critérios e diversidade        ✅ M1
│   ├── interpret/           regras + LLM local             🔜 M5
│   └── server/              comandos e eventos             🔜 M2
├── web/                     SOFTWARE — interface TypeScript 🔜 M2
│
├── data/                    DADOS — referência curada       ✅ D1
│   ├── sources.yaml         registro de fontes (fonte única das citações)
│   ├── site_defaults.yaml   muro, distância de janela à divisa, permeabilidade de referência
│   ├── room_types.yaml      catálogo de cômodos com fonte por valor
│   └── costs/               consumo SINAPI, preços datados, classes de acabamento
├── tests/                   testes (rápidos e `slow`, que rodam o solver) ✅
│   └── fixtures/            DADOS — casos de teste e os 5 pedidos da bancada (`requests/`)
├── out/                     DADOS — gerados (fora do git)
│
└── docs/
    ├── design/              design do MVP + mockups         ✅
    ├── plans/               um plano por marco              ✅
    ├── research/            pesquisas (relatório + notas)   ✅ D1
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
pytest -m "not slow"    # suíte rápida (~15 s): tudo menos o solver
pytest                  # suíte completa: inclui os testes que rodam o solver (vários minutos)
```

Checagem de tipos (opcional): `pyright`, instalado à parte com `npm install -g pyright`.

**Uso:**

```bash
# gerar 4 plantas alternativas a partir de um pedido (terreno + cômodos + relações)
python -m pygridplan generate tests/fixtures/requests/basic-program.json out/m1
#   → out/m1/alt-N.json, alt-N.dxf e report.html (comparação lado a lado)
#   opções: --k 4  --seed 0  --time-limit 4   (leva ~1 min para 4 plantas de 8 cômodos)

# validar e exportar uma planta descrita em JSON para DXF
python -m pygridplan export-dxf tests/fixtures/plans/basic-house.json out/basic-house.dxf
```

O formato do pedido está em `tests/fixtures/requests/basic-program.json`; os tipos de cômodo, em `data/room_types.yaml`.

## Aviso

Ferramenta de estudo e projeto preliminar. Uma construção real exige profissionais habilitados e aprovação municipal.
