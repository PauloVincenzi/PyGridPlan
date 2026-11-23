# Requisitos de hardware para LLM pequeno local (CPU/iGPU) — estimativa para o i5-1335U / 8 GB

> Notas de pesquisa (trilha M5). Estado em novembro de 2026. Rótulos: **[FATO]** = medido ou publicado por terceiros, com fonte; **[HIPÓTESE]** = estimativa do pesquisador a partir de fatos citados; **[OPINIÃO]** = julgamento. Os dados da máquina-alvo (i5-1335U, 8 × 1 GB LPDDR4x-4267, Iris Xe, Windows 11 Home, Galaxy Book 750XGK) foram medidos pelo coordenador em 2026-11-22 e não são repetidos aqui como fonte externa.

## 1. Especificações da máquina que importam para inferência (CPU, memória, iGPU)

### Takeaway
O i5-1335U tem 2 P + 8 E núcleos, 2 canais de memória e iGPU Iris Xe com 80 EU a 1,25 GHz. Com LPDDR4x-4267 num barramento de 128 bits, a banda teórica é de cerca de 68 GB/s. Uma máquina-irmã (750XGK com i7-1355U) mediu entre 58 e 62 GB/s de leitura efetiva pela iGPU. O chassi Samsung segura o processador em cerca de 23 W sustentados, contra 39 W de pico.

