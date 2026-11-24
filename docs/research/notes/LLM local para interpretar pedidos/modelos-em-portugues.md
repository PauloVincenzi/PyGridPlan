# Modelos abertos pequenos (0,5B–8B) para PT-BR e saída JSON / function calling (estado em nov/2026)

> Notas de pesquisa da trilha "LLM local para interpretar pedidos" (PyGridPlan, M5).
> Coleta: 2026-11-22. Legenda: **[FATO]** confirmado na fonte citada · **[HIPÓTESE]** inferência a confirmar · **[OPINIÃO]** julgamento do pesquisador.
> Complemento em 2026-11-23: cards do Qwen3.5-2B e do Gemma 4 E2B, GGUF do Qwen3.5-2B, licença e GGUF do Tucano 2, Sabiá-7B e PoETa v2.
> Orçamento de busca limitado (~25 chamadas no total). Vários itens vêm do conhecimento prévio do pesquisador e **não foram reconferidos nesta sessão**; eles aparecem como [HIPÓTESE] ou em "Gaps", nunca como [FATO].
> Restrição de hardware usada como filtro: i5-1335U, 8 GB de RAM compartilhada com CP-SAT e navegador, só CPU.

## 1. Famílias atuais com tamanhos pequenos e treino multilíngue/português

### Takeaway
Em nov/2026 as famílias pequenas mais fortes e com licença permissiva são **Qwen3.5** (0,8B/2B/4B/9B, Apache-2.0, fev/2026) e **Gemma 4** (E2B/E4B, Apache-2.0, 2026). Atrás delas, com o português listado de forma explícita: SmolLM3-3B, Granite-4.0-Micro (3B), Ministral 3 3B e Phi-4-mini (3,8B). Para 8 GB compartilhados, o alvo realista é a faixa de 2–4B em Q4/Q5. Qwen3.5-4B é o candidato principal.

