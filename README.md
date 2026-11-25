# PyGridPlan

Gerador inteligente de **plantas baixas residenciais**, que roda **offline**. Você informa o terreno, os cômodos e as preferências (em campos ou em texto livre), e o sistema constrói a planta 2D **ao vivo**, etapa por etapa, propondo alternativas que você aprova ou ajusta. O resultado sai em **DXF**, editável no AutoCAD.

## Destaques planejados

- Entrada mista: campos essenciais, campos opcionais e texto livre, interpretado por um LLM local.
- Grafo de relações entre ambientes (social, íntimo, serviço).
- Vários métodos de geração comparáveis lado a lado: árvore de subdivisão, crescimento em grade, otimização por restrições e recozimento simulado.
- Interface escura e minimalista, com a planta ocupando a tela e um console que mostra cada comando do motor.
- Exportação DXF com layers organizados.

## Estado atual

✅ **M0 (fundação)** · ✅ **D1 (dados de referência)** · ✅ **M1 (gerador CP-SAT): gera K plantas válidas e diferentes, com nota por critério, em JSON, DXF e HTML (103 testes).** ✅ **M1.1 (forma e implantação):** casa no recuo frontal e centralizada, encosto automático em lote pequeno com marcação "sem janela", muro, 4 cores (interna seca/molhada, externa construída/verde), vazio fechado proibido. **Calibração do M1.1:** o gerador passou a usar uma malha de linhas de parede resolvida em duas fases (topologia, depois medidas); a casa sai em **bloco cheio** nos 5 pedidos de referência e a **circulação tem função** (quartos e banheiro abrem para ela). Relatório: [docs/plans/m1-1-calibration.md](docs/plans/m1-1-calibration.md). **Regras da conferência visual (S06):** retângulo antes de recorte, espelho não é alternativa, janelas em níveis com fonte (obrigatória/preferida, com rigor escolhido no pedido) e zoneamento como critério de nota; norma é referência, não teto (design, seções 22 e 23). ✅ **D2 (mobiliário e folgas):** pesquisa concluída, promoção para `data/` no M1.2. ✅ **Pesquisa técnica do M2 (S07):** servidor local, console ao vivo, desenho da planta no navegador, re-solução interativa com CP-SAT (com experimento medido de travar cômodos) e árvore de estados; relatório em [docs/research/Arquitetura interativa do M2.md](<docs/research/Arquitetura interativa do M2.md>), base do design do M2. ✅ **Reprodutibilidade do gerador (S07):** o mesmo pedido, com a mesma semente, dá as mesmas plantas, mesmo quando a busca para no orçamento (lotes do CP-SAT, sem LNS; design, seção 22.5). ✅ **Fundamentação teórica do gerador (S07):** cobertura exata numa malha de linhas de parede, CP-SAT, duas fases, nota, diversidade, reprodutibilidade, limitações e comparação com subdivisão, crescimento em grade e recozimento simulado, com referências; em [docs/theory/cpsat-generator.md](docs/theory/cpsat-generator.md). ✅ **Pesquisa técnica do M5 (S07):** LLM local para interpretar o pedido em português (motores, modelos pequenos, saída estruturada por JSON Schema, parser de regras, avaliação com gabarito e hardware desta máquina); proposta: regras primeiro, `llama-server` com esquema delta e modelo de ~2B a 4B a decidir num spike de medição; relatório em [docs/research/LLM local para interpretar pedidos.md](<docs/research/LLM local para interpretar pedidos.md>). ✅ **D3 (aberturas: portas e janelas), pesquisa (S07):** larguras de porta por cômodo e por tipo, varredura e geometria derivada (NBR 9050:2020 e NBR 15930-2), frações de janela nacionais × municipais, peitoril, divisa (Código Civil, 1,50 m e 0,75 m), duto, poço e claraboia, gás (NBR 13103), porta de serviço e regras de posição; base do M4, sem promoção para `data/`; relatório em [docs/research/Portas e janelas residenciais.md](<docs/research/Portas e janelas residenciais.md>). 🟡 **M1.2 (dimensionamento pelo mobiliário), design aprovado (S08), implementação a seguir:** perfis de mínimo com fonte (`nbr`, `mcmv`, `ergonomico`, `folgado`), verificação "cabe?" (escada de medidas pré-calculada como restrição no CP-SAT + checagem exata com o arranjo dos móveis), móveis no relatório e no DXF, personalização no pedido; dados da D2 promovidos em `data/furniture.yaml`. Design: [docs/design/m1-2-furniture-sizing.md](docs/design/m1-2-furniture-sizing.md) · plano: [docs/plans/m1-2-furniture-sizing.md](docs/plans/m1-2-furniture-sizing.md) (a ajustar às respostas da DEC-0139). ✅ **Ajustes do gerador (S08):** `ortools` fixo em 9.15.6755; as formas provadas inviáveis não se repetem entre as alternativas (lote pequeno: 54 → 40 s, plantas idênticas); com menos de K plantas, o aviso e a CLI dizem o motivo (orçamento esgotado, não há mais plantas diferentes ou limite de tentativas); tipo de fonte `L-est`; bancada em [docs/research/notes/Bancada do gerador/](<docs/research/notes/Bancada do gerador/raw-data/README.md>) (DEC-0149 a DEC-0151). 🟡 **M1.3 (forma livre, blocos destacados e edícula), design aprovado (S09), sem código:** uma planta por família de forma (largo, comprido, L, U), janela antes de variedade, implantação no lote antes da planta, áreas com medida (piscina, quadra, horta), edícula e oficina com programa próprio, nota que não pune a forma; seis etapas, E0 a E5. Design: [docs/design/m1-3-free-form-and-blocks.md](docs/design/m1-3-free-form-and-blocks.md) (DEC-0152 a DEC-0160). Próximo: calibração 2 do M1.1 a partir da conferência da S08 (banheiro com parede externa, entrada pela sala, corredor sem sobra, espelho entre cômodos iguais; DEC-0146 a DEC-0148), que fecha o M1.1; depois, os spikes do M1.3 (E0), a implementação do M1.2 e as etapas E1 e E2 do M1.3; em paralelo, só documentos, a trilha D4 e o design do M2. Design: [docs/design/mvp.md](docs/design/mvp.md) · Planos: [docs/plans/](docs/plans/) · Pesquisa: [docs/research/](docs/research/) · Teoria: [docs/theory/](docs/theory/) · Dados: [data/README.md](data/README.md).
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
│   ├── furniture.yaml       mobiliário mínimo e folgas por perfil, com fonte por valor ✅ M1.2 (dados)
│   └── costs/               consumo SINAPI, preços datados, classes de acabamento
├── tests/                   testes (rápidos e `slow`, que rodam o solver) ✅
│   └── fixtures/            DADOS — casos de teste e os 5 pedidos da bancada (`requests/`)
├── out/                     DADOS — gerados (fora do git)
│
└── docs/
    ├── design/              design do MVP + mockups         ✅
    ├── plans/               um plano por marco              ✅
    ├── research/            pesquisas (relatório + notas; dados brutos em `notes/<título>/raw-data/`) ✅ D1, D2, D3 (aberturas), M2 e M5 (técnicas), bancada do gerador (S08)
    └── theory/              fundamentação teórica          ✅ M1 (gerador CP-SAT)
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
#   opções: --k 4  --seed 0  --batches 6   (~2 min para 4 plantas de 8 cômodos; mesmo pedido e semente = mesmas plantas)

# validar e exportar uma planta descrita em JSON para DXF
python -m pygridplan export-dxf tests/fixtures/plans/basic-house.json out/basic-house.dxf
```

O formato do pedido está em `tests/fixtures/requests/basic-program.json`; os tipos de cômodo, em `data/room_types.yaml`.

## Aviso

Ferramenta de estudo e projeto preliminar. Uma construção real exige profissionais habilitados e aprovação municipal.