### Cited Findings
- [FATO] Intel ARK, i5-1335U: 10 núcleos (2 P + 8 E), 12 threads, P-core até 4,6 GHz, E-core até 3,4 GHz. Potência base de 15 W, turbo máximo de 55 W e mínimo assegurado de 12 W. Suporta LPDDR4x até 4267 MT/s, LPDDR5/x até 6400, DDR5 até 5200 e DDR4 até 3200, com 2 canais de memória no máximo. GPU "Iris Xe Graphics eligible", **80 EU**, frequência máxima de 1,25 GHz. Extensões listadas: "SSE4.1, SSE4.2, AVX2". A ARK **não lista** AVX-VNNI (o pedido do coordenador citou AVX-VNNI por conhecimento prévio, **sem medição local**: o CIM não lista extensões de instrução) nem a banda máxima de memória. Lançamento no 1º trimestre de 2023. — [Intel ARK i5-1335U](https://www.intel.com/content/www/us/en/products/sku/232153/intel-core-i51335u-processor-12m-cache-up-to-4-60-ghz/specifications.html)
- [FATO] Banda teórica por tipo de memória para o i5-1335U: LPDDR4X-4266 = **68,2 GB/s**, LPDDR5-6400 = 102,4 GB/s, DDR5-5200 = 83,2 GB/s, DDR4-3200 = 51,2 GB/s. — [CPU-Monkey](https://www.cpu-monkey.com/en/cpu-intel_core_i5_1335u). Outro agregador cita 89,6 GB/s sem dizer o tipo de memória, então foi ignorado — [CPU-Compare](https://cpu-compare.com/cpu/intel_core_i5-1335u)
- [FATO] O die completo tem 96 EU, e o i5-1335U ativa 80 deles (o i7-1355U ativa os 96). — [Notebookcheck (PL)](https://notebookcheck.pl/Intel-Raptor-Lake-U-i5-1335U.773122.0.html) (conteúdo visto só pelo snippet da busca), coerente com a ARK (80 EU) e com o relato do i7-1355U (96 EU) em [inferzero #76](https://github.com/rizagp/inferzero/issues/76)
- [FATO] Review do Samsung Galaxy Book3 15 com i5-1335U (unidade **NP750XFG**, não 750XGK). Em High Performance, o clock da CPU se estabiliza em **PL2 de 39 W e PL1 de 23 W (dinâmico)**. A RAM é "16 GB of LPDDR4x RAM (non-replaceable) running at 2133 MHz with quad-channel operation" (4 × 32 bits = 128 bits). No laço de Cinebench R15 multi, a média foi de 1259 pontos, com faixa de 1080,88 a 1547,27; o desempenho foi "consistente", com leve queda no fim. No modo Quiet, o Cinebench perde cerca de 15%. Na bateria, em "Balanced", fica disponível "around 85 percent power". — [Notebookcheck, review Galaxy Book3](https://www.notebookcheck.net/Samsung-Galaxy-Book3-review-The-Intel-Core-i5-1335U-celebrates-a-solid-premiere.723256.0.html)
- [FATO] Máquina-irmã, Samsung Galaxy Book **750XGK** com i7-1355U e Iris Xe de 96 EU (Gen12.2 Xe-LP, "DP4a only, no XMX"), 15 GiB de LPDDR, Xubuntu 26.04.1. O `gpu_bench` mediu **leitura de memória de 57,6 a 61,9 GB/s**, FP16 vetorial de 3,34 TFLOPS (87% dos 3,84 teóricos) e INT8 DP4a de 3,67 TOPS (48% dos 7,68). Com o clock da iGPU limitado a 1250 MHz, foram registrados "Package Thermal Throttles: 0". Relato publicado em 2026-11-21. — [inferzero issue #76](https://github.com/rizagp/inferzero/issues/76)

### Inferences
- [HIPÓTESE] Banda teórica da máquina-alvo: 4267 MT/s × 16 bytes (128 bits) ≈ **68,3 GB/s**, o que bate com os 68,2 GB/s do CPU-Monkey. É o teto físico da geração de tokens, e ele vale tanto para a CPU quanto para a iGPU, que dividem a mesma RAM.
- [HIPÓTESE] O i5 tem 80 EU contra 96 do i7 da máquina-irmã (cerca de 17% menos) e clock máximo de 1,25 contra 1,3 GHz. O prefill na iGPU depende de computação, então deve ficar perto de 80 a 83% do medido no i7-1355U. A geração depende de banda, então deve mudar pouco.
- [HIPÓTESE] O teto de 55 W da ARK não vale neste chassi. O que conta é o PL1 de cerca de 23 W do chassi Samsung (medido no 750XFG; o 750XGK provavelmente segue o mesmo perfil, mas isso não foi confirmado).

### Gaps
- Não achei review de Notebookcheck nem medição de PL1/PL2 específica do **750XGK** com i5-1335U.
- A ARK não confirma AVX-VNNI. A presença da instrução não foi medida localmente (veio do pedido do coordenador, sem medição); falta conferir com uma ferramenta como o Coreinfo da Sysinternals. Não confirmei por fonte primária quanto o llama.cpp ganha com AVX-VNNI em Raptor Lake.

## 2. Matemática de memória: arquivo GGUF, cache KV e overhead

### Takeaway
Na prática, a memória é o arquivo GGUF mais o cache KV mais buffers de computação. Com Q4_K_M, os candidatos de 1,5 a 4B ocupam de 1,0 a 2,7 GB em disco. Com contexto de 2 a 4k, o cache KV vai de dezenas a algumas centenas de MiB, conforme a arquitetura. Os Qwen3.5 híbridos têm cache KV muito pequeno. Qwen3-4B e Llama 3.2 3B têm cache grande, e Gemma 3 depende do cache SWA. Modelos de 7 a 9B em Q4 (4,5 a 5,7 GB) não cabem com folga em 7,7 GB junto com Windows, navegador e CP-SAT.

### Cited Findings
- [FATO] Tamanhos de arquivo GGUF (bytes da API do Hugging Face, em GB decimais), consultados em 2026-11-22 (repositórios abaixo):

| Modelo | IQ4_XS | Q4_K_M | Q5_K_M | Q6_K | Q8_0 |
|---|---|---|---|---|---|
| Qwen2.5-0.5B-Instruct | 0,35 | 0,40 | 0,42 | 0,51 | 0,53 |
| Qwen3.5-0.8B | 0,49 | 0,53 | 0,59 | 0,64 | 0,81 |
| Llama-3.2-1B-Instruct | 0,74 | 0,81 | 0,91 | 1,02 | 1,32 |
| Qwen2.5-1.5B-Instruct | 0,90 | 0,99 | 1,13 | 1,27 | 1,65 |
| Qwen3-1.7B | 1,18 | 1,28 | 1,47 | 1,67 | 2,17 |
| Qwen3.5-2B | 1,17 | 1,28 | 1,44 | 1,57 | 2,01 |
| Qwen2.5-3B-Instruct | 1,74 | 1,93 | 2,22 | 2,54 | 3,29 |
| Llama-3.2-3B-Instruct | 1,83 | 2,02 | 2,32 | 2,64 | 3,42 |
| Gemma-3-4b-it | 2,26 | 2,49 | 2,83 | 3,19 | 4,13 |
| Qwen3-4B | 2,27 | 2,50 | 2,89 | 3,31 | 4,28 |
| Qwen3.5-4B | 2,48 | 2,74 | 3,14 | 3,53 | 4,48 |
| Qwen2.5-7B-Instruct | 4,22 | 4,68 | 5,44 | 6,25 | 8,10 |
| Llama-3.1-8B-Instruct | 4,45 | 4,92 | 5,73 | 6,60 | 8,54 |
| Qwen3.5-9B | 5,17 | 5,68 | 6,58 | 7,46 | 9,53 |

  Fontes: [bartowski/Qwen2.5-0.5B](https://huggingface.co/bartowski/Qwen2.5-0.5B-Instruct-GGUF), [bartowski/Qwen2.5-1.5B](https://huggingface.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF), [bartowski/Qwen2.5-3B](https://huggingface.co/bartowski/Qwen2.5-3B-Instruct-GGUF), [bartowski/Qwen2.5-7B](https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF), [bartowski/Qwen3-1.7B](https://huggingface.co/bartowski/Qwen_Qwen3-1.7B-GGUF), [bartowski/Qwen3-4B](https://huggingface.co/bartowski/Qwen_Qwen3-4B-GGUF), [bartowski/Llama-3.2-1B](https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF), [bartowski/Llama-3.2-3B](https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF), [bartowski/Llama-3.1-8B](https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF), [bartowski/gemma-3-4b-it](https://huggingface.co/bartowski/google_gemma-3-4b-it-GGUF), [unsloth/Qwen3.5-0.8B](https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF), [unsloth/Qwen3.5-2B](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF), [unsloth/Qwen3.5-4B](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF), [unsloth/Qwen3.5-9B](https://huggingface.co/unsloth/Qwen3.5-9B-GGUF). As quantizações de repositórios diferentes (bartowski vs unsloth) podem usar receitas diferentes (imatrix, camadas mantidas em precisão maior), então a comparação entre famílias é aproximada.

- [FATO] Parâmetros de atenção tirados do `config.json` de cada modelo (camadas / cabeças KV / head_dim). Onde o campo `head_dim` não existe, usei hidden_size ÷ num_attention_heads.
  - Qwen2.5-0.5B: 24 / 2 / 64 — [config](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/main/config.json)
  - Qwen2.5-1.5B: 28 / 2 / 128 (1536 ÷ 12) — [config](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/main/config.json)
  - Qwen2.5-3B: 36 / 2 / 128 (2048 ÷ 16) — [config](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/main/config.json)
  - Qwen2.5-7B: 28 / 4 / 128 — [config](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct/blob/main/config.json)
  - Qwen3-1.7B: 28 / 8 / 128 — [config](https://huggingface.co/Qwen/Qwen3-1.7B/blob/main/config.json)
  - Qwen3-4B: 36 / 8 / 128 — [config](https://huggingface.co/Qwen/Qwen3-4B/blob/main/config.json)
  - Llama-3.2-1B: 16 / 8 / 64 — [config (espelho unsloth)](https://huggingface.co/unsloth/Llama-3.2-1B-Instruct/blob/main/config.json)
  - Llama-3.2-3B: 28 / 8 / 128 — [config (espelho unsloth)](https://huggingface.co/unsloth/Llama-3.2-3B-Instruct/blob/main/config.json)
  - Llama-3.1-8B: 32 / 8 / 128 — [config (espelho unsloth)](https://huggingface.co/unsloth/Meta-Llama-3.1-8B-Instruct/blob/main/config.json)
  - Gemma-3-4B: 34 / 4 / 256, com `sliding_window: 1024` e `sliding_window_pattern: 6` (5 camadas locais para 1 global) — [config (espelho unsloth)](https://huggingface.co/unsloth/gemma-3-4b-it/blob/main/config.json)
  - Qwen3.5-0.8B e 2B: 24 camadas, sendo **18 `linear_attention` e 6 `full_attention`** (`full_attention_interval: 4`), cabeças KV 2, head_dim 256 — [config 2B](https://huggingface.co/Qwen/Qwen3.5-2B/blob/main/config.json), [config 0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B/blob/main/config.json)
  - Qwen3.5-4B e 9B: 32 camadas, sendo **24 lineares e 8 full**, cabeças KV 4, head_dim 256, 32 cabeças de valor lineares de 128 × 128 — [config 4B](https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/config.json), [config 9B](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/config.json)
- [FATO] No llama.cpp, o tipo do cache KV é configurado por `-ctk/--cache-type-k` e `-ctv/--cache-type-v` (padrão f16). Flash Attention é `-fa on|off|auto` (padrão `auto`), e `--swa-full` ("use full-size SWA cache", padrão false) indica que, por padrão, as camadas de janela deslizante guardam só a janela. — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] Ollama: "The K/V context cache can be quantized to significantly reduce memory usage when Flash Attention is enabled", via `OLLAMA_KV_CACHE_TYPE` (padrão `f16`, global para todos os modelos). O contexto padrão é de 4096 tokens (`OLLAMA_CONTEXT_LENGTH`). — [Ollama FAQ](https://docs.ollama.com/faq)
- [FATO] mmap no llama.cpp: a opção agora fica em `--load-mode`. "mmap: memory-map model (if mmap disabled, slower load but may reduce pageouts if not using mlock)" e "mlock: force system to keep model in RAM rather than swapping or compressing". — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

### Inferences
- [HIPÓTESE] Fórmula: bytes de KV por token = 2 (K e V) × camadas com atenção plena × cabeças KV × head_dim × bytes por elemento. Em f16 são 2 bytes. Em q8_0 são cerca de 1,0625 bytes (blocos de 32 valores int8 com escala f16, ou seja, 34 bytes por 32 elementos). Resultados calculados:

| Modelo | KiB/token (f16) | 2k f16 / q8_0 | 4k f16 / q8_0 | 8k f16 / q8_0 |
|---|---|---|---|---|
| Qwen2.5-1.5B | 28 | 56 / 30 MiB | 112 / 60 MiB | 224 / 119 MiB |
| Qwen2.5-3B | 36 | 72 / 38 MiB | 144 / 76 MiB | 288 / 153 MiB |
| Qwen3-1.7B | 112 | 224 / 119 MiB | 448 / 238 MiB | 896 / 476 MiB |
| Qwen3-4B | 144 | 288 / 153 MiB | 576 / 306 MiB | 1152 / 612 MiB |
| Llama-3.2-1B | 32 | 64 / 34 MiB | 128 / 68 MiB | 256 / 136 MiB |
| Llama-3.2-3B | 112 | 224 / 119 MiB | 448 / 238 MiB | 896 / 476 MiB |
| Gemma-3-4B (se todas as 34 camadas fossem plenas) | 136 | 272 / 144 MiB | 544 / 289 MiB | 1088 / 578 MiB |
| Gemma-3-4B com cache SWA (5 globais + 29 locais, janela 1024 + ubatch 512) | — | cerca de 215 MiB | cerca de 255 a 265 MiB | cerca de 335 a 360 MiB (f16) |
| Qwen3.5-0.8B / 2B (6 camadas plenas) | 12 | 24 / 13 MiB | 48 / 26 MiB | 96 / 51 MiB |
| Qwen3.5-4B / 9B (8 camadas plenas) | 32 | 64 / 34 MiB | 128 / 68 MiB | 256 / 136 MiB |
| Qwen2.5-7B | 56 | 112 / 60 MiB | 224 / 119 MiB | 448 / 238 MiB |
| Llama-3.1-8B | 128 | 256 / 136 MiB | 512 / 272 MiB | 1024 / 544 MiB |

- [HIPÓTESE] Nos Qwen3.5, as camadas lineares (Gated DeltaNet) guardam um estado recorrente de tamanho fixo, que não cresce com o contexto. Pela conta 18 camadas × 16 cabeças × 128 × 128 × 4 bytes, dá cerca de 18 MiB no 2B. No 4B (24 × 32 × 128 × 128 × 4) dá cerca de 48 MiB. Faltam o estado de convolução e a forma exata como o llama.cpp aloca isso; o spike deve medir.
- [HIPÓTESE] Para o caso PyGridPlan (prompt de 800 a 1500 tokens mais 200 de saída), **contexto de 2048 basta**, e 4096 dá folga. O Ollama usa 4096 por padrão. Nessa faixa, o cache KV é irrelevante nos Qwen2.5 e Qwen3.5 (menos de 150 MiB) e moderado no Qwen3-4B e no Llama-3.2-3B (até cerca de 580 MiB em f16 com 4k). Quantizar o KV em q8_0 só vale a pena para estes últimos e exige Flash Attention.
- [HIPÓTESE] Memória residente esperada ≈ arquivo GGUF + KV + buffers de computação (centenas de MiB, que crescem com `-ub`/`-b` e com o vocabulário: 248k nos Qwen3.5 e 262k no Gemma 3) + runtime (dezenas de MiB). Para Qwen3.5-2B Q4_K_M com 4k: cerca de 1,3 + 0,05 + 0,2 a 0,4 ≈ **1,6 a 1,8 GB**. Para um 3 a 4B Q4_K_M: cerca de **2,4 a 3,5 GB**. Para um 7 a 9B Q4_K_M: **5 a 6,5 GB**, inviável junto com o resto em 7,7 GB.
- [HIPÓTESE] Windows e mmap: com mmap, os pesos são páginas de arquivo. Sob pressão de memória, o Windows pode descartá-las sem gravar no pagefile e depois relê-las do SSD, o que causa falhas de página "duras" e quedas fortes e intermitentes de tokens/s. O risco real de pagefile vem da memória privada (KV, buffers, CP-SAT, navegador). `--load-mode mlock` reduz esse risco, mas no Windows o `VirtualLock` depende do tamanho do working set do processo. Não confirmei por fonte se o llama.cpp ajusta isso sozinho.
- [HIPÓTESE] Com a iGPU (Vulkan, `-ngl 99`), os pesos são copiados para buffers de GPU que ficam na mesma RAM do sistema. Se as páginas mmap do arquivo também ficarem residentes, o modelo pode ocupar até cerca de 2 vezes o tamanho do arquivo durante ou depois da carga. O spike deve medir isso, porque pode inverter a escolha entre CPU e iGPU numa máquina de 8 GB.

### Gaps
- Não encontrei fonte com o consumo base do Windows 11 Home mais um navegador numa máquina de 8 GB. A faixa de 3 a 5 GB citada no pedido continua sem fonte. A medição do coordenador (só 0,6 GB livres) indica que a máquina já opera perto do limite.
- Não confirmei por fonte o comportamento exato do llama.cpp no Windows com mmap mais Vulkan (se libera as páginas do arquivo depois do upload).
- O overhead de buffers de computação por modelo não foi medido por terceiros para estes modelos. Fica para o spike, lendo o log de carga (o llama.cpp imprime os tamanhos dos buffers CPU/Vulkan e do KV).

## 3. Velocidade: geração limitada por banda, prefill limitado por computação, e benchmarks publicados

### Takeaway
O dado publicado mais próximo foi medido em **uma máquina-irmã quase idêntica** (Galaxy Book 750XGK com i7-1355U). Lá, llama.cpp com Vulkan na Iris Xe rodou Qwen3.5-2B Q4_K_M (1,18 GiB) a **cerca de 420 t/s de prefill (pp512)**, **339 t/s em pp4096** e **cerca de 22 t/s de geração (tg128)**. Isso dá uma banda efetiva de cerca de 28 GB/s, perto de 41% dos 68 GB/s teóricos. Não achei benchmark publicado de llama.cpp **só na CPU** para i5-1335U, i7-1355U, i5-1235U ou chips equivalentes; as estimativas de CPU abaixo são hipóteses.

### Cited Findings
- [FATO] Na Iris Xe do i7-1355U (750XGK, 96 EU, clock limitado a 1250 MHz, Linux Mesa ANV), com llama.cpp Vulkan `-dev Vulkan0 -ngl 99 -t 2 -b 512 -ub 256 -fa 1 -ctk f16 -ctv f16` e Qwen3.5-2B-Q4_K_M.gguf (1,18 GiB): **pp512 = 420,06 t/s, pp4096 = 338,60 t/s, tg128 = 21,98 t/s**. O backend Level Zero alternativo (inferzero) fez cerca de 196 t/s de pp512 e 12,6 a 15,2 t/s de tg128. A versão do llama.cpp não foi informada. — [inferzero issue #76](https://github.com/rizagp/inferzero/issues/76)
- [FATO] Discussão oficial de Vulkan do llama.cpp, com o modelo padrão Llama 2 7B Q4_0 (3,56 GiB):
  - Iris Xe TGL GT2 (i7-1185G7, Tiger Lake): pp512 = 42,02 e tg128 = 7,28 (build 4459, jan/2025); depois de patches, pp512 ≈ 50,9 e tg128 ≈ 7,9 a 8,3 (fev/2025).
  - Outro usuário (build 5568, jun/2025): pp512 = 106,19 e tg128 = 5,89 com ngl 100, e pp512 = 73,26 e tg128 = 5,24 com **ngl 0**.
  - Para comparação de gerações: Arc 140V (Lunar Lake) chega a pp512 ≈ 865 e tg128 ≈ 24 a 25.
  - Comando padrão da thread: `llama-bench -m llama-2-7b.Q4_0.gguf -ngl 100 -fa 0,1`.
  - Fonte: [llama.cpp Discussion #10879](https://github.com/ggml-org/llama.cpp/discussions/10879)
- [FATO] O prefill (pp) "is typically compute limited" e a geração (tg) "is typically memory limited". — [llm-tracker, Benchmarking Cheat-Sheet](https://llm-tracker.info/howto/LLM-Inference-Benchmarking-Cheat%E2%80%91Sheet-for-Hardware-Reviewers) (conteúdo visto pelo snippet da busca)
- [FATO] Ponto de referência só de CPU, em ARM e de qualidade baixa: Raspberry Pi 5 com 4 threads e um modelo de 1,7B fez pp512 = 61,89 t/s e tg128 = 9,10 t/s. — [peppe8o](https://peppe8o.com/install-llama-cpp-raspberry-pi/) (visto só pelo snippet da busca)
- [FATO] Fontes secundárias e de qualidade baixa, sem chip identificado: "Laptop (i7, DDR4 dual-ch)" a cerca de 20 tok/s com um 3B Q4 — [InsiderLLM](https://insiderllm.com/guides/cpu-only-llms-what-actually-works/); Qwen3 4B em 4 bits a 15 a 18 tok/s em laptop de 8 GB com gráficos integrados (sem Iris Xe; cita Wildcat Lake) — [MindStudio](https://www.mindstudio.ai/blog/run-qwen-llama-cpp-low-ram-laptop/). Servem só como ordem de grandeza.
- [FATO] Núcleos híbridos: na discussão #572 do llama.cpp (antiga, Alder Lake), usuários relatam que usar todos os threads, E-cores incluídos, costuma ser pior que usar só os P-cores. A explicação dada é que threads que terminam cedo ficam em espera ativa (busy-wait), e os mais lentos (E-cores) seguram o passo. Um caso de `-t 6` reduziu o tempo de avaliação de cerca de 126 s para cerca de 42 s. — [llama.cpp Discussion #572](https://github.com/ggerganov/llama.cpp/discussions/572). Relatos de 2024 no r/LocalLLaMA são mistos (há quem não veja ganho) — [Reddit](https://libreddit.winscloud.net/r/LocalLLaMA/comments/1codot3/unlock_unprecedented_performance_boosts_with/l3ej877/?context=3). Num i7-8700 (não híbrido), a geração atingiu o pico com 8 threads e caiu com 12 — [InventiveHQ](https://inventivehq.com/blog/cpu-thread-scaling-llm-inference)
- [FATO] O llama.cpp separa `-t/--threads` (geração) de `--threads-batch` (prefill), e oferece `--cpu-mask`/`--cpu-range` para afinidade e `--prio` para prioridade. — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

### Inferences
- [HIPÓTESE] Validação do modelo "tg ≈ banda efetiva ÷ bytes lidos por token". Na máquina-irmã, 21,98 t/s × 1,27 GB ≈ **27,9 GB/s efetivos** (cerca de 41% dos 68 GB/s). Na Iris Xe TGL com 7B Q4_0 (3,82 GB), 7,3 a 8,3 t/s dão cerca de **28 a 32 GB/s** pela mesma conta. Os dois casos convergem para cerca de 28 a 32 GB/s em LPDDR4x com Iris Xe. Uso **25 a 40 GB/s** como faixa de banda efetiva, com o limite superior representando uma CPU bem afinada.
- [HIPÓTESE] Geração estimada na máquina-alvo (Q4_K_M, sem CP-SAT rodando ao mesmo tempo): 25 a 40 GB/s ÷ tamanho do arquivo.

| Modelo (Q4_K_M) | Arquivo | tg estimada | Conferência com dado publicado |
|---|---|---|---|
| Qwen3.5-0.8B | 0,53 GB | 35 a 60 t/s (modelos minúsculos rendem menos que a conta; overhead fixo) | — |
| Qwen2.5-1.5B | 0,99 GB | 22 a 38 t/s | — |
| Qwen3.5-2B / Qwen3-1.7B | 1,28 GB | 18 a 30 t/s | 22 t/s medidos (Vulkan, máquina-irmã) |
| Qwen2.5-3B / Llama-3.2-3B | 1,93 a 2,02 GB | 12 a 20 t/s | cerca de 20 t/s (InsiderLLM, fraco) |
| Qwen3-4B / Gemma-3-4B / Qwen3.5-4B | 2,49 a 2,74 GB | 9 a 15 t/s | 15 a 18 t/s (MindStudio, fraco) |
| Qwen2.5-7B / Llama-3.1-8B | 4,7 a 4,9 GB | 5 a 8 t/s | 5,2 a 8,3 t/s (7B Q4_0, Iris Xe TGL, CPU e GPU) |

- [HIPÓTESE] Prefill na iGPU (Vulkan) do i5-1335U: o pp512 de 420 t/s do 2B no i7, escalado por 80/96 EU, dá cerca de 350 t/s, e cerca de 280 t/s em contexto de 4k. Escalando de forma grosseira pelo inverso dos parâmetros (sem contar os embeddings): 1,5B em cerca de 350 a 450 t/s, 3B em cerca de 200 a 250, 4B em cerca de 140 a 180 e 7 a 8B em cerca de 70 a 90. Este último bate com os 50 a 106 t/s medidos na Iris Xe TGL, mais antiga.
- [HIPÓTESE] Prefill só na CPU (sem fonte direta). A partir do Pi 5 (62 t/s com 1,7B), assumindo que o i5-1335U tem de 3 a 4 vezes o desempenho multi-thread do Pi 5 (premissa não verificada aqui): 1,5 a 2B em cerca de **150 a 250 t/s**, 3B em cerca de 80 a 140, 4B em cerca de 60 a 100 e 7 a 8B em cerca de 30 a 55. A incerteza é grande, e por isso o spike precisa medir o pp na CPU contra o Vulkan.
- [OPINIÃO] O prefill é onde a iGPU tem mais chance de ganhar da CPU, porque é limitado por computação e a Iris Xe tem cerca de 3,3 TFLOPS FP16 medidos. A geração deve ficar parecida nos dois caminhos, porque os dois dividem a mesma banda. Há ainda um segundo argumento a favor do Vulkan: com `-ngl 99 -t 2`, a CPU fica quase livre.
- [HIPÓTESE] Afinação de threads no 2P + 8E: para a geração, testar `-t` em 2, 4, 6, 8 e 10. Imagino que o ótimo fique entre 4 e 8, porque o limite é a banda e 2 P-cores sozinhos provavelmente não saturam o barramento; mas os relatos sobre núcleos híbridos mandam medir. Para o prefill (`--threads-batch`), mais threads tendem a ajudar.

### Gaps
- **Não encontrei benchmark só de CPU (llama-bench, pp e tg) publicado para i5-1335U, i7-1355U, i7-1365U, i5-1235U ou chips de 15 W parecidos**, nem resultados do localscore.ai para esses chips. Todas as velocidades de CPU desta nota são estimativas.
- O resultado Vulkan da máquina-irmã foi medido **no Linux (Mesa ANV)**. Não há dado do driver Vulkan da Intel no Windows, cujo desempenho pode ser diferente.
- Não há dado publicado do backend **SYCL** do llama.cpp nesta iGPU (Xe-LP, sem XMX), nem de OpenVINO.
- Não confirmei o ganho de AVX-VNNI nos kernels Q4_K/Q8 do llama.cpp em Raptor Lake.

## 4. Convivência com CP-SAT, navegador e Windows em 8 GB (sequencial vs concorrente, descarregar o modelo)

### Takeaway
A arquitetura natural do PyGridPlan já é sequencial (interpretar e depois resolver) e é a única viável. LLM e CP-SAT disputam a mesma banda de memória, os mesmos núcleos e o mesmo PL1 de 23 W. Os dois runtimes oferecem descarga automática do modelo: `keep_alive` no Ollama (padrão de 5 min, ou 0 para descarregar logo) e `--sleep-idle-seconds` no llama-server. Assim, o LLM só ocupa RAM durante a interpretação.

### Cited Findings
- [FATO] Ollama: "By default models are kept in memory for 5 minutes before being unloaded". O `keep_alive` da API sobrepõe o `OLLAMA_KEEP_ALIVE`. "'0' which will unload the model immediately after generating a response", e um número negativo mantém o modelo carregado. `OLLAMA_MAX_LOADED_MODELS` tem padrão 3 para inferência em CPU. `ollama ps` mostra "100% CPU" ou "100% GPU". — [Ollama FAQ](https://docs.ollama.com/faq)
- [FATO] llama-server: `--sleep-idle-seconds` (padrão -1, desativado). Depois do período ocioso, "the model and its associated memory (including the KV cache) are unloaded from RAM", e "Any new incoming task will automatically trigger the model to reload". `GET /health`, `/props`, `/models` e `/metrics` não acordam o servidor, e `GET /props` informa `is_sleeping`. No modo roteador, há `POST /models/unload` e `--models-memory-margin N`, que descarrega modelos por LRU até sobrar N MiB. "A model that is serving requests is never unloaded". — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] O llama-server tem cache de prompt em RAM (`-cram, --cache-ram`, em MiB) e `--cache-idle-slots`. Para JSON, aceita `-j/--json-schema`, `--grammar` e `response_format` no endpoint compatível com OpenAI. — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] Na máquina-irmã, a carga do modelo de 2B levou 1696 ms (no backend inferzero). — [inferzero issue #76](https://github.com/rizagp/inferzero/issues/76)

### Inferences
- [HIPÓTESE] Rodar em paralelo é ruim nos dois sentidos. O CP-SAT com 8 workers ocupa os núcleos e o prefill na CPU perderia desempenho na mesma proporção. A geração, limitada por banda, cairia por contenção no barramento, e o CP-SAT também perderia velocidade. Com o LLM no Vulkan, a CPU fica mais livre, mas a banda continua compartilhada.
- [HIPÓTESE] Orçamento de memória sequencial, com Qwen3.5-2B Q4_K_M e 4k: Windows + navegador (sem fonte; de 3 a 5 GB conforme o pedido) + Python/app + LLM com cerca de 1,6 a 1,8 GB, totalizando cerca de 5 a 7 GB de 7,7. Cabe, mas com pouca folga. Com um 4B (cerca de 3 a 3,5 GB), o total vai a cerca de 6,5 a 8,5 GB, o que traz **risco real de paginação** quando há outros apps abertos (a medição do coordenador viu só 0,6 GB livres). Com 7 a 9B, não cabe.
- [HIPÓTESE] Política recomendada: subir o servidor sob demanda ou mantê-lo dormindo, com `--sleep-idle-seconds` de 30 a 120 s ou `keep_alive` entre "0" e "1m". Isso libera a RAM antes de o CP-SAT começar. O custo de recarga deve ser de 1 a 3 s para 1 a 3 GB vindos do SSD, ou menos se o arquivo ainda estiver no cache de arquivos do Windows (standby list). O spike precisa medir isso.
- [HIPÓTESE] Há um conflito entre descarregar o modelo e o cache de prefixo. O prompt fixo (esquema e exemplos few-shot, cerca de 600 a 1200 tokens) poderia ficar em cache e reduzir o prefill a só a frase do usuário (100 a 400 tokens). Mas esse cache se perde quando o modelo é descarregado. Com prefill rápido (Vulkan num 2B), a perda pesa pouco; na CPU com 3 a 4B, pesa vários segundos.

### Gaps
- Não achei medição publicada de CP-SAT e llama.cpp rodando juntos em laptop.
- Falta uma fonte sobre o consumo base de RAM do Windows 11 com navegador.
- Não confirmei se o `--sleep-idle-seconds` libera também os buffers de GPU (Vulkan) no Windows. O README fala em "RAM".

## 5. Térmica e desempenho sustentado em chip U de 15 W

### Takeaway
O chassi Samsung sustenta cerca de 23 W (PL1), com picos de 39 W (PL2). Em carga longa, a CPU cai cerca de 19% em relação ao pico, e no modo Quiet ou na bateria perde de 15 a 25%. Uma interpretação curta (menos de 30 s) cabe quase toda dentro da janela de turbo, mas a geração seguida do CP-SAT empurra o sistema para o PL1.

### Cited Findings
- [FATO] PL2 de 39 W e PL1 de 23 W (dinâmico) em High Performance. No laço de Cinebench R15, a média foi de 1259 pontos contra um pico de 1547. Pela minha conta, isso dá cerca de 19% abaixo do pico; a fonte não informa o percentual. No modo Quiet, cerca de -15%. Na bateria em Balanced, "around 85 percent power". A unidade testada foi a NP750XFG (Galaxy Book3). — [Notebookcheck](https://www.notebookcheck.net/Samsung-Galaxy-Book3-review-The-Intel-Core-i5-1335U-celebrates-a-solid-premiere.723256.0.html)
- [FATO] Com a iGPU limitada a 1250 MHz no 750XGK, os testes registraram "Package Thermal Throttles: 0", e o clock da GPU se manteve entre cerca de 1240 e 1245 MHz. — [inferzero issue #76](https://github.com/rizagp/inferzero/issues/76)

### Inferences
- [HIPÓTESE] A geração de tokens depende pouco do clock (o limite é a banda), então deve sofrer menos com o PL1 que o prefill e o CP-SAT, que dependem de computação.
- [OPINIÃO] O spike precisa registrar o modo de energia (Samsung "High Performance" vs "Optimized", e tomada vs bateria) e rodar cada medição depois de um aquecimento. Senão, a primeira rodada (em turbo) vai parecer melhor do que o uso real.

### Gaps
- Não há medição de laço sustentado (Cinebench ou llama-bench) no **750XGK com i5-1335U** especificamente.

## 6. Latência fim a fim estimada (prompt de 800 a 1500 tokens, saída de cerca de 200) e veredito

### Takeaway
**Todos os números desta seção são estimativas [HIPÓTESE].** Elas combinam os insumos citados nas seções 2 e 3. Um modelo de **cerca de 2B (Qwen3.5-2B ou Qwen3-1.7B) em Q4_K_M é o ponto de equilíbrio realista**: cerca de 10 a 15 s por pedido, com 1,6 a 1,8 GB de RAM. Modelos de 3 a 4B são possíveis (cerca de 20 a 40 s, 2,4 a 3,5 GB), mas no limite. Modelos de 7 a 9B são inviáveis nesta máquina. Em todos os casos, a geração dos cerca de 200 tokens de saída domina o tempo, então **encurtar o JSON é a alavanca mais forte**.

### Cited Findings
- [FATO] Insumos usados: pp e tg medidos na máquina-irmã (2B: pp512 420, pp4096 339, tg 22 t/s) — [inferzero #76](https://github.com/rizagp/inferzero/issues/76); 7B na Iris Xe TGL (pp 42 a 106, tg 5,2 a 8,3) — [llama.cpp #10879](https://github.com/ggml-org/llama.cpp/discussions/10879); tamanhos de arquivo — repositórios do Hugging Face listados na seção 2; banda teórica de 68,2 GB/s — [CPU-Monkey](https://www.cpu-monkey.com/en/cpu-intel_core_i5_1335u).

### Inferences
- [HIPÓTESE] Fórmula: latência ≈ carga (se o modelo estiver frio) + N_prompt ÷ pp + N_saída ÷ tg. Usei N_prompt = 1200 (meio da faixa de 800 a 1500) e N_saída = 200, com o modelo já carregado e sem cache de prefixo:

| Modelo Q4_K_M | Caminho | pp (t/s) | tg (t/s) | Prefill 1200 tok | Geração 200 tok | **Total (quente)** |
|---|---|---|---|---|---|---|
| 1,5B (Qwen2.5-1.5B) | CPU | 150 a 250 | 22 a 38 | 4,8 a 8 s | 5,3 a 9 s | **cerca de 10 a 17 s** |
| 2B (Qwen3.5-2B) | iGPU Vulkan | 280 a 350 | 18 a 22 | 3,4 a 4,3 s | 9 a 11 s | **cerca de 12 a 15 s** |
| 2B (Qwen3.5-2B) | CPU | 130 a 220 | 18 a 30 | 5,5 a 9 s | 6,7 a 11 s | **cerca de 12 a 20 s** |
| 3B (Qwen2.5-3B / Llama-3.2-3B) | CPU | 80 a 140 | 12 a 20 | 8,6 a 15 s | 10 a 17 s | **cerca de 19 a 32 s** |
| 3B | iGPU Vulkan | 200 a 250 | 12 a 18 | 4,8 a 6 s | 11 a 17 s | **cerca de 16 a 23 s** |
| 4B (Qwen3-4B / Gemma-3-4B / Qwen3.5-4B) | CPU | 60 a 100 | 9 a 15 | 12 a 20 s | 13 a 22 s | **cerca de 25 a 42 s** |
| 4B | iGPU Vulkan | 140 a 180 | 9 a 14 | 6,7 a 8,6 s | 14 a 22 s | **cerca de 21 a 31 s** |
| 7 a 8B | CPU ou iGPU | 30 a 90 | 5 a 8 | 13 a 40 s | 25 a 40 s | **cerca de 40 a 80 s**, e não cabe em RAM com o resto |

  - Somar a carga a frio, de cerca de 1 a 3 s, se o modelo foi descarregado.
  - Com cache de prefixo (só cerca de 300 tokens novos), o prefill cai para cerca de 1 a 4 s em qualquer linha até 4B, e o total passa a ser quase só a geração.
  - Com saída de 100 tokens (JSON compacto, chaves curtas), a geração cai pela metade.
  - Se rodar junto com o CP-SAT, os valores podem dobrar ou ficar piores.
- [HIPÓTESE] Modelos com "modo de pensamento" (família Qwen3/3.5) precisam ter o raciocínio desligado no template. Cada token de pensamento custa o mesmo que um token de JSON, e algumas centenas deles dobrariam a latência. É uma inferência a partir da fórmula; o mecanismo exato de desligar não foi verificado nesta nota.
- [OPINIÃO] Veredito para "cabe em 8 GB com o resto, responde em segundos":
  - **Realista:** 0,8B a 2B em Q4_K_M (ou Q5_K_M/Q6_K no 0,8 a 1,5B, cujo custo extra de memória é pequeno). Ocupa de 0,6 a 1,8 GB, com cerca de 5 a 15 s por pedido. É o alvo do spike.
  - **Limítrofe:** 3 a 4B em Q4_K_M ou IQ4_XS. Ocupa de 2,4 a 3,5 GB, com cerca de 20 a 40 s. Só vale se a qualidade do JSON em pt-BR do 2B não bastar. Exige descarregar o modelo antes do CP-SAT e fechar apps.
  - **Inviável:** 7 a 9B. O arquivo sozinho já tem de 4,5 a 5,7 GB, e a latência passa de 40 s.
  - "Em segundos", entendido como menos de 5 s, **não é alcançável** com cerca de 200 tokens de saída em nenhum tamanho útil, porque exigiria tg acima de 40 t/s. "Dezenas de segundos" ou "cerca de 10 s" é a expectativa honesta. Ou o critério de sucesso do design precisa de um número explícito (por exemplo, P50 de 15 s ou menos), ou o JSON precisa encolher.

### Gaps
- Nenhuma das latências da tabela foi medida nesta máquina. As velocidades de CPU não têm benchmark publicado de um chip equivalente.
- A qualidade do JSON por tamanho de modelo está fora do escopo desta nota (ver as notas de modelos em português e de avaliação).

## 7. Spike de medição proposto (não executado)

### Takeaway
Um spike de meio dia com binários pré-compilados do llama.cpp (CPU e Vulkan para Windows) e de 3 a 4 modelos GGUF confirma ou derruba as estimativas. Ele deve medir pp e tg (llama-bench), o melhor número de threads, a RAM de pico, a latência fim a fim de um pedido real com o esquema JSON e o custo de recarga, com e sem o CP-SAT rodando.

### Cited Findings
- [FATO] Comando de referência da comunidade para comparação: `llama-bench -m <modelo>.gguf -ngl 100 -fa 0,1`, informando o hash do git e a string do Vulkan. — [llama.cpp #10879](https://github.com/ggml-org/llama.cpp/discussions/10879)
- [FATO] Flags configuradas na máquina-irmã: `-dev Vulkan0 -ngl 99 -t 2 -b 512 -ub 256 -fa 1 -ctk f16 -ctv f16`. — [inferzero #76](https://github.com/rizagp/inferzero/issues/76)
- [FATO] Flags do servidor que serão usadas: `-t`, `--threads-batch`, `-c`, `-ctk/-ctv`, `-fa`, `--load-mode`, `--sleep-idle-seconds`, `-j/--json-schema`, `-np`, `--cache-ram`. — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

### Inferences
- [OPINIÃO] **Modelos** (todos Q4_K_M, mais Q8_0 no 2B para comparar quantização): Qwen3.5-0.8B (0,53 GB), Qwen3.5-2B (1,28 GB), Qwen2.5-3B ou Llama-3.2-3B (cerca de 2,0 GB) e Qwen3.5-4B (2,74 GB) ou Gemma-3-4B (2,49 GB). A escolha final de família vem da nota de modelos em português. Não testar 7 a 9B, porque a memória já os descarta.
- [OPINIÃO] **Preparação:**
  1. Fechar apps e anotar a RAM livre (`Get-Counter '\Memory\Available MBytes'`).
  2. Ligar na tomada, no modo Samsung "High Performance", e anotar o modo.
  3. Baixar os zips oficiais de release (CPU x64 e Vulkan x64) para pastas separadas. Os nomes exatos dos assets precisam ser conferidos na página de releases.
  4. Anotar o build (`llama-cli --version`) e o driver da GPU.
- [OPINIÃO] **Passo 1. Varredura de threads na CPU** (pp e tg; `-r 3` para repetir):
  `llama-bench -m Qwen3.5-2B-Q4_K_M.gguf -ngl 0 -t 2,4,6,8,10 -p 512 -n 128 -r 3 -o md`
- [OPINIÃO] **Passo 2. CPU vs Vulkan** com o melhor `-t`:
  `llama-bench -m <modelo> -ngl 0,99 -fa 0,1 -t <melhor> -p 512,1024 -n 128 -r 3 -o md`
  Repetir para cada modelo. Usar `-pg 1200,200` (prefill seguido de geração) para simular o pedido real.
- [OPINIÃO] **Passo 3. KV quantizado** (só em Qwen3-4B, Gemma-3-4B ou Llama-3.2-3B):
  `llama-bench -m <modelo> -fa 1 -ctk f16,q8_0 -ctv f16,q8_0 -p 1024 -n 128`
- [OPINIÃO] **Passo 4. Latência fim a fim e RAM de pico:**
  - Subir `llama-server -m <modelo> -c 4096 -t <melhor> [-ngl 99] --sleep-idle-seconds 60 -np 1`.
  - Mandar de 5 a 10 frases de teste reais em pt-BR com o esquema JSON do PyGridPlan (`response_format` ou `json_schema`), medindo o tempo total no cliente Python.
  - O `timings` da resposta traz prompt_n, prompt_ms, predicted_n e predicted_ms. Confirmar no README se esse é o nome dos campos.
  - Em paralelo, ler `(Get-Process llama-server).PeakWorkingSet64` e `PrivateMemorySize64`, e as falhas de página duras (`Get-Counter '\Memory\Pages Input/sec'`).
  - Repetir o mesmo pedido para medir o efeito do cache de prefixo.
- [OPINIÃO] **Passo 5. Recarga:** esperar o servidor dormir (`GET /props` → `is_sleeping`) e medir o primeiro pedido seguinte (custo de recarga a frio ou morno).
- [OPINIÃO] **Passo 6. Convivência:** repetir um pedido do passo 4 com o CP-SAT (8 workers) gerando uma planta ao mesmo tempo. Registrar a perda de pp e tg e o tempo extra do CP-SAT. Isso confirma que o fluxo deve ser sequencial.
- [OPINIÃO] **Passo 7. Térmica:** rodar o passo 2 três vezes seguidas e uma vez na bateria, e anotar a queda.
- [OPINIÃO] **Planilha do spike** (uma linha por medição): modelo, quantização, backend, -t, -fa, ctk/ctv, pp512, pp1024, tg128, pg1200+200, RAM de pico (working set e privada), RAM livre antes e depois, falhas duras/s, latência fim a fim (fria, quente, com prefixo em cache), JSON válido (sim ou não), modo de energia, tomada ou bateria, build do llama.cpp, driver.
- [OPINIÃO] **Critério de decisão sugerido:** escolher o menor modelo que (a) produza JSON válido e correto no conjunto de frases de teste, (b) fique abaixo de cerca de 2 GB de RAM de pico e (c) tenha latência quente P50 de 15 s ou menos. Se o 2B falhar em (a), testar 3 a 4B e aceitar a latência maior.

### Gaps
- Os nomes exatos dos assets de release do llama.cpp para Windows (CPU/Vulkan) e os campos de `timings` não foram conferidos nesta pesquisa.
- O Ollama não documenta Vulkan no FAQ ([Ollama FAQ](https://docs.ollama.com/faq)), então usar a iGPU via Ollama no Windows não está confirmado. O spike com llama.cpp puro evita essa dependência.