### Cited Findings
**Qwen3.5 (Alibaba)**
- [FATO] Qwen3.5-4B: "4B" parâmetros na visão geral (o box Safetensors mostra "5B params", provavelmente somando o encoder de visão), licença **apache-2.0**, contexto de 262.144 tokens nativos (extensível a ~1M), "201 languages and dialects". A citação do card traz fevereiro de 2026 — [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)
- [FATO] O card compara o 4B com o Qwen3.5-9B, o que confirma que o 9B existe — [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)
- [FATO, fonte secundária] Família Qwen3.5 com densos de 0,8B, 2B, 4B, 9B e 27B, mais MoE de 35B, 122B e 397B — [Codersera](https://codersera.com/blog/gemma-4-vs-qwen-3-5-comparison-2026/)
- [FATO] Qwen3.5-2B: Apache-2.0, 2B, contexto de 262.144 nativos, **sem raciocínio por padrão** ("operates in non-thinking mode by default"), ao contrário do 4B. A tabela do card traz também o 0,8B. MMMLU sem raciocínio: 2B = 56,9 e 0,8B = 34,1. Com raciocínio: 63,1 e 44,3 — [Qwen/Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B)
- [FATO] Gemma 4 E2B-it: 2,3B efetivos (5,1B com embeddings), Apache 2.0, 128K de contexto, MMMLU 67,4%, MMLU Pro 60,0%, Tau2 24,5%. O card não traz IFEval nem BFCL — [google/gemma-4-E2B-it](https://huggingface.co/google/gemma-4-E2B-it)
- [FATO, fonte secundária] Qwen3.8-27B, denso, lançado em agosto/2026 sob Apache-2.0. Fica fora da faixa de tamanho — [PromptQuorum](https://www.promptquorum.com/local-llms/best-local-llms-2026); [Slash Digital](https://slash-digital.io/en/insights/open-weight-models-2026/). Não encontrei Qwen3.8 pequeno.

**Gemma 4 (Google)**
- [FATO] gemma-4-E4B-it: "4.5B effective (8B with embeddings)", **Apache 2.0**, contexto de 128K nos modelos pequenos, suporte multilíngue em "over 140 languages" ("35+ languages" prontos para uso), function calling nativo. A família tem cinco modelos: E2B, E4B, 12B Unified, 26B A4B (MoE) e 31B Dense. O relatório técnico (arXiv 2607.02770) é de 2 de julho — [google/gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it)
- [FATO, fonte secundária] O lançamento foi em abril/2026, com quatro tamanhos. O 12B Unified veio em 3 de junho — [Wikipedia Gemma](https://en.wikipedia.org/wiki/Gemma_(language_model)); [Victor Grosser](https://victorgrosser.nl/blog/open-weight-models-april-october-2026-recap/). As datas variam entre as fontes.

**Outros com o português declarado no card**
- [FATO] SmolLM3-3B (Hugging Face): 3B, Apache-2.0, treinado com 64k de contexto (até 128k com YaRN). O português é uma das 6 línguas nativas (EN, FR, ES, DE, IT, PT). Tem tool calling (`xml_tools` / `python_tools`) e modo de raciocínio alternável — [HuggingFaceTB/SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B)
- [FATO] Granite-4.0-Micro (IBM): 3B, Apache-2.0, lançado em 2 de outubro de 2025, contexto de 128K. O português está entre as 12 línguas suportadas. Tool calling usa o schema de função da OpenAI, com saída em `<tool_call>`. A família 4.0 tem ainda H-Micro (3B, híbrido Mamba2), H-Tiny (MoE de 7B total, 1B ativo) e H-Small (MoE de 32B) — [ibm-granite/granite-4.0-micro](https://huggingface.co/ibm-granite/granite-4.0-micro)
- [FATO] Ministral 3 3B (Mistral, versão 2512 = dez/2025): Apache-2.0, LM de 3,4B mais encoder de visão de 0,4B, contexto de 256k. O português está na lista de línguas do card Base. A família tem 9 modelos open-weight — [Mistral docs](https://docs.mistral.ai/models/model-cards/ministral-3-3b-25-12); [HF Base card](https://huggingface.co/mistralai/Ministral-3-3B-Base-2512); [arXiv 2601.08584](https://arxiv.org/abs/2601.08584v1)
- [FATO] Phi-4-mini-instruct (Microsoft): 3,8B, **MIT**, lançado em fevereiro de 2025, contexto de 128K. O português está entre as línguas listadas. Function calling usa JSON entre tokens `<|tool|>`. O red team relatou que o modelo às vezes alucina nomes de função — [microsoft/Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)

**Famílias anteriores (não reconferidas nesta sessão)**
- [HIPÓTESE, conhecimento prévio] Qwen3 (abr/2025: 0,6B/1,7B/4B/8B, Apache-2.0, 119 línguas, Qwen3-4B-Instruct-2507 sem raciocínio). Llama 3.2 1B/3B (set/2024, Llama 3.2 Community License, português entre 8 línguas oficiais). Gemma 3 1B/4B (mar/2025, Gemma Terms of Use). Gemma 3n E2B/E4B (jun/2025). EXAONE 4.0 1.2B (2025, licença não comercial). Todas foram superadas pelas gerações de 2026 nos mesmos tamanhos — ver Gaps.

### Shortlist (síntese para o caso PyGridPlan)
| Modelo | Tamanho | Licença | Português | JSON / tools (evidência) | GGUF Q4_K_M | Lançamento |
|---|---|---|---|---|---|---|
| **Qwen3.5-4B** | 4B | Apache-2.0 | 201 línguas (PT não citado nominalmente) | BFCL-V4 50,3; IFEval 89,8 (card) | 2,74 GB (unsloth) | fev/2026 |
| Qwen3.5-2B | 2B | Apache-2.0 | idem | BFCL-V4 43,6 (com raciocínio); IFEval 61,2 sem / 78,6 com raciocínio (card) | 1,28 GB (unsloth) | fev/2026 |
| Qwen3.5-0.8B | 0,8B | Apache-2.0 [HIP: família] | idem | BFCL-V4 25,3; IFEval 52,1 sem raciocínio (tabela do card do 2B) | não conferido | fev/2026 |
| **Gemma 4 E2B-it** | 2,3B efetivos / 5,1B com embeddings | Apache-2.0 | 140+ línguas | function calling nativo; Tau2 24,5; MMMLU 67,4; sem BFCL/IFEval no card | 3,11 GB (unsloth) | 2026 |
| Gemma 4 E4B-it | 4,5B efetivos / 8B com embeddings | Apache-2.0 | 140+ línguas | Tau2 42,2 (card) | 4,98 GB (pesado para 8 GB) | 2026 |
| SmolLM3-3B | 3B | Apache-2.0 | PT nativo | BFCL 92,3 / IFEval 76,7 sem raciocínio (card; versão do BFCL não indicada) | não conferido | 2025 [HIP: jul/2025] |
| Granite-4.0-Micro | 3B | Apache-2.0 | PT listado | BFCL v3 59,98; IFEval 82,31 (card) | não conferido | 02/10/2025 |
| Ministral 3 3B | 3,4B + 0,4B de visão | Apache-2.0 | PT listado | sem número conferido | não conferido | dez/2025 |
| Phi-4-mini-instruct | 3,8B | MIT | PT listado | sem IFEval/BFCL no card | não conferido | fev/2025 |
| Tucano2-qwen-3.7B-Instruct | 3,7B | Apache-2.0 (via card de conversão e card do 1.5B) | nativo PT-BR | IFEval-PT adaptado; sem avaliação de JSON | sem GGUF oficial encontrado (há MLX 4-bit da comunidade) | mar/2026 |
| Qwen3.5-9B (stretch) | 9B | Apache-2.0 | 201 línguas | BFCL-V4 66,1; IFEval 91,5 | não conferido | fev/2026 |

### Inferences
- [OPINIÃO] Ordem de teste sugerida: **Qwen3.5-4B (sem raciocínio) → Gemma 4 E2B → Qwen3.5-2B → SmolLM3-3B / Granite-4.0-Micro**. O Tucano 2 3.7B entra como controle "nativo PT". O 9B só vale se o 4B falhar no conjunto de teste e a RAM aguentar.
- [HIPÓTESE] Os pesos de 2026 (Qwen3.5, Gemma 4) são multimodais. Para o PyGridPlan basta o texto: dá para omitir o arquivo `mmproj` e economizar ~0,7–1 GB.

### Gaps
- Não abri o card próprio do Qwen3.5-0.8B. Os números dele vêm da tabela do card do 2B, e a licença é inferida pela família.
- Não reconferi o Llama 3.2, o Gemma 3/3n, o Qwen3 e o EXAONE 4.0 nesta sessão (datas e licenças acima vêm de memória).
- Não encontrei lançamento pequeno de 2026 do Llama, do Phi (pós-Phi-4-mini), do SmolLM ou do Granite (pós-4.0) nas buscas feitas. Isso não prova que não existam.

## 2. Modelos específicos para português (Tucano, Gervásio, Bode, Cabrita, GlórIA, Sabiá, Amadeus, CabraLlama…)

### Takeaway
O único projeto PT-BR **recente e pequeno** com instruct é o **Tucano 2** (Polygl0t, mar/2026, 0,5B–3,7B, com variantes Instruct e Think, continuação de pré-treino do Qwen3). Ele publica dados de SFT com tool use e saída estruturada, mas **não reporta avaliação de JSON nem de function calling**. O Gervásio (PORTULAN) é de 7–8B, foi feito sobre Llama 2/3.1, e a ênfase é PT-PT.

### Cited Findings
- [FATO] Tucano 2, post publicado em 5 de março de 2026: família de "0.5B to 3.7B" (o TL;DR diz 0,5B–3,5B, uma inconsistência do próprio texto). O Tucano2-0.6-Base foi treinado do zero (~408B tokens). Os maiores fazem **continuação de pré-treino a partir de bases Qwen3**, com troca para um tokenizador PT de 49K e mais 50–100B tokens em português. Variantes Base/Instruct/Think: SFT mais APO, e o Think raciocina em português — [HF blog Tucano 2](https://huggingface.co/blog/Polygl0t/tucano2)
- [FATO] O SFT (GigaVerbo-v2 SFT, ~4M exemplos, 12 tipos de tarefa) **inclui tool use e saída estruturada**, mas não há avaliação de function calling ou JSON. Os benchmarks adaptados são IFEval, GSM8K, RULER e HumanEval. "Agentic capabilities" fica como trabalho futuro — [HF blog Tucano 2](https://huggingface.co/blog/Polygl0t/tucano2)
- [FATO, autodeclarado] Tucano2-qwen-3.7-Base com 59,21 no agregado do próprio autor, contra 57,86 do Qwen3-4B-Base e 57,97 do Qwen2.5-7B. O Instruct teria o melhor "Knowledge & Reasoning" entre 3–4B (acima do Qwen3-4B e do SmolLM3-3B), sem número no texto. Não há comparação com Gemma nem com Qwen3.5 — [HF blog Tucano 2](https://huggingface.co/blog/Polygl0t/tucano2)
- [FATO] Paper: "fully open suite… 0.5-3.7 billion parameters", tamanhos 0,5B/1,5B/3,7B em Base/Instruct/Think, "permissive license" sem nome — [arXiv 2603.03543](https://arxiv.org/html/2603.03543)
- [FATO] Gervásio PT* (Univ. de Lisboa/PORTULAN, 2024): decoder com ajuste de instrução sobre o LLaMA 2 7B, variantes PT-PT e PT-BR, licença aberta para pesquisa e uso comercial (MIT no card HF). Há uma versão Gervásio 8B PT-PT sobre o Llama 3.1 8B Instruct — [arXiv 2402.18766](https://arxiv.org/html/2402.18766v2); [HF gervasio-8b-ptpt](https://huggingface.co/PORTULAN/gervasio-8b-portuguese-ptpt-decoder); [HF gervasio-7b-ptbr](https://huggingface.co/PORTULAN/gervasio-7b-portuguese-ptbr-decoder/raw/9f6f81d4c6b72daee3d2924729c801c2aba4579f/README.md)
- [FATO] Sabiá (Maritaca, 2023): o paper descreve o Sabiá-65B no nível do GPT-3.5-turbo — [arXiv 2304.07880](https://arxiv.org/pdf/2304.07880v1)
- [FATO] O **Sabiá-7B** é o único Sabiá com pesos públicos encontrado (`maritaca-ai/sabia-7b`). Usa arquitetura e tokenizador do LLaMA-1-7B, sequência máxima de 2048 e dados até meados de 2022. Segundo espelhos e agregadores, a licença segue a do LLaMA-1 (**só pesquisa**) e o modelo **não tem ajuste de instrução**, então recomendam few-shot — [HF maritaca-ai/sabia-7b](https://huggingface.co/maritaca-ai/sabia-7b/tree/main); [mav23/sabia-7b-GGUF](https://huggingface.co/mav23/sabia-7b-GGUF); [Featherless](https://featherless.ai/models/maritaca-ai/sabia-7b/readme). [OPINIÃO] Fica descartado para o PyGridPlan.
- [FATO] Tucano 2: o card do Tucano2-qwen-1.5B-Instruct declara Apache 2.0, e uma conversão MLX 4-bit do 3.7B-Instruct repete essa licença — [Friendli (card 1.5B)](https://friendli.ai/models/Polygl0t/Tucano2-qwen-1.5B-Instruct); [pessini/Tucano2-qwen-3.7B-Instruct-MLX-4bit](https://huggingface.co/pessini/Tucano2-qwen-3.7B-Instruct-MLX-4bit). Não encontrei GGUF oficial nem de quantizador conhecido do Tucano 2. Os GGUFs achados são da geração anterior (TucanoBR/Tucano-1b1 e 2b4-Instruct, Apache-2.0) — [tensorblock/Tucano-2b4-Instruct-GGUF](https://huggingface.co/tensorblock/Tucano-2b4-Instruct-GGUF); [cnmoro/Tucano-1b1-Instruct-Q8_0-GGUF](https://huggingface.co/cnmoro/Tucano-1b1-Instruct-Q8_0-GGUF)
- [FATO] Outros PT pequenos citados no PoETa v2: Curió 1.1B (TinyLlama) e 7B (Llama 2), em continuação de pré-treino; TeenyTinyLlama de 160M/460M, treinados do zero; GlórIA de 1,3B/2,7B, para PT europeu — [arXiv 2511.17808](https://arxiv.org/html/2511.17808v2)
- [FATO, snippet] Na coleção "best models" do Open PT LLM Leaderboard aparece o **Gemma-3 Gaia PT-BR 4B** (CEIA-UFG), um fine-tune PT-BR do Gemma 3. Os rótulos de tamanho e pontuação do snippet pareciam desalinhados — [Coleção eduagarcia](https://huggingface.co/collections/eduagarcia/portuguese-llm-leaderboard-best-models)

### Inferences
- [OPINIÃO] Para extrair slots em JSON, os modelos PT legados (Bode, Cabrita, GlórIA, Gervásio 7B, Sabiá-7B, CabraLlama) não compensam: são de 2023–2024, sobre bases Llama 2/Mistral, sem treino de tool calling e grandes demais (7B) para o orçamento de RAM. O ganho em PT não cobre a perda em seguir instruções e formato.
- [HIPÓTESE] Como o Tucano 2 3.7B herda do Qwen3-4B e tem tokenizador PT (menos tokens por frase, mais rápido em CPU), ele pode ser competitivo na compreensão do pedido. A fidelidade ao formato precisa ser medida, e o GBNF/grammar do llama.cpp mitiga o problema.
- [HIPÓTESE] A troca de tokenizador pode quebrar o template de tool calling herdado do Qwen. Melhor usar o Tucano com JSON por gramática do que com tool calling nativo.

### Gaps
- O card HF do Tucano2-qwen-3.7B-Instruct devolveu 401 ao fetch. A licença (Apache-2.0) vem de fontes indiretas, e o contexto continua desconhecido. Para usar no llama.cpp, provavelmente será preciso converter o GGUF por conta própria [HIPÓTESE].
- Não verifiquei Bode, Cabrita, Amadeus nem CabraLlama (as buscas não os trouxeram). Nenhum foi citado como [FATO].
- Não encontrei modelo PT-BR de 2026 além do Tucano 2 com avaliação de instruções; pode haver fine-tunes da comunidade sobre Qwen3.5/Gemma 4 não indexados.

## 3. Benchmarks e leaderboards de português — o que dizem sobre modelos pequenos e seus limites

### Takeaway
O **Open Portuguese LLM Leaderboard** (eduagarcia) tem 9 benchmarks PT-BR e mais de 1.100 modelos avaliados, quase todos de **múltipla escolha/classificação** (ENEM, BLUEX, OAB, ASSIN2, tweetSentBR, HateBR etc.). Ele mede conhecimento e compreensão, **não extração estruturada**. Para a europeia existe o CLARIN-PT-LDB (2026, generativo). Nenhum dos dois mede o que o PyGridPlan precisa.

### Cited Findings
- [FATO] O Open PT LLM Leaderboard é específico do português, com nove benchmarks, todos em PT-BR — [arXiv 2603.03543](https://arxiv.org/html/2603.03543) (descrição no paper do Tucano 2); config das tarefas em [pt_config.yaml](https://huggingface.co/spaces/eduagarcia/open_pt_llm_leaderboard/raw/07a1890fc6f2b4a28fd81f60da58146fdd39af47/tasks_config/pt_config.yaml)
- [FATO, secundária] O leaderboard já avaliou mais de 1.100 modelos, abertos e proprietários, com tarefas como ENEM e vestibulares — [Canaltech](https://canaltech.com.br/inteligencia-artificial/qual-e-a-melhor-ia-em-portugues-teste-avalia-conhecimentos-do-brasil/)
- [FATO] CLARIN-PT-LDB (mar/2026): leaderboard de PT europeu com dez benchmarks, avaliado de forma puramente generativa — [arXiv 2603.12872](https://arxiv.org/html/2603.12872)
- [FATO] PoETa v2 (nov/2025): 44 tarefas, 12 delas criadas originalmente em português, mais de 20 modelos avaliados, métrica NPM normalizada (0 = aleatório, 100 = perfeito) — [arXiv 2511.17808](https://arxiv.org/html/2511.17808v2). Um artigo do STIL 2026 avaliou três variantes do Qwen3-1.7B no PoETa v2. As médias gerais diferem em menos de 1 ponto percentual, mas a análise por origem, categoria e subárea mostra padrões bem diferentes — [ACL Anthology 2026.stil-1.18](https://aclanthology.org/2026.stil-1.18/)
- [FATO] O Tucano 2 adaptou IFEval, GSM8K, RULER e HumanEval ao português. O IFEval-PT é o mais próximo de "seguir formato" — [HF blog Tucano 2](https://huggingface.co/blog/Polygl0t/tucano2)
- [FATO] Nos benchmarks multilíngues do card, o Qwen3.5-4B tem MMMLU 76,1, MMLU-ProX 71,5 (média de 29 línguas), INCLUDE 71,0 e WMT24++ 66,6. O Gemma 4 E4B tem MMMLU 76,6 — [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B); [Gemma 4 E4B](https://huggingface.co/google/gemma-4-E4B-it)
- [FATO] O Phi-4-mini tem Multilingual MMLU 49,3 — [Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct). Os números de PT do SmolLM3 (modelo base): Global MMLU CF 36,88 e Belebele 47,67 — [SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B). As métricas e os protocolos são diferentes; não dá para comparar direto com Qwen/Gemma.

### Inferences
- [OPINIÃO] Múltipla escolha ≠ extração. Um bom ENEM/OAB indica compreensão do PT, mas não garante mapear "cantinho pra costura" para `oficina` nem tirar "bem longe" → intensidade 5. A decisão precisa de um **conjunto de teste próprio** (pedidos PT-BR coloquiais → JSON-ouro), com métricas de validade de schema, acerto de tipo, acerto de relação e erro de intensidade.
- [HIPÓTESE] Os números do MMMLU (Qwen3.5-4B 76,1 contra Phi-4-mini 49,3) indicam uma diferença grande de compreensão multilíngue entre gerações, embora os protocolos possam diferir.

### Gaps
- Não consegui ler o ranking atual do Space (é um app Gradio). Não sei se Qwen3.5-4B ou Gemma 4 E2B/E4B já foram avaliados lá nem com qual nota.
- Não extraí a Tabela 2 do PoETa v2 com os números por modelo. Napolab não foi pesquisado. [OPINIÃO] O achado do STIL (médias quase iguais, perfis diferentes) reforça que a média de um leaderboard não basta para escolher o modelo.

## 4. Benchmarks de saída estruturada / function calling para modelos pequenos

### Takeaway
O **BFCL V4** é a referência de function calling. Entre os pequenos com número no card oficial: **Qwen3.5-4B = 50,3** e Qwen3.5-9B = 66,1 (V4); **Granite-4.0-Micro = 59,98 (V3)**; SmolLM3-3B = 92,3 (versão/subconjunto não indicado). **V3 e V4 não são comparáveis.** Para JSON por schema, o **JSONSchemaBench** mostra que a decodificação restrita (inclusive no llama.cpp) garante a sintaxe e pode até acelerar. Em modelos pequenos, porém, ela garante a sintaxe e não a semântica.

### Cited Findings
- [FATO] O BFCL V4 avalia "the LLM's ability to call functions (aka tools) accurately" — [Berkeley leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)
- [FATO] Qwen3.5-4B: BFCL-V4 50,3 e IFEval 89,8. Qwen3.5-9B: BFCL-V4 66,1 e IFEval 91,5 — [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)
- [FATO] Qwen3.5-2B: BFCL-V4 43,6 (com raciocínio), IFEval 61,2 sem e 78,6 com raciocínio. Qwen3.5-0.8B: BFCL-V4 25,3, IFEval 52,1 sem e 44,0 com raciocínio. O card só informa BFCL com raciocínio — [Qwen/Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B). [OPINIÃO] Do 4B para o 2B a queda de IFEval é grande (89,8 → 61,2 sem raciocínio), e o 0,8B é fraco demais para a tarefa.
- [FATO] Granite-4.0-Micro: BFCL v3 59,98; IFEval 85,5 (instrução, strict), 79,12 (prompt, strict), média 82,31 — [granite-4.0-micro](https://huggingface.co/ibm-granite/granite-4.0-micro)
- [FATO] SmolLM3-3B: BFCL 92,3 sem raciocínio e 88,8 com raciocínio; IFEval 76,7 sem e 71,2 com — [SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B). O card não deixa claro qual versão ou subconjunto do BFCL foi usado. [HIPÓTESE] Provavelmente é um subconjunto simples do V3, logo não comparável ao 50,3 do V4.
- [FATO] Aviso de que BFCL v3 e v4 são suítes diferentes e "NOT cross-comparable" — [BenchLM BFCL v4](https://benchlm.ai/md/benchmarks/bfcl-v4.md)
- [FATO, terceiro] Fine-tune "CloudSurf-4B-FC" (QLoRA sobre Gemma 4 E4B) relata BFCL V4 de 55,53/54,86/56,81 em três seeds — [HF CloudSurf-4B-FC](https://huggingface.co/cloudsurf-software/CloudSurf-4B-FC). É autodeclarado e mostra que o Gemma 4 E4B fica na faixa de ~50 no V4 depois de fine-tune.
- [FATO, terceiro, não verificado] Relato de Phi-4-mini com BFCL v4 "low-to-mid 80s" sem linha oficial de Berkeley. A própria página pede cautela — [d-central](https://d-central.tech/local-llm-agent-capability/). [OPINIÃO] Não usar esse número.
- [FATO] JSONSchemaBench: 10K schemas, compara seis frameworks de decodificação restrita (Guidance, Outlines, **llama.cpp**, XGrammar, OpenAI, Gemini). O melhor cobre o dobro de schemas do pior. A decodificação restrita acelera a geração em até 50% e melhora tarefas a jusante em até 4% — [arXiv 2501.10868](https://arxiv.org/html/2501.10868v3)
- [FATO, snippet do resumo] StructureBench (IJCAI 2026), sobre modelos on-device de 0,5B–8B: a decodificação restrita "guarantees syntactic validity, it does not necessarily improve semantic accuracy; smaller models may degenerate under complex grammars" — [IJCAI 2026 p.267](https://www.ijcai.org/proceedings/2026/0267.pdf)
- [FATO, snippet do resumo] "The Constraint Tax": para modelos abaixo de 3B, o próprio schema pode virar "a material part of the generation problem" — [arXiv 2605.26128](https://arxiv.org/pdf/2605.26128)

### Inferences
- [OPINIÃO] Para o PyGridPlan, o BFCL importa menos que a **fidelidade a um schema fixo e pequeno**. Recomendo JSON por gramática (GBNF/`json_schema` do llama.cpp) em vez de tool calling nativo. Isso elimina a dependência do template de tools de cada modelo e garante a validade sintática; a validação semântica fica com o Pydantic.
- [OPINIÃO] Manter o schema raso: enum de tipos de cômodo, `intensity` como enum 1–5 e listas curtas. Isso reduz o "constraint tax" que os dois papers apontam para modelos menores que 3B.
- [HIPÓTESE] O IFEval alto do Qwen3.5-4B (89,8) sugere boa aderência a instruções de formato também sem gramática.

### Gaps
- Não acessei a tabela atual do BFCL (o site é dinâmico). Não confirmei se Qwen3.5-4B ou Gemma 4 E2B têm linha oficial.
- Não li os papers de StructureBench e Constraint Tax na íntegra; cito só os resumos.
- NexusRaven e o IFEval do Gemma 4 E2B/E4B não foram encontrados.

## 5. Licenças e implicações para um projeto de portfólio público

### Takeaway
Quase todos os candidatos de 2025–2026 têm **Apache-2.0** (Qwen3.5, Gemma 4, SmolLM3, Granite 4.0, Ministral 3) ou **MIT** (Phi-4-mini). Isso basta para um portfólio público com código aberto e para redistribuir ou baixar o modelo. A mudança do Gemma para Apache-2.0 na geração 4 tira o atrito dos "Gemma Terms". O Llama 3.2 e o EXAONE são os casos restritivos.

### Cited Findings
- [FATO] Qwen3.5-4B: apache-2.0 — [card](https://huggingface.co/Qwen/Qwen3.5-4B)
- [FATO] Gemma 4 E4B: Apache 2.0 — [card](https://huggingface.co/google/gemma-4-E4B-it)
- [FATO] SmolLM3-3B: Apache 2.0 — [card](https://huggingface.co/HuggingFaceTB/SmolLM3-3B)
- [FATO] Granite-4.0-Micro: Apache 2.0 — [card](https://huggingface.co/ibm-granite/granite-4.0-micro)
- [FATO] Ministral 3 (os nove modelos): Apache 2.0 — [arXiv 2601.08584](https://arxiv.org/abs/2601.08584v1); [HF](https://huggingface.co/mistralai/Ministral-3-3B-Base-2512)
- [FATO] Phi-4-mini-instruct: MIT — [card](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [FATO] Gervásio: licença aberta para pesquisa e uso comercial (MIT no card) — [arXiv 2402.18766](https://arxiv.org/html/2402.18766v2)
- [FATO] Tucano 2: "permissive license", sem nome no post nem no trecho lido do paper — [blog](https://huggingface.co/blog/Polygl0t/tucano2)
- [FATO, secundária] O checkpoint maior do Qwen3.8 teria licença própria, diferente da do 27B (Apache) — [Codersera/aggregadores via busca](https://slash-digital.io/en/insights/open-weight-models-2026/). Não afeta os tamanhos pequenos.

### Inferences
- [HIPÓTESE, conhecimento prévio] A Llama 3.2 Community License exige o aviso "Built with Llama", tem política de uso aceitável e limite de 700M MAU. A licença do EXAONE é não comercial. Ambas são aceitáveis para estudo, mas menos limpas para um portfólio. Preferir Apache/MIT.
- [OPINIÃO] O app não deve **embutir** o GGUF no repositório. Basta baixar sob demanda e registrar no README o modelo, o quantizador e a licença.

### Gaps
- Qwen3.5-2B: Apache-2.0, confirmado no card. Gemma 4 E2B: Apache 2.0, confirmado no card. A licença do Tucano 2 (Apache-2.0) vem só de fontes indiretas (card do 1.5B e conversão MLX). A do Qwen3.5-0.8B é inferida pela família.

## 6. Disponibilidade de GGUF, tamanhos de arquivo e contexto

### Takeaway
Os dois candidatos principais têm GGUF da **unsloth** em todos os níveis de quantização. **Qwen3.5-4B Q4_K_M = 2,74 GB**, o que cabe com folga. **Gemma 4 E2B Q4_K_M = 3,11 GB**. O **Gemma 4 E4B Q4_K_M = 4,98 GB** é pesado demais para 8 GB compartilhados com CP-SAT e navegador.

### Cited Findings
- [FATO] unsloth/Qwen3.5-4B-GGUF: Q4_K_M 2,74 GB; Q5_K_M 3,14 GB; Q8_0 4,48 GB; UD-Q4_K_XL 2,91 GB; IQ4_XS 2,48 GB; Q3_K_M 2,29 GB. O mmproj (visão) é separado: BF16 676 MB — [HF tree](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/tree/main)
- [FATO] unsloth/Qwen3.5-2B-GGUF: Q4_K_M 1,28 GB; Q5_K_M 1,44 GB; Q8_0 2,01 GB; mmproj BF16 671 MB à parte — [HF tree](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF/tree/main)
- [FATO] unsloth/gemma-4-E2B-it-GGUF: Q4_K_M 3,11 GB; Q5_K_M 3,36 GB; Q8_0 5,05 GB; IQ4_XS 2,98 GB. mmproj ~987 MB e drafter MTP de 97,8 MB — [HF tree](https://huggingface.co/unsloth/gemma-4-E2B-it-GGUF/tree/main)
- [FATO] unsloth/gemma-4-E4B-it-GGUF: Q4_K_M 4,98 GB; Q5_K_M 5,48 GB; Q8_0 8,19 GB; Q3_K_M 4,06 GB — [HF tree](https://huggingface.co/unsloth/gemma-4-E4B-it-GGUF/tree/main)
- [FATO] Contexto: Qwen3.5-4B tem 262.144 nativos; Gemma 4 E2B/E4B, 128K; SmolLM3, 64k (128k com YaRN); Granite-4.0-Micro, 128K; Ministral 3 3B, 256k; Phi-4-mini, 128K — cards citados nas seções 1 e 5.

### Inferences
- [HIPÓTESE] O GGUF do Gemma 4 é grande para o "tamanho efetivo" porque inclui as embeddings por camada (E4B = "8B with embeddings"). Em RAM, o custo real pode ser menor se o llama.cpp mapear essas tabelas com mmap, mas isso precisa ser medido.
- [OPINIÃO] O pedido do PyGridPlan tem poucas centenas de tokens. Um contexto de 2–4K basta e limita o KV-cache, então o contexto longo dos cards é irrelevante e deve ser **reduzido** (`-c 4096`) para poupar RAM.
- [HIPÓTESE] Orçamento estimado para o Qwen3.5-4B Q4_K_M com ctx 4K: ~3–3,5 GB residentes. É viável ao lado de CP-SAT e navegador em 8 GB, mas apertado. O Qwen3.5-2B ou o Gemma 4 E2B servem de plano B.

### Gaps
- [FATO] Não encontrei GGUF do Tucano 2 (Polygl0t), só MLX 4-bit da comunidade — [pessini MLX](https://huggingface.co/pessini/Tucano2-qwen-3.7B-Instruct-MLX-4bit).
- Não conferi os tamanhos de GGUF de Qwen3.5-0.8B, SmolLM3, Granite-4.0-Micro, Ministral 3 3B, Phi-4-mini e Tucano 2. Também não conferi repositórios de bartowski/ggml-org (só a unsloth).
- Não há medição de tokens/s no i5-1335U; é preciso fazer benchmark local.

## 7. Modos de raciocínio ("thinking") em modelos pequenos: latência e efeito na extração JSON

### Takeaway
Qwen3.5, Gemma 4 e SmolLM3 têm raciocínio **alternável**. Desligar é obrigatório no PyGridPlan, por latência em CPU. O Qwen3.5-4B vem com **raciocínio ligado por padrão**, e o Qwen3.5-2B **desligado por padrão**. Nos dois casos, o Qwen3.5 e **não aceita** mais `/think`/`/no_think`: desliga-se com `enable_thinking: False` no template. No SmolLM3, os números de BFCL e IFEval **caem** com o raciocínio ligado.

### Cited Findings
- [FATO] Qwen3.5: "operate in thinking mode by default". Para desligar, usar `"chat_template_kwargs": {"enable_thinking": False}`. O Qwen3.5 "does not officially support" os soft switches `/think` e `/nothink`. O tool calling exige parser (`qwen3_coder`) no servidor — [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)
- [FATO] Qwen3.5-2B: "operates in non-thinking mode by default". O IFEval do 2B **sobe** com raciocínio (61,2 → 78,6), mas o do 0,8B **cai** (52,1 → 44,0) — [Qwen/Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B). [HIPÓTESE] No 2B, ligar o raciocínio pode compensar em qualidade, ao custo de latência; vale medir no conjunto próprio.
- [FATO] Gemma 4: o raciocínio é ligado pelo token `<|think|>` no início do system prompt. Sem o token (ou com `enable_thinking=False`), fica desligado — [gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it)
- [FATO] SmolLM3: raciocínio estendido ligado por padrão, alternável com `/think`/`/no_think` no system prompt ou com o kwarg `enable_thinking`. O flag no system prompt prevalece. BFCL 92,3 sem raciocínio contra 88,8 com; IFEval 76,7 contra 71,2 — [SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B)
- [FATO] O Tucano 2 tem variante "Think" separada, que raciocina em português, e uma Instruct sem raciocínio — [blog](https://huggingface.co/blog/Polygl0t/tucano2)

### Inferences
- [OPINIÃO] Em CPU, um traço de raciocínio de centenas de tokens multiplica a latência (a geração é sequencial) e ainda pode "vazar" para fora do JSON. Com gramática ativa desde o primeiro token, o modelo nem consegue emitir o bloco de raciocínio. É preciso desligar o raciocínio **no template** para não haver conflito.
- [HIPÓTESE] No llama.cpp (`llama-server`), o `enable_thinking` passa por `chat_template_kwargs`; o comportamento exato por versão precisa ser verificado no M5.
- [HIPÓTESE] O dado do SmolLM3 (o raciocínio piora tool calling e IFEval) sugere que, em extração simples, o raciocínio não ajuda os modelos pequenos. Isso precisa ser confirmado no conjunto de teste próprio.

### Gaps
- Não encontrei medições publicadas da latência com e sem raciocínio em CPU para esses modelos.

## 8. Relatos de modelos pequenos em slot-filling / NER / extração de intenção em português

### Takeaway
Não encontrei relatos publicados e confiáveis de LLMs pequenos (≤ 8B) usados em slot-filling ou extração de intenção para JSON **em PT-BR**. A evidência disponível é indireta: IFEval-PT do Tucano 2, benchmarks multilíngues e literatura de decodificação restrita.

### Cited Findings
- [FATO] O SFT do Tucano 2 inclui tool use e saída estruturada em português, mas não há avaliação publicada dessas capacidades — [blog](https://huggingface.co/blog/Polygl0t/tucano2)
- [FATO] O Open PT LLM Leaderboard é dominado por classificação e múltipla escolha (ENEM, ASSIN etc.), sem tarefa de extração para JSON — [pt_config.yaml](https://huggingface.co/spaces/eduagarcia/open_pt_llm_leaderboard/raw/07a1890fc6f2b4a28fd81f60da58146fdd39af47/tasks_config/pt_config.yaml)
- [FATO] Para modelos on-device de 0,5–8B, a decodificação restrita garante a sintaxe mas não a semântica — [IJCAI 2026](https://www.ijcai.org/proceedings/2026/0267.pdf)

### Inferences
- [OPINIÃO] Essa lacuna é uma **oportunidade de portfólio**: um conjunto de teste PT-BR de pedidos de planta (coloquial → JSON-ouro), com métricas por campo, comparando 3–4 modelos locais, é contribuição original e verificável.
- [OPINIÃO] Estratégia de prompt sugerida para o teste: um system prompt com o catálogo (id, sinônimos PT-BR) e uma tabela de intensidade verbal ("perto"=3, "bem perto/colado"=5, "longe"=3, "bem longe/o mais longe possível"=5), mais 3–5 exemplos few-shot e gramática JSON. Sinônimos determinísticos e um pós-processamento em Python reduzem o que o modelo precisa "saber".

### Gaps
- Não pesquisei a fundo relatos de NER/intent em PT com modelos pequenos (como benchmarks de intenção HAREM/MASSIVE-pt ou MASSIVE com LLMs); o orçamento de busca acabou antes.
