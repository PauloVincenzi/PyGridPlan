# Motores de inferência local para um LLM pequeno embutido no PyGridPlan (Windows, offline, i5-1335U + Iris Xe, 8 GB)

> Notas de pesquisa coletadas em 2026-11-22. Versões e datas lidas na API JSON do PyPI, na API do GitHub (repositório e releases) e nas páginas oficiais, todas consultadas em 2026-11-22. Em 2026-11-23 a nota foi complementada com o padrão de `--port` e o `response_format` do llama-server, a doc de instalação do vLLM, o status do repositório onnxruntime-genai e os dados de Iris Xe da discussão #10879.
> Rótulos: **[FATO]** = conferido na fonte citada; **[HIPÓTESE]** = inferência a confirmar; **[OPINIÃO]** = julgamento do pesquisador.
> Limitação: a API do GitHub bloqueou por limite de requisições no meio da coleta, então alguns nomes de assets (wheels do llama-cpp-python no GitHub) não foram lidos.

## 1. llama.cpp (llama-server, llama-cli, libllama): versão, cadência, backends nesta máquina, binários Windows, servidor OpenAI, saída estruturada, licença

### Takeaway
O llama.cpp continua sendo o motor de referência. Publica várias builds por dia (b12635 em 2026-11-22), tem licença MIT e traz zips prontos para Windows x64 com CPU, Vulkan, SYCL e até OpenVINO. O `llama-server` é compatível com a API da OpenAI e restringe a saída por gramática (GBNF) ou por `json_schema`. Para este projeto, é a base mais madura e com menos dependências.

