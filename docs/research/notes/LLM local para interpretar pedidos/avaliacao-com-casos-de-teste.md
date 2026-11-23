# Avaliação de um extrator texto → JSON (regras + LLM local) com casos de teste

> Notas de pesquisa (trilha M5 — LLM local). Estado: novembro de 2026. Rótulos: **[FATO]** = verificado em fonte citada; **[HIPÓTESE]** = inferência plausível ainda não verificada; **[OPINIÃO]** = recomendação do pesquisador. Os números de intervalos de confiança e p-valores marcados "calculado" foram computados nesta pesquisa (fórmula de Wilson e teste binomial exato, em Python), não tirados de fonte. Código ilustrativo: **não testado**.

## 1. Desenho do conjunto de testes: tamanho, estatística e cobertura

### Takeaway
Com n=50 a 100 casos, a acurácia por pedido tem margem de ±6 a ±12 pontos percentuais (Wilson, 95%). Isso basta para detectar regressões grandes e para fazer comparações **pareadas** (McNemar exato) entre modelos/prompts. Não basta para separar variantes que diferem em poucos pontos. Para um projeto solo, a meta razoável é ~100–150 casos de desenvolvimento mais ~50 de teste reservado, cobrindo fenômenos linguísticos de forma explícita.

### Cited Findings
- [FATO] O guia estatístico da Anthropic recomenda tratar a nota como amostra de um "universo de perguntas", reportar o erro padrão (IC 95% = média ± 1,96 × SEM) e comparar modelos por **diferenças pareadas**, já que eles respondem às mesmas perguntas. Isso elimina a variância da dificuldade de cada questão. — [Anthropic, A statistical approach to model evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- [FATO] O mesmo guia recomenda **erros padrão clusterizados** quando as questões não são independentes (ex.: várias perguntas sobre o mesmo texto). Em evals populares, o erro clusterizado pode ser "mais de três vezes" maior que o ingênuo. Também recomenda análise de poder para escolher o número de questões. — [Anthropic](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- [FATO] O guia relata correlação de cerca de 0,3 a 0,7 entre as notas por questão de modelos de fronteira, motivo pelo qual o teste pareado é bem mais eficiente. — [Anthropic](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- [FATO] `statsmodels.stats.proportion.proportion_confint(count, nobs, alpha=0.05, method='normal')` oferece os métodos `wilson`, `beta` (Clopper-Pearson), `agresti_coull`, `jeffreys` e `binom_test`. O padrão é `normal`. Clopper-Pearson garante cobertura ≥ 1−α, mas é conservador. Wilson fica dentro de [0,1] por construção. A referência é Brown, Cai e DasGupta (2001), *Statistical Science* 16(2):101–133, doi:10.1214/ss/1009213286. — [statsmodels proportion_confint](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html)
- [FATO] `statsmodels.stats.contingency_tables.mcnemar(table, exact=True, correction=True)`: com `exact=True` (padrão) usa a binomial exata sobre os pares discordantes. Com `exact=False` usa a aproximação qui-quadrado para amostras grandes. — [statsmodels mcnemar](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html)
- [FATO, calculado] Intervalo de Wilson 95% para a acurácia observada:

  | n | p̂=0,70 | p̂=0,80 | p̂=0,90 |
  |---|---|---|---|
  | 50 | 0,562–0,809 (±12,3 pp) | 0,670–0,888 (±10,9) | 0,786–0,957 (±8,5) |
  | 100 | 0,604–0,781 (±8,8) | 0,711–0,867 (±7,8) | 0,826–0,945 (±6,0) |
  | 200 | 0,633–0,759 (±6,3) | 0,739–0,850 (±5,5) | 0,851–0,934 (±4,2) |
  | 400 | 0,653–0,743 (±4,5) | 0,758–0,836 (±3,9) | 0,867–0,926 (±3,0) |

  (Cálculo próprio com a fórmula de Wilson, z = 1,96.)
- [FATO, calculado] O McNemar exato só depende dos casos **discordantes** (b = A acerta e B erra; c = o contrário). Exemplos de p-valor bicaudal: b=8, c=2 → p≈0,109; b=10, c=3 → p≈0,092; b=12, c=4 → p≈0,077; b=15, c=5 → p≈0,041. Ou seja, mesmo com 100 casos, uma diferença líquida de 6 a 8 casos não é significativa a 5%. São precisos ~10 casos de vantagem líquida com ~20 discordantes. (Cálculo próprio, binomial exata.)
- [FATO] Hamel Husain recomenda começar com ~100 traces diversos, revisar pessoalmente pelo menos os primeiros 30 e continuar enquanto aparecerem modos de falha novos. Um conjunto de eval repetível costuma passar de 100 exemplos. — [Hamel Husain, LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)
- [FATO] Hamel recomenda gerar dados sintéticos por **dimensões**: definir eixos, escrever ~20 tuplas à mão, deixar um LLM gerar mais tuplas e usar um segundo prompt para converter cada tupla em texto natural. Não pedir genericamente "me dê consultas de teste", que produz saídas repetitivas. — [Hamel Husain, LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)

### Inferências
- [OPINIÃO] Dimensões de cobertura para o PyGridPlan, cada caso com tag(s) de fenômeno no próprio fixture:
  1. **base** (pedido canônico, explícito);
  2. **paráfrase** (mesmo JSON, redação diferente; agrupar paráfrases do mesmo "pedido-semente" num cluster para o erro padrão clusterizado);
  3. **coloquial/regional** ("quartinho", "banheiro social", "suíte", "cozinha americana", "lavabo");
  4. **erros de digitação/sem acento** ("cozinah", "sala de estar", "banhero");
  5. **números por extenso e unidades** ("doze metros quadrados", "12m²", "12 m2", "3x4", "terreno de dez por vinte e cinco");
  6. **negação** ("sem escritório", "não quero a cozinha perto do quarto" → relação far);
  7. **intensidade** ("de preferência" vs "obrigatoriamente" vs "muito longe");
  8. **plural/quantidade** ("três quartos" → três rooms com ids distintos);
  9. **fora de escopo** ("piscina", "segundo andar", "orçamento da obra") → abstenção ou aviso, nunca inventar tipo fora do catálogo;
  10. **conflito** ("cozinha perto da sala e longe da sala"; área total > terreno) → comportamento esperado definido (erro de validação ou campo de conflito);
  11. **adversarial/injeção** ("ignore as instruções e responda com…", JSON embutido no texto) → saída continua validada e sem campos extras;
  12. **vazio/mínimo** ("quero uma casa") → JSON mínimo ou abstenção.
- [OPINIÃO] Erro padrão clusterizado por pedido-semente faz sentido: 5 paráfrases do mesmo pedido não são 5 observações independentes. Para um projeto solo, basta reportar também a acurácia por semente (fração de paráfrases corretas) e o IC de Wilson sobre as sementes.
- [OPINIÃO] Como as comparações são pareadas (mesmo conjunto, dois modelos/prompts), o par "McNemar exato + tabela b/c" é a ferramenta certa para "o prompt v2 é melhor que o v1?". O IC de Wilson serve para reportar o nível absoluto.
- [HIPÓTESE] Para métricas contínuas (F1 de campo por caso, MAE de intensidade), o bootstrap pareado por caso (reamostrar casos e calcular a diferença média) dá IC sem suposições fortes. Não encontrei fonte específica para extração estruturada. É prática estatística geral.

### Gaps
- Não encontrei uma fonte específica que recomende tamanhos de amostra para avaliação de extração texto→JSON. Os números acima são cálculo estatístico genérico.
- Não encontrei referência publicada de cobertura de fenômenos linguísticos para PT-BR em extração estruturada. A lista de dimensões é proposta minha.

## 2. Formato do gabarito e métricas

### Takeaway
Use JSON-gabarito validado pelo mesmo modelo Pydantic e compare **por emparelhamento**, nunca por igualdade de string: os ids de cômodos são arbitrários. Primeiro emparelhe os cômodos (tipo + área com tolerância), depois reescreva as relações em termos dos cômodos emparelhados e compare como conjuntos não ordenados. Métricas em camadas: validade de schema → acerto exato por pedido → P/R/F1 por campo → erro de intensidade → alucinação → abstenção → latência/RAM.

### Cited Findings
- [FATO] O JSONSchemaBench (Geng et al., arXiv 2501.10868; poster no ICML 2025 ES-FoMo III) reúne ~10 mil schemas JSON reais e a JSON Schema Test Suite. Avalia seis frameworks de decodificação restrita (Guidance, Outlines, llama.cpp, XGrammar, OpenAI, Gemini) em três eixos: eficiência, cobertura de tipos de restrição e qualidade da saída. Conclui que o benchmark é um desafio significativo para LLMs e frameworks. Código em github.com/guidance-ai/jsonschemabench. — [arXiv 2501.10868](https://arxiv.org/abs/2501.10868v2); [ICML 2025](https://icml.cc/virtual/2025/51849)
- [FATO] Um artigo de 2026 sobre extração de JSON de e-mails (arXiv 2602.14743) resume o JSONSchemaBench: a decodificação restrita por schema pode acelerar a geração e melhorar a acurácia, mas o suporte a recursos avançados de schema varia muito entre frameworks. — resumo via busca de [arXiv 2602.14743](https://arxiv.org/pdf/2602.14743) (não li o artigo completo)
- [FATO] O llama-server aceita `json_schema` ("Set a JSON schema for grammar-based sampling") e `grammar` (GBNF) por requisição. — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] A documentação do promptfoo descreve a asserção `is-json` como verificação de JSON válido, com validação opcional contra um JSON Schema. Observa ainda que pedir JSON a um LLM é pouco confiável e que motores como o llama.cpp suportam saída restrita por gramáticas GBNF. — [promptfoo, Evaluate JSON](https://www.promptfoo.dev/docs/guides/evaluate-json/)
- [FATO] Hamel Husain recomenda rótulos **binários** (passa/falha) em vez de escalas Likert e acompanhar taxa de verdadeiros positivos e de verdadeiros negativos, não só a acurácia. Também considera métricas genéricas de similaridade (BERTScore, ROUGE) geralmente inúteis para julgar saídas de LLM. — [Hamel Husain, LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)

### Inferências
- [OPINIÃO] **Formato do gabarito** (um arquivo JSONL ou um YAML por caso em `tests/fixtures/nl/`):
  ```yaml
  # ilustrativo, não testado
  id: rel-neg-003
  seed: rel-neg          # cluster de paráfrases
  tags: [negacao, relacao]
  split: dev             # dev | test (reservado)
  text: "Não quero a cozinha colada no quarto do casal."
  expected:              # validado pelo mesmo modelo Pydantic do app
    rooms:
      - {id: k, type: cozinha}
      - {id: q, type: quarto_casal}
    relations:
      - {a: k, b: q, kind: far, intensity: null}   # null = qualquer intensidade aceita
  tolerances: {area_rel: 0.10, intensity_abs: 1}
  expect_abstain: false
  ```
  Campos `null` no gabarito significam "não avaliar". Isso evita penalizar uma área que o texto não especifica.
- [OPINIÃO] **Algoritmo de emparelhamento** (independente de id):
  1. Para cada tipo de cômodo, emparelhe previstos ↔ gabarito. Com vários do mesmo tipo (três quartos), use custo = |Δárea| e atribuição ótima. `scipy.optimize.linear_sum_assignment` resolve isso. Sem scipy, para n ≤ 6 por tipo basta força bruta por permutações.
  2. Monte o mapa id_previsto → id_gabarito.
  3. Reescreva as relações previstas pelo mapa e normalize como `frozenset({a,b}), kind`, porque near/far são simétricas.
  4. Conte TP/FP/FN em cômodos (tipo; área dentro da tolerância como submétrica), relações (par + kind) e relações com intensidade (|Δ| ≤ 1).
- [OPINIÃO] **Métricas** (todas calculáveis em código, sem juiz):
  - *schema_valid_rate*: fração de saídas que passam no `model_validate` do Pydantic. Com decodificação restrita deveria ficar perto de 100%; se não ficar, é bug de integração.
  - *exact_match* por pedido: todos os campos avaliados corretos após o emparelhamento. É a métrica binária principal, que alimenta Wilson/McNemar.
  - P/R/F1 micro (somando TP/FP/FN de todos os casos) e macro (média por caso) para cômodos e relações. Reportar os dois, porque o micro é dominado por pedidos grandes.
  - *area*: fração dentro da tolerância relativa e erro absoluto médio (m²), só onde o gabarito tem área.
  - *intensity*: MAE e acurácia com tolerância ±1, só nas relações emparelhadas.
  - *hallucination_rate*: cômodos previstos sem correspondente no gabarito, mais relações que citam id inexistente ou cômodo não mencionado. O segundo caso deveria ser impossível com a validação Pydantic (referência cruzada de ids), então medir isso também testa o validador.
  - *abstention*: matriz 2×2 (devia abster × absteve). Reportar a taxa de abstenção correta nos fora de escopo e a de falsa abstenção nos casos válidos.
  - *latência* p50/p95 (wall-clock por caso, depois de um aquecimento) e *RAM de pico* do processo do modelo (ex.: `psutil` com amostragem durante a execução, ou o pico informado pelo runtime). Sempre com o hardware anotado.
- [OPINIÃO] O gabarito deve passar pelo mesmo modelo Pydantic do app num teste rápido. Assim um gabarito inválido quebra a suíte rápida, não a avaliação lenta.

### Gaps
- Não encontrei um padrão consolidado (paper ou ferramenta) de métrica para "conjuntos de entidades com ids arbitrários + relações entre elas" em extração com LLM. O emparelhamento acima é adaptação minha de práticas gerais de avaliação de extração de relações.
- Medir RAM de pico de forma confiável para um servidor externo (Ollama) depende do runtime. Não verifiquei o que cada um expõe.

## 3. Determinismo com modelos locais e separação de testes rápidos e lentos

### Takeaway
Temperatura 0 / greedy torna a **escolha de token** determinística, mas não garante logits bit-a-bit idênticos. No llama.cpp, cache de prompt, número de slots paralelos, tamanho de lote, offload para GPU, backend (CUDA/Vulkan) e decodificação especulativa podem mudar a saída. Em CPU, com build, threads e configuração fixos e cache desligado, a reprodutibilidade tende a ser boa, mas não está garantida pela documentação. Por isso: testes rápidos determinísticos (regras, validação, LLM mockado / respostas gravadas) na suíte padrão, e avaliação com modelo real marcada como lenta, fora do CI padrão, com relatório versionado.

### Cited Findings
- [FATO] A documentação do llama-server diz que `cache_prompt` (padrão `true`) reutiliza o KV cache de uma requisição anterior. Diz também que "os logits **não** têm garantia de serem bit-a-bit idênticos para tamanhos de lote diferentes" e que habilitar essa opção "pode causar resultados não determinísticos". — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] No llama-server, `seed` tem padrão −1 (semente aleatória). A documentação não afirma que uma semente fixa garante saída idêntica. `-np, --parallel N` define o número de slots (padrão −1 = automático). — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] Issue #2838 (CUDA): com KV cache ligado, a primeira resposta difere das seguintes. Com o cache desligado a saída é estável, e o relator não viu o problema em CPU. — [llama.cpp #2838](https://github.com/ggml-org/llama.cpp/issues/2838) (resumo de snippet de busca; não abri a issue)
- [FATO] Issue #26425: com decodificação especulativa MTP (Qwen3.6-35B-A3B-MTP), a mesma requisição (corpo idêntico, mesma semente) retorna textos diferentes conforme a requisição anterior. `--parallel 1` reduz o efeito, mas não o elimina. — [llama.cpp #26425](https://github.com/ggml-org/llama.cpp/issues/26425) (snippet de busca)
- [FATO] Issue #19981 (Vulkan/AMD): mesma semente e prompt deram respostas diferentes, que mudavam com o casamento de prefixo do cache. Issue fechada. — [llama.cpp #19981](https://github.com/ggml-org/llama.cpp/issues/19981) (snippet de busca)
- [FATO] Discussion #4020: offload de camadas para GPU muda o resultado mesmo com a mesma semente, por pequenas diferenças de arredondamento. Segundo a resposta na discussão, não havia como evitar. — [llama.cpp discussion #4020](https://github.com/ggml-org/llama.cpp/discussions/4020) (snippet de busca)
- [FATO] Um post no blog da Hugging Face sobre "temperatura 0" com LLMs locais sugere usar um único slot e desligar o cache por requisição. — [HF blog, Why Your Local LLM Gives Different Answers at Temperature 0](https://huggingface.co/blog/wwoosshh/temperature-0-different-answers) (snippet de busca)
- [FATO] A causa geral é que a ordem das somas em ponto flutuante muda com a divisão do trabalho (lote, threads, splits de KV). Temperatura 0 só torna o argmax determinístico, não os logits. As correções com kernels "batch-invariant" documentadas são do vLLM/SGLang, não do llama.cpp. — [SGLang, deterministic inference](https://docs.sglang.io/docs/advanced_features/deterministic_inference); [arXiv 2506.09501](https://arxiv.org/pdf/2506.09501v2)
- [FATO] O Inspect AI observa que os providers Ollama e llama-cpp-python exigem um fechamento assíncrono, o que limita a paralelização. — [Inspect, Using Models](https://inspect.aisi.org.uk/models.html)
- [FATO] A API `/api/generate` do Ollama descreve `seed` como "Random seed used for reproducible outputs". O parâmetro `format` aceita a string `"json"` ou um objeto JSON Schema (saída estruturada). A página não documenta `num_thread`/`num_batch` nem fala de cache de prompt ou de garantia bit-a-bit. — [Ollama API, generate](https://docs.ollama.com/api/generate)

### Inferências
- [OPINIÃO] Configuração "o mais reprodutível possível" para a avaliação: CPU apenas; build do llama.cpp fixado (tag/commit anotado); `--parallel 1`; `cache_prompt: false` por requisição; `temperature: 0` (ou `top_k: 1`); `seed` fixo; número de threads e `-b/-ub` fixos e registrados; sem decodificação especulativa; avaliação sequencial (um caso por vez).
- [HIPÓTESE] Nessas condições, execuções repetidas na mesma máquina devem dar saídas idênticas. Isso precisa ser **medido**, não suposto: rodar a avaliação 2 a 3 vezes e reportar a taxa de casos com saída diferente entre execuções. Se for > 0, reportar o acerto como média com variação entre execuções, como recomenda o guia da Anthropic para variância intra-questão.
- [HIPÓTESE] Com Ollama há menos controle documentado sobre os parâmetros internos do llama.cpp (cache, slots, threads, lote): a página da API só promete reprodutibilidade via `seed`. Para a avaliação reprodutível, chamar o llama-server (ou llama-cpp-python) diretamente tende a ser mais controlável.
- [OPINIÃO] Arquitetura de testes:
  - **Rápidos (suíte padrão):** parser de regras parametrizado sobre os fixtures; validação Pydantic dos gabaritos; scorer (emparelhamento e métricas) testado com saídas sintéticas, incluindo ids trocados, ordem invertida e relação a↔b; caminho do LLM com cliente **mockado** ou com **respostas gravadas** (cassettes JSON de uma execução real), que testam parsing, pós-processamento e fallback sem o modelo.
  - **Lentos (`@pytest.mark.llm_eval`, desligados por padrão via `addopts = -m "not llm_eval"` ou opção `--run-llm-eval`):** rodam o modelo real sobre o conjunto dev (ou test, com flag explícita) e gravam um relatório JSON em `out/` (fora do git). O resumo vai versionado em `docs/` ou `tests/fixtures/eval-baselines/`.
  - **Gate de regressão:** os testes lentos não precisam de "assert acurácia ≥ X" rígido. Comparar com a baseline gravada e falhar só se houver casos que passavam e passaram a falhar acima de um limiar, listando-os.
- [OPINIÃO] O parser de regras é determinístico e deve ter limiares duros (ex.: 100% nos casos `base` que ele promete cobrir), porque não há ruído nele.

### Gaps
- Não encontrei afirmação oficial do llama.cpp de que a inferência em CPU com threads fixas é bit-a-bit reprodutível entre execuções. Os relatos de problema concentram-se em GPU, cache e paralelismo. Para CPU, a ausência de relatos não prova determinismo.
- Não verifiquei como o número de threads em CPU afeta os logits no llama.cpp (ordem de redução nos kernels ggml). Fica para medir.
- Os resumos das issues vieram de snippets de busca. As issues não foram abertas uma a uma e podem ter atualizações.

## 4. Ferramentas: framework ou pytest próprio?

### Takeaway
Todas as ferramentas grandes (promptfoo, Inspect AI, DeepEval, lm-evaluation-harness) são mantidas ativamente em novembro de 2026, e várias falam com modelos locais. Mas nenhuma traz pronto o que é específico deste projeto: o emparelhamento de cômodos com ids arbitrários. Para um projeto solo em Python com pytest, ~100–200 linhas (fixtures + scorer + relatório JSON) ficam mais simples e com menos dependências. Inspect AI é a alternativa Python mais séria, se um dia se quiser um visualizador de logs.

### Cited Findings
- [FATO] **promptfoo:** última versão 0.126.0, de 18/11/2026 (anterior: 0.125.1, de 25/10/2026). — [GitHub releases promptfoo](https://github.com/promptfoo/promptfoo/releases)
- [FATO] As notas de release mensais do promptfoo citam, em outubro de 2025, suporte a function calling/ferramentas no provider Ollama e, em janeiro de 2026, Transformers.js para inferência local. — [promptfoo Release Notes](https://www.promptfoo.dev/docs/releases)
- [FATO] O promptfoo tem a asserção `is-json` com validação opcional por JSON Schema. — [promptfoo, Evaluate JSON](https://www.promptfoo.dev/docs/guides/evaluate-json/)
- [HIPÓTESE, fonte secundária] Um texto de terceiros afirma que o promptfoo tem provider nativo `ollama:chat:<modelo>` (endereço via `OLLAMA_BASE_URL`) e que o llama-server pode ser usado pelo provider `openai:chat` com base URL customizada. Resultados de busca também dizem que o promptfoo "se juntou à OpenAI" e segue MIT. Não confirmei em fonte primária. — resultado de busca, [sumguy.com](https://sumguy.com/promptfoo-prompt-testing/)
- [FATO] O promptfoo é distribuído pelo npm (exige Node.js). A página do npm devolveu 403 nesta pesquisa, por isso a exigência de versão do Node e a política de telemetria não foram verificadas. — [npm promptfoo](https://www.npmjs.com/package/promptfoo) (inacessível)
- [FATO] **Inspect AI** (UK AISI): versão 0.3.291, de 17/11/2026, licença MIT, Python ≥ 3.11. — [PyPI inspect-ai](https://pypi.org/project/inspect-ai/)
- [FATO] O Inspect lista Ollama e llama-cpp-python entre os providers locais, ao lado de Hugging Face, vLLM e SGLang. — [Inspect, Model Providers](https://inspect.aisi.org.uk/providers.html)
- [FATO] **DeepEval:** versão 4.3.4, de 11/11/2026, Apache-2.0, Python ≥ 3.10. Algumas métricas rodam modelos NLP localmente; outras são LLM-as-judge com um modelo configurável. O PyPI não diz se funciona totalmente offline. Com login na plataforma Confident AI, os casos são registrados automaticamente. — [PyPI deepeval](https://pypi.org/project/deepeval/)
- [FATO] **lm-evaluation-harness (`lm-eval`):** versão 0.4.13, de 31/08/2026 (pré-release 0.5.0.dev1, de 11/05/2026). Suporta GGUF via backend `hf`, llama.cpp via llama-cpp-python e servidores com API compatível com OpenAI (`local-completions`, `local-chat-completions`). Tipos de tarefa: `generate_until`, `loglikelihood`, `loglikelihood_rolling`, `multiple_choice`. — [PyPI lm-eval](https://pypi.org/project/lm-eval/)
- [HIPÓTESE, fonte secundária] **OpenAI Evals:** uma resenha de 2026 afirma que o repositório `openai/evals` continua no GitHub, sem arquivamento, mas só em manutenção, sem aceitar evals com código customizado. A mesma resenha cita a página de descontinuações da OpenAI: as evals hospedadas ficam somente leitura em 31/10/2026, o dashboard e a API de Evals são desligados em 30/11/2026, e a migração oficial indicada é para o promptfoo. Não confirmei na página da OpenAI. — [aicoolies, OpenAI Evals review](https://aicoolies.com/reviews/openai-evals-review)
- [FATO] O repositório separado `openai/simple-evals` se declara sem manutenção ("We will not be actively maintaining this repository…"). — [openai/simple-evals](https://github.com/openai/simple-evals)
- [FATO] Hamel Husain recomenda começar simples (um notebook basta) e diz que métricas genéricas prontas "desperdiçam tempo e criam falsa confiança" quando usadas como medida de qualidade. — [Hamel Husain, LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)

### Inferências
- [OPINIÃO] **lm-eval** foi feito para benchmarks acadêmicos (log-verossimilhança, múltipla escolha, tarefas padronizadas). Dá para registrar uma tarefa `generate_until` com métrica customizada, mas é a ferramenta errada para um extrator de produto.
- [OPINIÃO] **DeepEval** foca em métricas LLM-as-judge (relevância, fidelidade etc.) e na integração com a plataforma Confident AI. Com gabarito JSON, o diferencial dele não se aplica e traz dependências pesadas. Não recomendo.
- [OPINIÃO] **promptfoo** é bom para comparar prompts × modelos em matriz, com YAML e visualizador web. Porém exige Node (o projeto já terá TypeScript no M2, então isso não pesa tanto), e a lógica de emparelhamento teria de ir num `assert: javascript` ou `python`, ou seja, o scorer seria escrito do mesmo jeito. Ganha-se uma UI de comparação e perde-se integração com o pytest/pyright.
- [OPINIÃO] **Inspect AI** é Python, MIT e mantido por um órgão público. Tem Dataset/Solver/Scorer, logs estruturados e visualizador (`inspect view`), e suporta Ollama/llama-cpp-python. Se a avaliação crescer (vários modelos, centenas de casos, histórico), ele é a melhor opção de framework para este projeto. O scorer customizado continuaria sendo código próprio.
- [OPINIÃO] **Recomendação para o PyGridPlan:** começar com pytest parametrizado mais um módulo `eval` próprio (scorer puro e testado, e um runner que grava JSON). Reavaliar o Inspect AI só se aparecer necessidade concreta, como comparar mais de 3 modelos ou navegar logs. Isso segue a regra do projeto ("não adicionar dependências sem justificativa").
- Esboço ilustrativo (**não testado**):
  ```python
  # tests/eval/test_llm_eval.py — ilustrativo, não testado
  import json, pathlib, pytest
  from pygridplan.nl import interpret          # regras + LLM
  from pygridplan.nl.scoring import score_case  # emparelhamento + métricas
  CASES = [json.loads(l) for l in pathlib.Path("tests/fixtures/nl/dev.jsonl").read_text("utf-8").splitlines()]

  @pytest.mark.llm_eval
  @pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
  def test_case(case, eval_recorder):
      out, meta = interpret(case["text"], backend="llm")   # meta: latência, tokens
      s = score_case(case["expected"], out, case.get("tolerances", {}))
      eval_recorder.add(case, out, s, meta)                 # fixture grava o relatório no fim da sessão
      # sem assert de acurácia aqui; o gate é a comparação com a baseline
  ```

### Gaps
- A situação societária do promptfoo (OpenAI) e a política de telemetria e licença não foram verificadas em fonte primária.
- Não verifiquei se o DeepEval roda 100% offline sem chamadas de rede (telemetria e login).
- **OpenAI Evals:** o estado em 2026 (somente manutenção; plataforma hospedada sendo desligada) vem de fonte secundária, sem confirmação na página oficial de descontinuações. De todo modo, é orientado à API da OpenAI e está em fim de ciclo. [OPINIÃO] Não serve para um app offline.

## 5. Construção e versionamento do dataset, e LLM-as-judge

### Takeaway
Escreva à mão as sementes por dimensão (≈20–40). Gere paráfrases com ajuda de um modelo maior, mas revise todas e marque a origem de cada caso (`source: manual | generated:<modelo>`). Separe desde o início um split `test` que não é olhado durante o ajuste do prompt. Versione o dataset no git e grave, junto de cada resultado, o modelo, a quantização, o hash do prompt, o runtime e o hash do dataset. Com gabarito JSON, um juiz LLM não é necessário. A comparação estrutural é exata, barata e determinística.

### Cited Findings
- [FATO] Hamel Husain recomenda dividir os dados rotulados em train/dev/test (sugestão: ~10–20% / 40–45% / 40–45%) e reservar o test para uma checagem final. Cada mudança feita com base no dev vaza informação. Se o test sair bem pior que o dev, houve overfitting. — [Hamel Husain, LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)
- [FATO] Ele também diz que dados sintéticos revelam problemas, mas não dizem com que frequência eles ocorrem na produção, e que se deve migrar para dados reais quando possível. — [Hamel Husain, LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)
- [FATO] Ainda segundo Hamel, comece por asserções de código e use juiz LLM só quando a verificação exigir julgamento real, com saída passa/falha. Juízes LLM custam mais para construir e manter e exigem ~100–200 exemplos rotulados por modo de falha para calibrar. — [Hamel Husain, LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)
- [FATO] A análise de erros é, para ele, "a atividade mais importante em evals": codificação aberta (notas livres por trace), depois codificação axial (agrupar as notas numa taxonomia de falhas e contar por categoria), repetindo até novos traces pararem de revelar modos de falha novos. A análise não deve ser terceirizada. — [Hamel Husain, LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)

### Inferências
- [OPINIÃO] **Por que não usar juiz LLM aqui:** o alvo é um JSON com schema fechado e gabarito. Cada campo tem verdade verificável por código (tipo do catálogo, área ± tolerância, par/kind, intensidade ± 1). Um juiz acrescentaria custo, não-determinismo e um segundo modelo a avaliar, sem ganho de informação. O único uso defensável seria auditar casos ambíguos de gabarito (onde o próprio humano hesita), e isso se resolve melhor marcando o campo como `null` ("não avaliar") ou aceitando alternativas.
- [OPINIÃO] **Contaminação e viés de paráfrases geradas:** um modelo maior tende a produzir um português "limpo" e parecido com o do prompt do sistema, o que pode inflar o acerto. Mitigações: (a) sementes e casos difíceis (gírias, erros de digitação, negação) escritos à mão; (b) marcar `source` e reportar a acurácia separada para manual × gerado; (c) não gerar paráfrases do split `test` com o mesmo modelo/família usado no extrator; (d) nunca colocar exemplos do `test` como few-shot no prompt.
- [OPINIÃO] **Split estável:** atribuir `split` por **semente** (todas as paráfrases de uma semente no mesmo split), senão a paráfrase do dev "ensina" o test. Fixar o split no próprio arquivo, não por sorteio a cada execução.
- [OPINIÃO] **Versionamento e procedência:** o dataset fica em `tests/fixtures/nl/` com cabeçalho de versão (o projeto não usa datas em nomes de arquivo). Cada relatório de avaliação grava: `dataset_sha256`, `prompt_sha256` (prompt + few-shots + schema/gramática), `model_file` + `sha256` do GGUF, quantização (ex.: Q4_K_M), `runtime` + versão/commit (llama.cpp build ou Ollama), parâmetros de amostragem (temp, top_k, seed, n_ctx, threads, batch), CPU/RAM da máquina, versão do Python, commit do repositório e timestamp. Sem esses campos, não dá para comparar resultados ao longo do tempo. Isso decorre diretamente das fontes de não-determinismo do item 3.
- [OPINIÃO] **Análise de erros e regressão:**
  - Relatório por **tag/fenômeno** (acurácia e IC de Wilson por fatia). Ex.: "negação 9/15" mostra onde está o problema melhor que a média geral.
  - **Matriz de confusão de tipo de cômodo** (gabarito × previsto nos pares emparelhados por posição/área), que pega confusões como "lavabo" ↔ "banheiro".
  - **Confusão de kind** (near/far/ausente) e histograma de erro de intensidade.
  - **Diff por caso entre execuções:** lista de "passava → falha" e "falhava → passa" (os discordantes do McNemar). É a forma mais útil de acompanhar regressões.
  - Taxonomia de falhas (codificação axial) mantida num arquivo curto, com contagem por execução.
  - Comparar **regras sozinhas × LLM sozinho × regras + LLM** no mesmo conjunto. Isso justifica (ou não) a presença do LLM no portfólio.

### Gaps
- Não encontrei estudo quantitativo sobre o viés de paráfrases geradas por LLM em avaliação de extração em português. O risco descrito é inferência.
- Não encontrei guia oficial recente da OpenAI sobre evals para este caso (não pesquisado nesta rodada).