### Cited Findings
- [FATO] Release mais recente: `b12635`, publicada em 2026-11-22T23:55:51Z. Só em 2026-11-22 saíram ao menos 10 builds (b12624 a b12635), ou seja, a cadência é de várias builds por dia, com numeração `bNNNNN` e sem versão semântica — [GitHub releases](https://github.com/ggml-org/llama.cpp/releases); [API GitHub](https://api.github.com/repos/ggml-org/llama.cpp)
- [FATO] Licença MIT, repositório ativo (último push em 2026-11-22) com cerca de 136 mil estrelas — [API GitHub](https://api.github.com/repos/ggml-org/llama.cpp)
- [FATO] Assets Windows da b12635 que importam para esta máquina: `llama-b12635-bin-win-cpu-x64.zip`, `llama-b12635-bin-win-vulkan-x64.zip`, `llama-b12635-bin-win-sycl-x64.zip` e `llama-b12635-bin-win-openvino-2026.4.1-x64.zip`. Há também CUDA 12.4/13.5, ROCm 10.0 e OpenCL Adreno (ARM), que não servem aqui — [GitHub releases](https://github.com/ggml-org/llama.cpp/releases)
- [FATO] Pelo README, o `llama-server` oferece "OpenAI API compatible chat completions, responses, and embeddings routes" — [README do server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] Saída estruturada no servidor: o campo `json_schema` (amostragem guiada por gramática) e o campo `grammar` (gramática BNF; exemplos na pasta `grammars/`). Na CLI, os equivalentes são `-j, --json-schema SCHEMA` e `--grammar GRAMMAR`. O README não lista o que o JSON Schema suporta e remete a `test-json-schema-to-grammar.cpp` — [README do server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] Flags úteis para uso offline e embutido: `-m/--model FNAME`, `--offline` ("forces use of the cache and blocks network access"), `--host` com padrão no loopback 127.0.0.1 (aceita também socket UNIX `.sock`) e `--jinja` ativo por padrão para templates de chat. Existe um modo "router" multi-modelo (`--models-dir`, `--models-max`, padrão 4, `--models-memory-margin`, `--models-autoload`) — [README do server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] A tabela de opções diz "port to listen (default: 9931)". Historicamente o padrão era 8080; o app deve sempre passar `--port` explícito — [README do server (raw)](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md)
- [FATO] Em `/v1/chat/completions`, "The `response_format` parameter supports both plain JSON output" e aceita schema: `{"type": "json_object", "schema": {...}}`. A forma OpenAI `{"type": "json_schema", "json_schema": {"name": ..., "strict": ..., "schema": {...}}}` "is also accepted". O README não lista limitações e remete aos testes — [README do server (raw)](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md)
- [FATO] Comparação de backends em iGPU Intel (Panther Lake / Arc B390, Linux, MoE de 35B): Vulkan 624,5 t/s pp512 e 32,8 t/s tg128; SYCL 609,4 e 30,6; CPU 101,6 e 19,4. O backend OpenVINO do llama.cpp **falhou** nesse modelo, que tem arquitetura híbrida com Mamba2 e MTP. Conclusão do autor: "use Vulkan", que dispensa o oneAPI — [grigio.org, 2026-09-16](https://grigio.org/benchmarking-llama-cpp-backends-on-intel-panther-lake-vulkan-vs-sycl-vs-openvino-vs-cpu/)
- [FATO] A discussão oficial de desempenho SYCL tem como referência `llama-2-7b.Q4_0.gguf` com `llama-bench -fa 0,1`. Não há nenhuma entrada de Iris Xe, Raptor/Alder/Tiger Lake: as iGPUs presentes são Panther Lake Xe3, Arc 140T e Core Ultra 7 258V (Lunar Lake). Exemplo: Panther Lake Xe3 com Llama-3.2-1B-Instruct Q4_0 chega a cerca de 3433 t/s pp512 e 88,7 t/s tg128 (SYCL, fp16) — [Discussão #23313](https://github.com/ggml-org/llama.cpp/discussions/23313)
- [FATO] Existe uma discussão oficial de desempenho do backend Vulkan, mas não foi lida a fundo — [Discussão #10879](https://github.com/ggml-org/llama.cpp/discussions/10879)

### Inferences
- [HIPÓTESE] Na Iris Xe (Raptor Lake-U, Xe-LP), o Vulkan deve ser o backend de GPU mais prático no Windows: vem num zip pronto, usa o driver Intel que já traz Vulkan e não exige oneAPI. O SYCL exige o runtime oneAPI e, nos dados disponíveis, não supera o Vulkan em iGPU Intel.
- [HIPÓTESE] Com 8 GB compartilhados e um modelo pequeno (cerca de 1–4B em Q4), a vantagem da iGPU sobre a CPU deve aparecer sobretudo no processamento do prompt (prefill). A geração de tokens é limitada pela banda da LPDDR4x, que CPU e iGPU dividem. Como o pedido do PyGridPlan tem prompt grande (schema mais instruções) e saída curta (JSON), o prefill pesa. Precisa ser medido com `llama-bench` na máquina de referência.
- [OPINIÃO] O modo padrão recomendado é a build CPU AVX2, por ser a mais previsível. A build Vulkan fica como opção medida, porque drivers de iGPU no Windows são uma fonte de falhas.
- [HIPÓTESE] A cadência de várias builds por dia obriga a **fixar uma build** (ex.: b12635) no app, e não seguir a "latest".

### Gaps
- Não achei benchmark de llama.cpp em Raptor Lake-U nem em Windows. A Iris Xe só aparece em Tiger Lake/Linux em 2025 (ver seção 6). O post de zenvanriel.com traz só estimativas (6–10 t/s de geração para 7B Q4) e não medições — [zenvanriel.com](https://zenvanriel.com/ai-engineer-blog/local-ai-integrated-graphics-vulkan-offload/). É preciso medir localmente.
- Não li a lista de recursos de JSON Schema que **não** são suportados (ex.: `pattern`, `minItems` ou `$ref` complexos), que só aparece no arquivo de testes `test-json-schema-to-grammar.cpp`. É preciso testar o schema real do `Request` (enums de tipo de cômodo, `intensity` 1..5) contra o conversor.

## 2. llama-cpp-python: manutenção em 2026, wheels Python 3.13 no Windows, atraso em relação ao llama.cpp, bindings alternativos

### Takeaway
O llama-cpp-python está mantido e ativo: 0.3.37 saiu em 2026-11-15, com releases mensais ou mais frequentes. No PyPI, porém, só publica **sdist**, o que obriga a compilar com um toolchain C++ no Windows. As wheels Windows vêm de um índice próprio (`abetlen.github.io/.../whl/cpu`), em formato `py3-none-win_amd64`, que serve ao Python 3.13. As variantes Vulkan saem como releases no GitHub.

### Cited Findings
- [FATO] PyPI: última versão `0.3.37`, enviada em 2026-11-15. As anteriores: 0.3.36 (2026-10-01), 0.3.35 (2026-08-17), 0.3.34 (2026-07-12), 0.3.33 (2026-07-05) e 0.3.32 (2026-06-29). A 0.3.37 tem um único arquivo, `llama_cpp_python-0.3.37.tar.gz` (sdist, sem wheel). Licença MIT, `requires_python >=3.8` — [PyPI JSON](https://pypi.org/pypi/llama-cpp-python/json)
- [FATO] O repositório `abetlen/llama-cpp-python` não está arquivado: último push em 2026-11-22, cerca de 10,7 mil estrelas, MIT — [API GitHub](https://api.github.com/repos/abetlen/llama-cpp-python)
- [FATO] No GitHub, a v0.3.37 saiu em várias tags por backend no mesmo dia (15 nov): `v0.3.37-vulkan`, `-cu121` a `-cu132`, `-rocm72` e `-hip-radeon`. As notas dizem só "chore: bump version to 0.3.37 (#2415)", sem indicar o commit do llama.cpp embutido — [GitHub releases](https://github.com/abetlen/llama-cpp-python/releases)
- [FATO] O índice de wheels CPU tem `llama_cpp_python-0.3.36-py3-none-win_amd64.whl`, e o mesmo padrão vale da 0.3.32 à 0.3.36. A última wheel com tag `cp313-cp313-win_amd64` foi a 0.3.19. A 0.3.37 ainda não aparecia no índice — [índice whl/cpu](https://abetlen.github.io/llama-cpp-python/whl/cpu/llama-cpp-python/)
- [FATO] O pacote `llama-cpp-python-binary` está parado na 0.2.26 (2024-01-04) e não serve como alternativa — [PyPI JSON](https://pypi.org/pypi/llama-cpp-python-binary/json)

### Inferences
- [HIPÓTESE] A tag `py3-none` indica que a wheel não depende da ABI do CPython: a extensão carrega a `llama.dll` via ctypes. Por isso deve funcionar no Python 3.13. Confirmar com `pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu`.
- [HIPÓTESE] O atraso em relação ao llama.cpp é de semanas: as releases saem a cada 1–6 semanas, contra várias builds diárias do llama.cpp. Modelos de arquitetura muito nova podem não rodar até a próxima release. O commit exato do submódulo `vendor/llama.cpp` não foi conferido por causa do limite da API.
- [OPINIÃO] Para o PyGridPlan, rodar no mesmo processo (in-process) traz uma vantagem: não há porta nem processo extra. As desvantagens: um crash nativo (segfault no driver Vulkan, por exemplo) derruba o servidor Starlette inteiro, a instalação depende de um índice extra fora do PyPI e cresce o risco de compilação local. Rodar `llama-server` como subprocesso isola falhas e usa o binário oficial.

### Gaps
- Não li os nomes dos assets da release `v0.3.37-vulkan` (4 assets), então não sei se há wheel Windows Vulkan pronta.
- Não encontrei outro binding Python ativo e maduro para o llama.cpp. As alternativas reais citadas aqui são falar HTTP com o `llama-server` ou usar o cliente `ollama`. Uma busca dedicada não foi feita.
- Não verifiquei se o llama-cpp-python 0.3.37 expõe `response_format` com `json_schema` e gramáticas GBNF da mesma forma que as versões 0.2/0.3 anteriores. [HIPÓTESE] Sim, por continuidade da API (`LlamaGrammar`, `response_format`).

## 3. Ollama: versão, Windows, GPU Intel (Vulkan/IPEX), `format` com JSON Schema, overhead, serviço, cliente Python, licença, armazenamento, uso offline

### Takeaway
O Ollama (v0.40.17, 2026-11-10, MIT) roda nativamente no Windows como aplicativo em segundo plano, com API em `localhost:11434`. Tem saída estruturada via `format` com JSON Schema, integrada a Pydantic. O Vulkan, que cobre iGPUs, vem ativo por padrão quando o backend está instalado, e as releases recentes corrigem justamente iGPUs no Windows. O caminho IPEX-LLM para GPU Intel está morto: o repositório foi arquivado. Para um app de portfólio, exigir que o usuário instale o Ollama é aceitável, mas acrescenta um processo pesado e fora do controle do app.

### Cited Findings
- [FATO] Releases: v0.40.17 (2026-11-10), v0.40.16 (2026-11-09), v0.40.15 (2026-11-03) e v0.40.8 (21 out). A cadência é de várias releases por semana. Licença MIT, cerca de 188 mil estrelas — [GitHub releases](https://github.com/ollama/ollama/releases); [API GitHub](https://api.github.com/repos/ollama/ollama)
- [FATO] Na v0.40.17: "Vulkan now uses mmap for integrated GPUs, fixing `Failed to allocate pinned memory` load failures on shared-memory GPUs" e uma correção para modelos parcialmente descarregados em **iGPUs no Windows**, que falhavam ao alocar o KV cache. A v0.40.16 atualizou o llama.cpp embutido. A v0.40.17 menciona XGrammar pré-compilado nas builds de fonte — [GitHub releases](https://github.com/ollama/ollama/releases)
- [FATO] Doc de GPU: "Additional GPU support on Windows and Linux is provided via Vulkan"; "Vulkan is enabled by default when the backend is installed"; desliga-se com `OLLAMA_VULKAN=0` ou `GGML_VK_VISIBLE_DEVICES=-1`; "On Windows most GPU vendors drivers come bundled with Vulkan support". A página não detalha iGPUs Intel e não chama o Vulkan de experimental — [docs.ollama.com/gpu](https://docs.ollama.com/gpu)
- [FATO] Windows: requer Windows 10 22H2 ou mais novo, instala sem administrador no diretório do usuário (`OllamaSetup.exe /DIR=...`), "will run in the background", API em `http://localhost:11434`, pelo menos 4 GB de disco para os binários, modelos em `%HOMEPATH%\.ollama` (relocáveis via `OLLAMA_MODELS`). O zip `ollama-windows-amd64.zip` serve para "embedding Ollama in other apps" ou para rodar como serviço com `ollama serve` (ex.: NSSM). A página só cita GPUs NVIDIA e AMD como suportadas — [docs.ollama.com/windows](https://docs.ollama.com/windows)
- [FATO] Saída estruturada: `format` aceita `"json"` ou um JSON Schema. O exemplo em Python usa `Model.model_json_schema()` e depois `model_validate_json(...)`. Recomendações da doc: passar o schema também no prompt e usar temperatura 0. Também funciona pela API compatível com OpenAI (`response_format`). "Ollama's cloud currently does not support structured outputs" (só a nuvem; o local funciona) — [docs.ollama.com/capabilities/structured-outputs](https://docs.ollama.com/capabilities/structured-outputs)
- [FATO] Cliente Python `ollama` 0.6.3 (2026-09-29), MIT, `requires_python >=3.8` — [PyPI JSON](https://pypi.org/pypi/ollama/json)
- [FATO] `intel/ipex-llm` está **arquivado** (archived=true, último push em 2026-01-28). O fork `ipex-llm/ipex-llm` está parado desde abril de 2025 (v2.3.0-nightly, 2025-04-21) — [API GitHub intel/ipex-llm](https://api.github.com/repos/intel/ipex-llm); [API GitHub ipex-llm/ipex-llm](https://api.github.com/repos/ipex-llm/ipex-llm)

### Inferences
- [HIPÓTESE] Depois do `ollama pull`, o uso é offline: os modelos ficam em disco local e a API é local. Isso decorre da arquitetura descrita, mas não achei uma frase da doc que afirme "funciona sem internet".
- [HIPÓTESE] O Ollama embute o llama.cpp e soma a ele um runner, um gerenciador de modelos, um app de bandeja e um formato próprio de armazenamento (blobs, manifests). O overhead de RAM sobre o llama.cpp puro não foi medido em fonte alguma.
- [OPINIÃO] O Ollama é ótimo para o **desenvolvimento** (trocar de modelo em segundos, cliente Python pronto, `format` com Pydantic). Para **distribuir** o PyGridPlan, exigir a instalação do Ollama é aceitável num projeto de portfólio, mas tira do app o controle da versão do motor, que muda várias vezes por semana. Um adaptador fino (interface `Interpreter`) permite usar Ollama ou `llama-server` sem mudar o resto.
- [HIPÓTESE] O caminho "Ollama + IPEX-LLM" para GPU Intel, comum em tutoriais de 2024–2025, deve ser descartado: o projeto foi arquivado. O caminho atual para a Iris Xe no Ollama é o Vulkan.

### Gaps
- Overhead de memória do Ollama ocioso e carregado contra o `llama-server` puro: não encontrei fonte.
- Não há confirmação explícita, na doc, de que a Iris Xe é detectada e usada pelo Vulkan do Ollama no Windows. As notas da v0.40.17 sugerem uso de iGPU, mas sem citar modelo de GPU.
- Não verifiquei se o `format` do Ollama usa o mesmo conversor JSON Schema→GBNF do llama.cpp, ou XGrammar, nem quais palavras-chave do schema ele ignora.

## 4. Outros motores: LM Studio, OpenVINO GenAI/optimum-intel, ONNX Runtime GenAI (DirectML), MLC-LLM, llamafile, KoboldCpp, Jan, vLLM/SGLang, Transformers em CPU. Quais têm decodificação restrita?

### Takeaway
Fora do ecossistema GGUF, o **OpenVINO GenAI** é o candidato mais sério para esta máquina. É Intel, tem wheel cp313 para Windows, licença Apache-2.0, lista a Iris Xe como GPU suportada e oferece saída estruturada (JSON Schema, regex, EBNF). O **ONNX Runtime GenAI** também tem wheels cp313 e restrição via LLGuidance, mas a variante DirectML parou em junho de 2026. O **LM Studio** é proprietário e seus termos proíbem redistribuir e integrar fora das interfaces publicadas. KoboldCpp (AGPL-3.0), Jan e llamafile são invólucros do llama.cpp, sem vantagem para embutir. vLLM e SGLang são servidores para GPU de datacenter e não se encaixam aqui.

### Cited Findings
**OpenVINO GenAI / optimum-intel**
- [FATO] `openvino-genai` 2026.4.1.0 (2026-10-01). As anteriores: 2026.4.0.0 (2026-09-16), 2026.3.1.0 (2026-08-26) e 2026.3.0.0 (2026-08-04), com cadência mensal ou bimestral. Há wheel `openvino_genai-2026.4.1.0-2636-cp313-cp313-win_amd64.whl`. `requires_python >=3.10`, Apache-2.0 — [PyPI JSON](https://pypi.org/pypi/openvino-genai/json)
- [FATO] O README do PyPI tem uma seção "Structured Output generation": JSON, regex ou gramática EBNF via `StructuredOutputConfig(json_schema=...)`, com exemplo baseado num modelo Pydantic — [PyPI openvino-genai](https://pypi.org/project/openvino-genai/)
- [FATO] `StructuredOutputConfig` tem os campos `json_schema`, `grammar`, `regex` e `compound_grammar` — [API OpenVINO GenAI](https://docs.openvino.ai/2025/api/genai_api/_autosummary/openvino_genai.StructuredOutputConfig.html); [guia Structured Output](https://l-bat.github.io/openvino.genai/docs/guides/structured-output) (espelho num github.io pessoal; preferir a doc oficial)
- [FATO] Os requisitos do OpenVINO 2026 listam "Intel® Iris® Xe Graphics" entre as GPUs suportadas e Windows 10/11 64-bit. "The use of GPU requires drivers that are not included" — [requisitos de sistema OpenVINO 2026](https://docs.openvino.ai/2026/about-openvino/release-notes-openvino/system-requirements.html)
- [FATO] `optimum-intel` 2.2.0 (2026-09-17), Apache, é a ferramenta de exportação HF→OpenVINO IR. O release 2.0.0 saiu em 2026-06-10 — [PyPI JSON](https://pypi.org/pypi/optimum-intel/json)
- [FATO] O OpenVINO Model Server (OVMS) 2026 serve respostas estruturadas via `response_format` — [OVMS structured output 2026](https://docs.openvino.ai/2026/model-server/ovms_structured_output.html)
- [FATO] O llama.cpp ganhou um backend OpenVINO, com zip Windows pronto (`...-bin-win-openvino-2026.4.1-x64.zip`) — [GitHub releases llama.cpp](https://github.com/ggml-org/llama.cpp/releases). Num teste de Panther Lake ele falhou com um modelo híbrido (Mamba2/MTP), e o autor o considera imaturo para essas arquiteturas — [grigio.org](https://grigio.org/benchmarking-llama-cpp-backends-on-intel-panther-lake-vulkan-vs-sycl-vs-openvino-vs-cpu/). Um fórum descreve o backend como "half-baked" na comparação com o Vulkan (não lido a fundo) — [Level1Techs](https://forum.level1techs.com/t/llama-cpp-for-openvino-how-does-a-half-baked-build-stack-up-against-vulkan/248447)

**ONNX Runtime GenAI**
- [FATO] `onnxruntime-genai` 0.20.0 (2026-11-14). As anteriores: 0.19.0 (2026-11-03), 0.18.0 (2026-10-14) e 0.17.1 (2026-09-29). Há wheels `cp313-cp313-win_amd64`, licença MIT, e "GenAI wheels do not bundle ONNX Runtime binaries" — [PyPI JSON](https://pypi.org/pypi/onnxruntime-genai/json)
- [FATO] `onnxruntime-genai-directml`: última versão 0.14.1 (2026-06-02), com wheel cp313 win_amd64. Desde junho não acompanha o pacote principal (0.20.0) — [PyPI JSON](https://pypi.org/pypi/onnxruntime-genai-directml/json)
- [FATO] A restrição de saída usa LLGuidance: `GeneratorParams.set_guidance("json_schema", json.dumps(schema))`, e há também `lark_grammar`. Os nomes dos tipos variam entre os SDKs — [guia constrained decoding (espelho Mintlify)](https://www.mintlify.com/microsoft/onnxruntime-genai/guides/constrained-decoding); [llguidance](https://github.com/guidance-ai/llguidance)
- [FATO, conflitante] `github.com/microsoft/onnxruntime-genai` e `raw.githubusercontent.com/microsoft/onnxruntime-genai/main/README.md` responderam 404 em 2026-11-22 e de novo em 2026-11-23 (consulta direta com curl). Os metadados da 0.20.0 no PyPI não trazem `project_urls`. Já a doc oficial continua apontando esse repositório como fonte — [ONNX Runtime generate() API](https://onnxruntime.ai/docs/genai/). Existe também uma variante `onnxruntime-genai-winml` (Windows ML) — [PyPI onnxruntime-genai-winml 0.11.0](https://pypi.org/project/onnxruntime-genai-winml/0.11.0/)

**LM Studio**
- [FATO] Termos do app (versão de 23 de agosto de 2026): licença "solely for Your personal and / or internal business purposes". Proíbem "sublicense, distribute, sell", transferir a terceiros, "integrate the Software with other software other than through Company published interfaces" e engenharia reversa. O software é "exclusive property of Company" — [lmstudio.ai/app-terms](https://lmstudio.ai/app-terms)
- [FATO] Em julho de 2025 o uso no trabalho passou a ser gratuito, sem licença comercial separada — [blog LM Studio](https://www.lmstudio.ai/blog/free-for-work)
- [FATO] A CLI `lmstudio-ai/lms` é MIT — [API GitHub](https://api.github.com/repos/lmstudio-ai/lms)

**Invólucros do llama.cpp**
- [FATO] KoboldCpp v1.125.1 (2026-11-22), licença **AGPL-3.0** — [API GitHub](https://api.github.com/repos/LostRuins/koboldcpp)
- [FATO] Jan v0.8.8 (2026-10-28); a API do GitHub mostra licença "NOASSERTION" (não identificada automaticamente) — [API GitHub](https://api.github.com/repos/janhq/jan)
- [FATO] llamafile, hoje em `mozilla-ai/llamafile`: 0.10.6 (2026-09-15), também com licença "NOASSERTION" — [API GitHub](https://api.github.com/repos/mozilla-ai/llamafile)

**MLC-LLM, vLLM, SGLang**
- [FATO] `mlc-ai/mlc-llm` tem atividade (push em 2026-11-21, Apache-2.0), mas a única release no GitHub é `v0.1.dev0` (2023-04-29); a distribuição é feita por outros canais — [API GitHub](https://api.github.com/repos/mlc-ai/mlc-llm)
- [FATO] vLLM v0.34.0 (2026-11-16) e SGLang v0.5.23 (2026-11-02), ambos Apache-2.0 — [API GitHub vLLM](https://api.github.com/repos/vllm-project/vllm); [API GitHub SGLang](https://api.github.com/repos/sgl-project/sglang)
- [FATO] A página de instalação do vLLM lista como hardware NVIDIA CUDA, AMD ROCm, Intel XPU e Apple Silicon (vLLM-Metal) nas GPUs, e x86, AArch64, Apple silicon e S390X nas CPUs. **Não menciona Windows** — [docs vLLM installation](https://docs.vllm.ai/en/latest/getting_started/installation/)

**Bibliotecas de decodificação restrita (para Transformers e outros)**
- [FATO] `xgrammar` 0.2.9 (2026-11-09), Apache-2.0, com wheels cp313 win_amd64 — [PyPI JSON](https://pypi.org/pypi/xgrammar/json)
- [FATO] `outlines` 1.3.3 (2026-08-06), Apache-2.0, `requires_python <3.14,>=3.10` (serve ao 3.13, mas ainda não ao 3.14) — [PyPI JSON](https://pypi.org/pypi/outlines/json)

### Inferences
- [HIPÓTESE] Saída estruturada **nativa**: llama.cpp (GBNF e json_schema), llama-cpp-python, Ollama (`format`), OpenVINO GenAI (`StructuredOutputConfig`), ONNX Runtime GenAI (LLGuidance) e OVMS. KoboldCpp, Jan e llamafile herdam a gramática do llama.cpp; o grau de exposição varia e não foi verificado. vLLM e SGLang também suportam (XGrammar), mas não servem para esta máquina. Transformers em CPU pode ser restringido com xgrammar ou outlines.
- [HIPÓTESE] vLLM e SGLang não servem para o PyGridPlan. A doc do vLLM não cita Windows entre as plataformas (só o caminho de CPU x86, provavelmente em Linux ou WSL), e os dois são servidores de alto throughput com dependência de PyTorch. Para o SGLang não li a doc de instalação.
- [OPINIÃO] O LM Studio fica descartado como motor embutido, por ser proprietário e proibir redistribuição e integração fora das interfaces publicadas. Só serviria como ferramenta pessoal do desenvolvedor para testar modelos.
- [OPINIÃO] O KoboldCpp, sob AGPL-3.0, contaminaria a distribuição se fosse embutido. Jan e llamafile não acrescentam nada ao `llama-server` oficial.
- [HIPÓTESE] O ONNX Runtime GenAI com DirectML (que usaria a Iris Xe) parece em descontinuação: o pacote DirectML parou na 0.14.1 enquanto o principal chegou à 0.20.0. Não achei anúncio oficial. O repositório no GitHub dá 404, talvez porque mudou de lugar. Os dois sinais são de risco.
- [OPINIÃO] O OpenVINO GenAI é a alternativa a avaliar se a medição mostrar que o llama.cpp Vulkan é ruim na Iris Xe: é do próprio fabricante, tem Python nativo e JSON Schema. O custo: formato IR específico, conversão com optimum-intel (dependência pesada só na exportação) e wheels grandes.
- [OPINIÃO] Transformers + PyTorch em CPU é pesado demais (dependências de GB, sem quantização eficiente em CPU) para 8 GB. É útil só como referência de pesquisa.

### Gaps
- Não sei a razão do 404 no repositório onnxruntime-genai (renomeação, privatização ou falha). A doc oficial ainda aponta para ele, e o pacote PyPI segue publicando (0.20.0 em 2026-11-14).
- Não confirmei se o `StructuredOutputConfig` do OpenVINO GenAI funciona no dispositivo `"GPU"`, ou só em `"CPU"`. Os exemplos usam CPU.
- Licenças exatas de Jan e llamafile (a API retornou NOASSERTION). [HIPÓTESE] O llamafile historicamente é Apache-2.0 e o Jan AGPL/Apache; é preciso conferir o arquivo LICENSE.
- Transformers em CPU: não houve busca dedicada (versão e desempenho).
- MLC-LLM: não verifiquei o canal de distribuição atual (wheels nightly) nem o suporte a Windows/Vulkan em 2026.

## 5. Distribuição: como o app Python embarca e lança o motor offline; formato de modelo; tamanho e local de armazenamento

### Takeaway
Há três caminhos realistas. (a) **Subprocesso do `llama-server`**, um zip oficial fixado numa build, com loopback, `--offline` e porta escolhida pelo app, consumido via HTTP compatível com OpenAI. (b) **In-process com llama-cpp-python**, a partir de uma wheel `py3-none-win_amd64` do índice próprio. (c) **Exigir o Ollama instalado** e falar com `localhost:11434`. O formato é GGUF para (a), (b) e (c), OpenVINO IR para o OpenVINO GenAI e ONNX para o ORT GenAI.

### Cited Findings
- [FATO] Zips oficiais Windows por backend (cpu, vulkan, sycl, openvino) a cada build — [GitHub releases llama.cpp](https://github.com/ggml-org/llama.cpp/releases)
- [FATO] O `llama-server` escuta por padrão em 127.0.0.1, tem `--offline` para bloquear rede e carrega o modelo por caminho (`-m`) ou por variável de ambiente (`LLAMA_ARG_MODEL`) — [README do server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [FATO] As wheels CPU do llama-cpp-python saem do índice `https://abetlen.github.io/llama-cpp-python/whl/cpu`, fora do PyPI; no PyPI só há sdist — [índice whl/cpu](https://abetlen.github.io/llama-cpp-python/whl/cpu/llama-cpp-python/); [PyPI JSON](https://pypi.org/pypi/llama-cpp-python/json)
- [FATO] O Ollama oferece um zip standalone para "embedding Ollama in other apps" e guarda os modelos em `%HOMEPATH%\.ollama` (ou `OLLAMA_MODELS`) — [docs.ollama.com/windows](https://docs.ollama.com/windows)
- [FATO] OpenVINO GenAI e ONNX Runtime GenAI distribuem wheels cp313 win_amd64 no PyPI — [PyPI openvino-genai](https://pypi.org/pypi/openvino-genai/json); [PyPI onnxruntime-genai](https://pypi.org/pypi/onnxruntime-genai/json)

### Inferences
- [OPINIÃO] Recomendação para o M5: começar com **Ollama no desenvolvimento** (troca rápida de modelos para escolher um) e uma **interface única no código** (o cliente HTTP compatível com OpenAI ou com o `format` do Ollama). Na entrega, preferir o **`llama-server` como subprocesso** gerido pelo app Starlette: iniciar no primeiro uso, health-check em `/health`, porta livre escolhida pelo app, encerrar junto com o app. Assim o motor fica fixado e isolado, o servidor sobrevive a um crash nativo, não há compilação e não é preciso instalar nada externo.
- [HIPÓTESE] Local de armazenamento: o modelo GGUF fica em `%LOCALAPPDATA%\PyGridPlan\models\` (ou na pasta `out/` ou numa pasta de dados do usuário, fora do git), com o hash SHA-256 registrado em `data/` para garantir que é o arquivo esperado. O download é feito uma única vez, manualmente ou por script, e depois o app roda com `--offline`.
- [HIPÓTESE] Tamanho: um modelo de 1–4B parâmetros em Q4_K_M ocupa da ordem de 1–3 GB em GGUF. É uma estimativa por regra de bolso (cerca de 4,5–5 bits por peso), sem fonte nesta coleta; quem pesquisa modelos deve confirmar com os tamanhos reais dos arquivos no Hugging Face. Em 8 GB compartilhados (sistema, navegador e iGPU), um modelo acima de cerca de 4B tende a forçar swap.
- [HIPÓTESE] O OpenVINO IR e o ONNX exigem uma etapa de conversão, ou modelos já convertidos (ex.: repositórios OpenVINO/ e onnx-community no Hugging Face), e prendem o app a um runtime específico. O GGUF tem o maior ecossistema e serve a todos os invólucros do llama.cpp.

### Gaps
- Tamanhos exatos de GGUF e IR dos modelos candidatos: fora deste escopo (pesquisa de modelos).
- Não verifiquei o tamanho dos zips do llama.cpp (cpu/vulkan) nem das wheels do OpenVINO GenAI e do ORT GenAI, porque o limite da API impediu ler os tamanhos dos assets.

## 6. Comparações medidas (t/s, prefill, RAM): llama.cpp CPU × Vulkan × SYCL × OpenVINO em Iris Xe / Raptor Lake-U ou similares

### Takeaway
Não há benchmark público confiável em **Raptor Lake-U** com as versões de 2026. O dado mais próximo é a **Iris Xe do Tiger Lake (i7-1185G7, Linux, 2025)**: Llama-2 7B Q4_0 com Vulkan rende cerca de 42–106 t/s de prefill (pp512) e 6–8 t/s de geração; na CPU, 30–73 de prefill e 5–10 de geração. Ou seja, na Iris Xe o ganho do Vulkan aparece no prefill (cerca de 1,4×) e quase não aparece na geração, que às vezes é até pior que na CPU. Os demais dados medidos são de iGPUs Intel mais novas (Panther Lake, Arrow Lake, Lunar Lake), e mostram de forma consistente: Vulkan ≥ SYCL, iGPU com prefill cerca de 6× melhor que a CPU e geração cerca de 1,7× melhor (no MoE de 35B), e o backend OpenVINO do llama.cpp ainda imaturo. Para a máquina de referência, é obrigatório medir localmente com `llama-bench`.

### Cited Findings
- [FATO] Core Ultra X7 358H (Panther Lake, Arc B390 integrada, 12 Xe3, cerca de 32 GB LPDDR5, Linux CachyOS, Mesa ANV 26.2.2), Qwen3.6-35B-A3B Q4_K_M, KV q4_0, FA ligado, 16 threads: **Vulkan 624,5 pp512 / 32,8 tg128**; SYCL 609,4 / 30,6 (com Level Zero: 614,9 / 30,9); **CPU 101,6 / 19,4**; OpenVINO falhou. Memória: modelo de cerca de 22 GiB, KV f16 estimado em cerca de 10 GiB; "context size is the hidden bottleneck" em UMA — [grigio.org, 2026-09-16](https://grigio.org/benchmarking-llama-cpp-backends-on-intel-panther-lake-vulkan-vs-sycl-vs-openvino-vs-cpu/)
- [FATO] Intel B390, mesmo autor, Vulkan contra SYCL em Qwen3 35B-A3B: Vulkan 758 t/s pp512 e 30,9 tg, SYCL 439 e 28,3 (dado lido só no snippet da busca, não na página) — [grigio.org](https://grigio.org/llama-cpp-0-9-x-vulkan-vs-sycl-benchmark-on-intel-b390-with-qwen3-35b-a3b-mtp-ud-q4_k_m/)
- [FATO] SYCL na discussão oficial: Core Ultra 7 258V, llama-2-7b Q4_0, 535,6 pp512 / 24,6 tg128 (Ubuntu 26.04, 2026-06-12); Panther Lake Xe3 com Llama-3.2-1B Q4_0, 3433 / 88,7. Nenhuma entrada de Iris Xe — [Discussão #23313](https://github.com/ggml-org/llama.cpp/discussions/23313)
- [FATO] **Iris Xe (TGL GT2, i7-1185G7, Tiger Lake)** na discussão oficial de Vulkan, todas em Arch Linux com Mesa e Llama-2 7B Q4_0. Em 2025-01-10 (build 4459), Vulkan ngl 100 deu **42,0 pp512 / 7,3 tg128**, e CPU ngl 0 com 4 threads deu 30,5 / 9,9. Em 2025-02-05, Vulkan deu cerca de 50,9 / 7,9–8,3. Em 2025-06-01 (build 5568), Vulkan ngl 100 deu **106,2 pp512 / 5,9 tg128**, e CPU ngl 0 deu 73,3 / 5,2. Procedimento: `llama-bench -m llama-2-7b.Q4_0.gguf -ngl 100 -fa 0,1`. A própria discussão diz que, em iGPU, "memory speed and channel count strongly affect inference speed" — [Discussão #10879](https://github.com/ggml-org/llama.cpp/discussions/10879)
- [FATO] As estimativas de 6–10 t/s de geração para 7B Q4 em iGPU com Vulkan são declaradamente estimativas, não medições — [zenvanriel.com](https://zenvanriel.com/ai-engineer-blog/local-ai-integrated-graphics-vulkan-offload/)

### Inferences
- [HIPÓTESE] A Iris Xe do i5-1335U (Xe-LP, geração anterior a Xe2 e Xe3) com LPDDR4x-4267 tem banda e computação bem menores que a Panther Lake com LPDDR5. Os números absolutos acima são **teto otimista**, não expectativa. A proporção "iGPU muito melhor no prefill, pouco melhor na geração" deve valer em parte.
- [HIPÓTESE] Para o caso do PyGridPlan (prompt de cerca de 1–2 mil tokens com schema e exemplos, saída de cerca de 100–300 tokens de JSON, modelo de 1–4B Q4), o prefill domina a latência na CPU. O Vulkan pode reduzir bastante o tempo até o primeiro token. A gramática JSON acrescenta custo por token na amostragem.
- [OPINIÃO] Plano de medição sugerido para a máquina de referência: `llama-bench -m <modelo.gguf> -p 512,1024 -n 128 -t 4,8,12` com os zips cpu e vulkan da mesma build. Registrar pp, tg e RAM de pico (Gerenciador de Tarefas ou `psutil`), e repetir uma vez com o OpenVINO GenAI (CPU e GPU) no mesmo modelo convertido. Os threads importam: com 2 P-cores e 8 E-cores, usar todos os 12 threads pode piorar em relação a 4–8.

### Gaps
- Nenhuma medição pública de llama.cpp (CPU, Vulkan ou SYCL) nem de OpenVINO GenAI em Iris Xe ou Raptor Lake-U com software de 2026.
- Nenhuma medição de RAM de pico para modelos de 1–4B nesses backends.
- As entradas de Iris Xe na #10879 são de 2025, em Linux/Mesa, com Tiger Lake (não Raptor Lake) e modelo de 7B. Não há dados em Windows com driver Intel nem com modelos de 1–4B. [HIPÓTESE] Para modelos de 1–4B, os t/s escalam aproximadamente com o inverso do tamanho do arquivo: um 3B Q4 daria uns 2× o tg de um 7B. Isso precisa ser medido.
