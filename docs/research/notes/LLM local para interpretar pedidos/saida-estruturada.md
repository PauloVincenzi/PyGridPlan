# Saída estruturada para LLMs locais: JSON Schema, gramáticas e decodificação restrita (estado em nov/2026)

> Nota de pesquisa (trilha M5, LLM local). Coletada em 2026-11-22/23. Rótulos: **[FATO]** = conferido na fonte citada; **[HIPÓTESE]** = plausível, não verificado; **[OPINIÃO]** = recomendação do pesquisador. Trechos de código são **ilustrativos, não testados**.
>
> Contexto do projeto: Python 3.13, Pydantic v2 (o venv do projeto tem pydantic 2.14.3), LLM de 1–4B quantizado rodando em CPU (i5-1335U, 8 GB). Um parser de regras roda primeiro; o LLM preenche só um esquema "delta" (relações e preferências), nunca a geometria.

## 1. llama.cpp: GBNF, conversão JSON Schema → gramática, `response_format` no llama-server e llguidance

### Takeaway
O llama.cpp converte um **subconjunto** de JSON Schema em gramática GBNF e mascara os tokens que violariam a gramática. Recursos que ele não suporta são **ignorados em silêncio**. `enum`, `required`, `minItems`/`maxItems`, `minLength`/`maxLength` e limites numéricos em `integer` funcionam. Limites em `number`, `$ref` aninhados, `anyOf` misturado com `properties`, `uniqueItems`, `not` e condicionais não funcionam. O llguidance (Microsoft) está integrado desde fev/2025, mas só com o flag de build `LLAMA_LLGUIDANCE`, que exige Rust.

### Cited Findings
**GBNF e conversão**
- [FATO] "GBNF (GGML BNF) is a format for defining formal grammars to constrain model outputs in `llama.cpp`"; tem suporte em `tools/cli`, `tools/completion` e `tools/server`. A sintaxe tem regras `nome ::= ...`, `|`, `()`, `* + ? {m} {m,} {m,n}`, classes `[...]` e a regra `root` como ponto de partida — [grammars/README.md](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
- [FATO] A GBNF também casa **tokens** específicos (`<think>`, `<[1000]>`) e aceita negação com `!` — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] **O esquema não entra no prompt:** "The JSON schema is only used to constrain the model output and is not injected into the prompt. The model has no visibility into the schema, so if you want it to understand the expected structure, describe it explicitly in your prompt. This does not apply to tool calling, where schemas are injected into the prompt." — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] **Armadilha de desempenho:** "Grammars currently have performance gotchas (see #4218)". Uma sequência `x? x? x? ... x?` é semanticamente correta, mas pode deixar a amostragem "extremely slow". O recomendado é `x{0,N}` — [grammars/README.md](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
- [FATO] A regra de espaço gerada pelo conversor é **limitada**: `space ::= | " " | "\n" [ \t]{0,20}` — [grammars/README.md](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)

**llama-server**
- [FATO] No endpoint `/completion`, os campos são `grammar` (GBNF) e `json_schema`. Exemplo da doc: `{"items": {"type": "string"}, "minItems": 10, "maxItems": 100}`. A doc diz que os testes em `tests/test-json-schema-to-grammar.cpp` são a referência do que é suportado — [tools/server/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md)
- [FATO] No endpoint compatível com OpenAI (`/v1/chat/completions`), `response_format` aceita `{"type": "json_object"}`, `{"type": "json_object", "schema": {...}}`, `{"type": "json_schema", "schema": {...}}` e o envelope OpenAI `{"type": "json_schema", "json_schema": {"name": ..., "strict": ..., "schema": {...}}}` — [tools/server/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md)
- [FATO] Uma gramática inválida enviada ao `/completion` devolve o erro "Failed to parse grammar" — [tools/server/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md)

**Palavras-chave de JSON Schema (conversor nativo)**
- [FATO] Lista oficial de limitações, citada da doc:
  - "`additionalProperties` defaults to `false` (produces faster grammars + reduces hallucinations)";
  - "Unsupported features are skipped silently. It is currently advised to use the command-line Python converter (see above) to see any warnings, and to inspect the resulting grammar / test it w/ llama-gbnf-validator";
  - "Can't mix `properties` w/ `anyOf` / `oneOf` in the same type" (#7703);
  - "prefixItems is broken (but items works)";
  - "`minimum`, `exclusiveMinimum`, `maximum`, `exclusiveMaximum`: only supported for `"type": "integer"` for now, not `number`";
  - "Nested `$ref`s are broken" (#8073);
  - "patterns must start with `^` and end with `$`";
  - "Remote `$ref`s not supported in the C++ version";
  - "`string` formats lack `uri`, `email`";
  - "No `patternProperties`".

  Fonte: [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] Recursos que "are unlikely to be implemented (hard and/or too slow to support w/ stateless grammars)": `uniqueItems`, `contains`/`minContains`, `$anchor`, `not` e `if`/`then`/`else`/`dependentSchemas` — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] O exemplo da própria doc usa um `$ref` de um nível (`"$ref": "#/$defs/QAPair"`), e o conversor C++ resolve `$ref` locais (`_resolve_ref`). O conversor também trata `enum` (`KIND_ENUM`) e faz a interseção de `enum` e de faixas numéricas dentro de `allOf`. Padrões não suportados geram o aviso "pattern ... is not supported ..., accepting any string" — [common/json-schema-to-grammar.cpp](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/common/json-schema-to-grammar.cpp); [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] `minItems: 10, maxItems: 100` vira a repetição `{9,99}` após o primeiro item, e `minLength`/`maxLength` vira `char{m,n}` — [grammars/README.md](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)

**llguidance no llama.cpp**
- [FATO] A integração está no llama.cpp desde 2025-02-01 (build b4613, PR #10224) — [llguidance README](https://github.com/guidance-ai/llguidance)
- [FATO] Ativação: `cmake -B build -DLLAMA_LLGUIDANCE=ON`. Exige "the Rust compiler and the `cargo` tool", o que "complicates the llama.cpp build process". Não há argumentos novos de linha de comando. Gramáticas que começam com `%llguidance` vão para o llguidance, e os pedidos de JSON Schema (por exemplo `-j`) também — [docs/llguidance.md](https://github.com/ggml-org/llama.cpp/blob/master/docs/llguidance.md)
- [FATO] O que o llguidance acrescenta:
  - separação entre lexer e parser ("GBNF lacks the concept of a lexer"; "the parser is engaged in under 0.5% of tokens");
  - CFG em uma variante de Lark;
  - máscara de token em ~50 μs de CPU em média para um tokenizer de 128k (p99 0,5 ms, p100 20 ms);
  - "Unsupported schemas result in an error message—no keywords are silently ignored".

  Fonte: [docs/llguidance.md](https://github.com/ggml-org/llama.cpp/blob/master/docs/llguidance.md)
- [FATO] Diferenças do modo llguidance:
  - "`additionalProperties` defaults to `true`, unlike current grammars";
  - "any whitespace is allowed";
  - a ordem de definição das propriedades é mantida mesmo quando elas são `required`;
  - os erros "are currently printed to `stderr`, and generation continues".

  Fonte: [docs/llguidance.md](https://github.com/ggml-org/llama.cpp/blob/master/docs/llguidance.md)

### Inferences
- [HIPÓTESE] O contraste da doc do llguidance ("Property definition order is kept, even when properties are required") sugere que o conversor nativo **reordena** as propriedades, com as `required` antes das opcionais. Na prática, um campo de "raciocínio" opcional pode acabar depois da resposta. A saída segura é declarar o campo de raciocínio **como `required` e como primeira propriedade**.
- [HIPÓTESE] Com llguidance, convém declarar `additionalProperties: false` explicitamente (o Pydantic já faz isso com `extra="forbid"`), porque o padrão do llguidance é o oposto do nativo.
- [OPINIÃO] Como os recursos não suportados são ignorados em silêncio no modo nativo, o projeto precisa de um teste que converta o esquema delta e verifique a gramática gerada, ou que valide uma amostra de saídas com Pydantic. O conversor Python em linha de comando mostra os avisos.

### Gaps
- Não verifiquei se os binários pré-compilados do llama.cpp (releases do GitHub, Windows/CPU) ou as wheels do llama-cpp-python vêm com `LLAMA_LLGUIDANCE` ligado. A API de releases do GitHub bloqueou por limite de requisições.
- A doc não diz como `const` é tratado. O código mostra o tratamento de `enum`; o de `const` não foi conferido.

## 2. Ollama: parâmetro `format` com JSON Schema

### Takeaway
O Ollama aceita `format: "json"` ou um JSON Schema completo (cliente Python: `format=Model.model_json_schema()`). No código atual (`main`, nov/2026), todos os modelos GGUF rodam como subprocesso do **llama-server original**, e o esquema é repassado ao campo `json_schema` do llama-server. Por isso o Ollama **herda os mesmos limites de palavras-chave do llama.cpp**.

### Cited Findings
- [FATO] "Provide a JSON schema to the `format` field". O padrão em Python é `format=Country.model_json_schema()` seguido de `Country.model_validate_json(response.message.content)` — [Ollama docs: Structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
- [FATO] Recomendações da doc: "It is ideal to also pass the JSON schema as a string in the prompt to ground the model's response"; temperatura baixa (ex.: `0`). A API compatível com OpenAI também aceita `response_format`. "Ollama's cloud currently does not support structured outputs" — [Ollama docs](https://docs.ollama.com/capabilities/structured-outputs)
- [FATO] O recurso foi anunciado em 2024-12-06. Dicas do anúncio: "Set the temperature to 0 for more deterministic output" e adicionar "return as JSON" ao prompt. Em "What's next" aparecem "Performance and accuracy improvements for structured outputs" e "GPU acceleration for sampling" — [Ollama blog](https://ollama.com/blog/structured-outputs)
- [FATO] O código do Ollama (`main`) diz: "All GGUF models are served via the upstream llama-server subprocess" — [llm/server.go](https://raw.githubusercontent.com/ollama/ollama/main/llm/server.go)
- [FATO] O comentário de cabeçalho diz: "For structured output, a JSON schema is passed to llama-server via its json_schema field and the "json" format as a builtin grammar via the grammar field. A format that applies after a response's thinking is sent as a grammar built around the GBNF llama-server itself derives from the schema." — [llm/llama_server.go](https://raw.githubusercontent.com/ollama/ollama/main/llm/llama_server.go)
- [FATO] O Ollama guarda em **cache LRU de 64 entradas** as gramáticas derivadas dos esquemas: "The conversion depends only on the llama-server build, which is fixed for the process, so entries are shared by every runner and never expire" (`schemaGrammarsSize = 64`) — [llm/llama_server.go](https://raw.githubusercontent.com/ollama/ollama/main/llm/llama_server.go)
- [FATO] Versão do cliente Python: `ollama` 0.6.3 (PyPI, 2026-09-29) — [PyPI ollama](https://pypi.org/project/ollama/)

### Inferences
- [HIPÓTESE] Modelos com "thinking" podem pensar livremente e só depois ter a resposta restringida (o comentário "format that applies after a response's thinking"). Isso pode recuperar parte da qualidade de raciocínio sem um campo `reasoning` no esquema, mas custa tokens e tempo em CPU.
- [HIPÓTESE] Esquemas dinâmicos diferentes a cada pedido (ids distintos) não aproveitam o cache entre pedidos. Para esquemas pequenos, o custo de conversão é desprezível (ver seção 4).
- [OPINIÃO] O Ollama acrescenta uma camada (daemon, gestão de modelos) sem acrescentar capacidade de restrição. Para controle fino (GBNF direto, llguidance, teste de gramática), o llama-server ou o llama-cpp-python dão acesso direto.

### Gaps
- O comportamento descrito é o do branch `main` lido em 2026-11-22. Não confirmei qual release estável já traz o "llama-server upstream para todo GGUF", porque a API de releases do GitHub bloqueou por limite de requisições. Versões antigas usavam o runner próprio com gramática do llama.cpp embutido (PR #2404), o que mostra a mesma família de limitações.
- Não achei, na doc oficial do Ollama, uma lista própria de palavras-chave suportadas.

## 3. Bibliotecas: Outlines, XGrammar, llguidance, lm-format-enforcer, Instructor, Guidance, llama-cpp-python

### Takeaway
Para llama.cpp/Ollama em CPU, as opções reais são três: (a) a restrição **nativa** do llama.cpp/Ollama (GBNF/json_schema); (b) o **llguidance** dentro do llama.cpp, com build próprio; (c) o **Outlines** ou o **Guidance** sobre o `llama-cpp-python`. O XGrammar não tem integração com llama.cpp ou Ollama. O Instructor não restringe a decodificação: ele valida e tenta de novo sobre a API.

### Cited Findings
**Versões no PyPI (consultadas em 2026-11-22)** — [PyPI JSON API](https://pypi.org/pypi/outlines/json)

| Pacote | Última versão | Data | Python |
|---|---|---|---|
| outlines | 1.3.3 | 2026-08-06 | >=3.10,<3.14 |
| outlines-core | 0.2.14 | 2026-01-09 | >=3.8 |
| xgrammar | 0.2.9 | 2026-11-09 | >=3.8,<4 |
| llguidance | 1.9.1 | 2026-09-30 | >=3.10 |
| lm-format-enforcer | 0.11.3 | 2025-08-24 | >=3.8,<4 |
| instructor | 1.17.0 | 2026-09-09 | >=3.9,<4 |
| guidance | 0.3.1 | 2026-02-03 | >=3.10 |
| llama-cpp-python | 0.3.37 | 2026-11-15 | >=3.8 |
| ollama | 0.6.3 | 2026-09-29 | >=3.8 |
| pydantic | 2.14.4 | 2026-11-19 | >=3.10 |

**Biblioteca por biblioteca**
- [FATO] **llama-cpp-python**: `create_chat_completion(response_format={"type": "json_object", "schema": {...}})` restringe a saída a um JSON Schema. O módulo `llama_cpp/llama_grammar.py` tem um porte Python próprio do conversor (`class SchemaConverter`, `json_schema_to_gbnf(schema, prop_order=...)`, `LlamaGrammar.from_json_schema`). Function calling: formatos `chatml-function-calling` e `functionary-v2` — [README llama-cpp-python](https://raw.githubusercontent.com/abetlen/llama-cpp-python/main/README.md); [llama_grammar.py](https://raw.githubusercontent.com/abetlen/llama-cpp-python/main/llama_cpp/llama_grammar.py)
- [FATO] **Outlines** (dottxt): integra com llama.cpp **via llama-cpp-python** (recebe um `llama_cpp.Llama`). "The `LlamaCpp` model supports all output types available in Outlines": Pydantic, `Literal`, `Regex`, `CFG`, tipos básicos. A doc também tem uma página para Ollama — [Outlines: llama.cpp](https://dottxt-ai.github.io/outlines/latest/features/models/llamacpp/)
- [FATO] **XGrammar**: "default structured generation backend for most LLM inference engines, including vLLM, SGLang, TensorRT-LLM, and MLC-LLM". Lista CPU e Windows entre as plataformas. O README **não menciona** llama.cpp nem Ollama. O XGrammar-2 saiu em 2026/05 — [XGrammar GitHub](https://github.com/mlc-ai/xgrammar)
- [FATO] **llguidance**: aceita "a large subset" de JSON Schema e CFG em formato Lark. Integrações: OpenAI Structured Outputs (2025-05-20), Chromium, vLLM, SGLang, llama.cpp e onnxruntime-genai. Sobre a máscara: "approximately 50μs of single-core CPU time for a tokenizer with 128k tokens ... There is no significant startup cost". "llama.cpp can be also used Guidance Python package" — [llguidance README](https://github.com/guidance-ai/llguidance)
- [FATO] **lm-format-enforcer**: diz funcionar com transformers, LangChain, LlamaIndex, llama.cpp (exemplo com llama-cpp-python), vLLM, TensorRT-LLM e ExLlamaV2. Limitações próprias: precisa de acesso aos logits por API Python, e o suporte a regex não é 100% — [README lm-format-enforcer](https://raw.githubusercontent.com/noamgat/lm-format-enforcer/main/README.md)
- [FATO] **Instructor** com Ollama: `instructor.from_provider("ollama/<modelo>")` com `response_model=<Pydantic>`. Os modos são JSON e TOOLS. Por padrão usa TOOLS em modelos com function calling (llama3.1, qwen2.5, mistral-nemo) e JSON nos outros. Tem `max_retries` com backoff e `timeout` total — [Instructor: Ollama](https://python.useinstructor.com/integrations/ollama/)
- [FATO] JSONSchemaBench (Llama-3.2-1B, cobertura empírica no GlaiveAI): Guidance 0,96, Llamacpp 0,95, Outlines 0,95, XGrammar 0,93, só o LM 0,90. Em esquemas difíceis o Outlines cai bastante (GitHub Hard: 0,03), sobretudo por timeouts — [JSONSchemaBench v3](https://arxiv.org/html/2501.10868v3)

### Inferences
- [HIPÓTESE] O lm-format-enforcer está com manutenção lenta: nenhuma release em ~15 meses (a última é de ago/2025). O Guidance não lança desde fev/2026, mas o llguidance (o motor) segue ativo (set/2026).
- [OPINIÃO] Para o PyGridPlan, nenhuma biblioteca extra é necessária no primeiro corte: a restrição nativa do llama.cpp/Ollama cobre o esquema delta (ver seção 4), e a validação fica com o Pydantic, que já é dependência. O Instructor só valeria pela retentativa, que é um laço de ~15 linhas escrito à mão. O Outlines (<3.14) prende o projeto ao llama-cpp-python. Seguindo a regra do CLAUDE.md, nenhuma dependência entra sem justificativa.

### Gaps
- A doc do Instructor não confirmou se a retentativa reenvia o erro de validação ao modelo ("reask"). Sei que é o comportamento conhecido da biblioteca, mas não verifiquei nesta rodada: **[HIPÓTESE]**.
- Não verifiquei se o Outlines 1.x usa o outlines-core como processador de logits no llama-cpp-python, nem qual é o custo dele em CPU.

## 4. Enums dinâmicos (catálogo de tipos de cômodo, ids presentes no pedido) e custo de compilação por pedido

### Takeaway
Sim: dá para gerar o modelo Pydantic **em tempo de execução** com `Literal[tuple_de_ids]` e `create_model`. O esquema resultante usa `enum`, que o llama.cpp suporta. Assim, `a` e `b` de uma relação só podem citar ids existentes. A compilação de um esquema pequeno custa dezenas de milissegundos no llama.cpp, desprezível perto da geração em CPU. Já o Outlines é bem mais lento para compilar.

### Cited Findings
- [FATO] Teste local (pydantic 2.14.3 do venv do projeto, sem LLM): `create_model` com `a=(Literal[('sala','cozinha','dorm1')], ...)` e `relations: tuple[Rel, ...]` com `max_length=10` gera `{"$defs": {"Rel": {"additionalProperties": false, "properties": {"a": {"enum": ["sala","cozinha","dorm1"], "type": "string"}, ..., "kind": {"enum": ["near","far"]}, "intensity": {"maximum": 5, "minimum": 1, "type": "integer"}}, "required": [...]}}, "properties": {"relations": {"items": {"$ref": "#/$defs/Rel"}, "maxItems": 10, "type": "array"}}, "additionalProperties": false, ...}`. Ou seja: só `enum`, `$ref` de um nível, `maxItems`, limites em `integer` e `additionalProperties: false`, tudo dentro do subconjunto suportado do llama.cpp — conferido contra o [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] Custo de compilação da gramática no JSONSchemaBench (Llama-3.1-8B, backend llama.cpp):

  | Motor | GlaiveAI (compila / por token) | GitHub Medium (compila) |
  |---|---|---|
  | Guidance (llguidance) | 0,00 s / 6,37 ms | 0,01 s |
  | Llamacpp | 0,05 s / 29,98 ms | 0,06 s |
  | Outlines | 3,48 s / 30,33 ms | 8,05 s |
  | Só o LM, sem restrição | — / 15,40 ms | — |

  No backend HF, o XGrammar compila em 0,12 s. Fonte: [JSONSchemaBench v3](https://arxiv.org/html/2501.10868v3)
- [FATO] O Ollama mantém em cache LRU (64) a gramática de cada esquema — [llm/llama_server.go](https://raw.githubusercontent.com/ollama/ollama/main/llm/llama_server.go)
- [FATO] A restrição nativa do llama.cpp não suporta `uniqueItems` nem regras entre campos ("hard and/or too slow to support w/ stateless grammars") — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)

### Inferences
- [HIPÓTESE] O tempo por token com gramática no llama.cpp (~30 ms contra ~15 ms sem restrição, no benchmark com GPU/8B) indica um **custo de amostragem por token** que, em CPU, se soma ao tempo do modelo. No i5 com modelo de 1–4B, a sobrecarga relativa deve ser menor, porque o modelo domina o tempo. Isso precisa de medição.
- [HIPÓTESE] Um `enum` com todos os tipos do catálogo (dezenas de valores) continua barato: vira uma alternância de literais na GBNF.
- [OPINIÃO] O enum de tipos só é útil se o LLM criar cômodos. No desenho atual (o LLM preenche só relações e preferências), basta o enum de **ids**. Os rótulos em português do catálogo ajudam o modelo a mapear "quarto do casal" → `dorm1` se o prompt listar `id: rótulo` para cada cômodo.

### Gaps
- Não converti o esquema delta em GBNF nem medi o tempo de compilação localmente. A execução do conversor Python baixado (`llama_grammar.py`) foi bloqueada pela política de permissões desta sessão. Próximo passo: rodar com o llama-cpp-python instalado ou com o llama-server (`json_schema` + `response_fields: ["generation_settings/grammar"]`, a mesma técnica que o Ollama usa para obter a gramática).

## 5. Efeitos na qualidade: a decodificação restrita piora ou melhora?

### Takeaway
A evidência mais rigorosa (JSONSchemaBench 2025, contraprova da dottxt) mostra que a restrição **não piora, e em geral melhora levemente**, a acurácia, **desde que** o prompt descreva o formato e o raciocínio venha antes da resposta. O resultado negativo de Tam et al. (2024) vem, em boa parte, de prompts inconsistentes e da confusão entre "JSON mode" e geração estruturada.

### Cited Findings
- [FATO] Tam et al. (arXiv 2408.02442, v1 de 2024-08-05, v3 de 2024-10-14): restrições de formato "significantly" reduziram o raciocínio, e restrições mais estritas causaram quedas maiores — [arXiv 2408.02442](https://arxiv.org/abs/2408.02442)
- [FATO] Contraprova da dottxt (Will Kurt, "Say What You Mean"; sem data na página). Problemas apontados: prompts diferentes entre os modos; prompts JSON que não especificavam o esquema; parser feito por LLM (Claude 3 Haiku); JSON mode tratado como geração estruturada. Com Llama-3-8B-Instruct, estruturado contra livre: GSM8K 0,78 × 0,77; Last Letter 0,77 × 0,73; Shuffled Objects 0,44 × 0,41 — [blog dottxt](https://blog.dottxt.ai/say-what-you-mean.html)
- [FATO] Recomendações da dottxt:
  - prompts iguais nos dois modos;
  - chat template correto do modelo;
  - um exemplo (one-shot) no formato exato;
  - **campo de raciocínio antes da resposta**;
  - mostrar no prompt o esquema exigido.

  Fonte: [blog dottxt](https://blog.dottxt.ai/say-what-you-mean.html)
- [FATO] JSONSchemaBench (Geng et al., arXiv 2501.10868, v3 de 2025-02-27; 10K esquemas reais), Llama-3.1-8B, acurácia em Last Letters / Shuffle Objects / GSM8K:

  | Configuração | Last Letters | Shuffle Objects | GSM8K |
  |---|---|---|---|
  | Só o LM | 50,7 | 52,6 | 80,1 |
  | XGrammar | 51,2 | 52,7 | 83,7 |
  | Llamacpp | 52,0 | 52,6 | 82,4 |
  | Outlines | 53,3 | 53,0 | 81,6 |
  | Guidance | 54,0 | 55,9 | 83,8 |

  Todos os motores restritos ficaram acima do baseline sem restrição. O ganho do Guidance é atribuído ao *token healing* — [JSONSchemaBench v3](https://arxiv.org/html/2501.10868v3)
- [FATO] Modos de falha no JSON Schema Test Suite (número de categorias com ao menos uma falha):

  | Falha | Llamacpp | Outlines | XGrammar | Guidance |
  |---|---|---|---|---|
  | Erro de compilação | 37 | 42 | 3 | 25 |
  | Restrição excessiva | 18 | 16 | 5 | 7 |
  | Restrição insuficiente | 7 | 8 | 38 | 1 |

  O XGrammar troca precisão por permissividade — [JSONSchemaBench v3](https://arxiv.org/html/2501.10868v3)
- [FATO] A doc do llama.cpp diz que o modelo **não vê** o esquema, e a do Ollama recomenda pôr o esquema no prompt — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md); [Ollama docs](https://docs.ollama.com/capabilities/structured-outputs)

### Inferences
- [HIPÓTESE] Os resultados positivos são de modelos de 8B em tarefas de raciocínio em inglês. Em modelos de 1–4B, a restrição tende a ajudar **mais** na validade sintática (o LM sozinho erra mais o formato) e o risco de piorar o raciocínio é baixo, porque a tarefa aqui é extração, não cálculo.
- [OPINIÃO] Ordem dos campos: primeiro um `notas` ou `raciocinio` curto (`maxLength` ~200, `required`, primeira propriedade), depois `relations`. Vale medir com e sem esse campo no conjunto de casos de teste: em CPU, cada token custa caro.
- [OPINIÃO] Chaves em português ou inglês: manter **chaves em inglês** (iguais ao modelo de domínio, sem camada de tradução) e **descrições e exemplos em português** no prompt. Os valores de enum (ids) são o que o modelo precisa ligar ao texto. Não há evidência medida; ver Gaps.

### Gaps
- Não encontrei estudo sobre o efeito do idioma das chaves (pt × en) na acurácia de modelos pequenos.
- Não encontrei avaliação específica de decodificação restrita em modelos de 1–4B em português.

## 6. O que a decodificação restrita não garante, e o laço de validação e reparo

### Takeaway
A gramática garante **sintaxe** e parte da estrutura (tipos, enums, tamanhos), mas não as regras entre campos: unicidade, ausência de autorrelação, pares repetidos e coerência com o texto. Também não garante JSON completo se a geração for cortada. Por isso o Pydantic continua sendo o validador final, com uma estratégia de reparo ou retentativa e um fallback determinístico.

### Cited Findings
- [FATO] `uniqueItems`, `not` e condicionais não são suportados no llama.cpp e "unlikely to be implemented" — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] Recursos não suportados são "skipped silently" no modo nativo; no llguidance, os erros vão para o `stderr` "and generation continues" — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md); [docs/llguidance.md](https://github.com/ggml-org/llama.cpp/blob/master/docs/llguidance.md)
- [FATO] Limites em `number` (ex.: `target_area_m2 > 0`, que o Pydantic emite como `exclusiveMinimum: 0` em `number`) **não** são aplicados pela gramática do llama.cpp — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] Uma doc de terceiros (Liquid AI) também observa que a gramática garante que a saída é parseável, não que os valores estão semanticamente corretos — [Liquid AI docs](https://docs.liquid.ai/deployment/on-device/llama-cpp/structured-output)
- [FATO] O padrão oficial do Ollama já termina em `Model.model_validate_json(...)` — [Ollama docs](https://docs.ollama.com/capabilities/structured-outputs)

### Inferences
- [HIPÓTESE] **JSON truncado:** se `max_tokens`/`num_predict` acabar antes do fecho, a saída fica incompleta. A gramática não força o fechamento antecipado. Mitigações: `maxItems` em toda lista, `maxLength` em toda string livre e um `max_tokens` com folga calculada a partir desses limites.
- [HIPÓTESE] **Laços de espaço em branco:** no conversor nativo, o espaço é limitado (`[ \t]{0,20}`). No llguidance, "any whitespace is allowed", e um modelo pequeno pode ficar emitindo espaços ou quebras até o limite de tokens. A defesa é o mesmo `max_tokens` e a detecção de saída sem `}` final.
- [HIPÓTESE] Strings sem `maxLength` (ex.: um `raciocinio` livre) são o caminho mais comum para repetição sem fim em modelos pequenos.
- [OPINIÃO] Laço sugerido: (1) gerar com o esquema dinâmico; (2) `Delta.model_validate_json`; (3) mesclar no `Request` e rodar o `model_validator` existente; (4) se falhar, **reparo determinístico primeiro** (descartar relações duplicadas ou autorrelações e registrar aviso), porque a maioria das violações de regras entre campos dá para corrigir sem o LLM; (5) só então **uma** retentativa com a mensagem de erro no prompt; (6) se falhar de novo, cair para "só regras" e avisar o usuário. Retentativas custam segundos em CPU.

### Gaps
- Não achei uma fonte primária que descreva o comportamento exato do llama-server quando `n_predict` corta uma gramática no meio (se ele marca o motivo de parada como `length`). A hipótese é que sim, como em qualquer geração.

## 7. Function calling / tool calling contra JSON Schema simples em modelos pequenos

### Takeaway
Para uma única extração estruturada, o JSON Schema em `response_format`/`format` é o caminho mais simples e o menos dependente do template do modelo. Tool calling acrescenta injeção do esquema no prompt e um parser específico por família de modelo, e só compensa se houver mais de uma ação.

### Cited Findings
- [FATO] No llama.cpp, em tool calling os esquemas **são injetados no prompt**; em `json_schema`/`response_format`, não — [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)
- [FATO] O llama-cpp-python implementa function calling por formatos específicos (`chatml-function-calling`, `functionary-v2`). O Functionary exige o tokenizer HF por "discrepancies between llama.cpp and HuggingFace's tokenizers" — [README llama-cpp-python](https://raw.githubusercontent.com/abetlen/llama-cpp-python/main/README.md)
- [FATO] O Instructor escolhe TOOLS para modelos treinados em function calling (llama3.1, qwen2.5, mistral-nemo) e JSON para os demais — [Instructor: Ollama](https://python.useinstructor.com/integrations/ollama/)
- [FATO] O Ollama distingue os caminhos de template ("Models with explicit Ollama renderers/parsers ... render prompts in Go and call /completion. Other GGUF chat models use llama-server's chat_template handling") — [llm/llama_server.go](https://raw.githubusercontent.com/ollama/ollama/main/llm/llama_server.go)

### Inferences
- [OPINIÃO] Usar `response_format`/`format` com o esquema delta **e** descrever o esquema no prompt (chaves, ids válidos com rótulos, 1–2 exemplos em português). Isso dá ao modelo o mesmo "contexto" que o tool calling daria, sem depender do parser de ferramentas de cada família.
- [HIPÓTESE] Modelos pequenos treinados em tool calling (ex.: Qwen) podem acertar melhor o formato no modo TOOLS. Com a restrição de gramática, porém, a vantagem de formato desaparece, e sobra só a questão semântica.

### Gaps
- Não encontrei benchmark comparando tool calling e JSON Schema restrito em modelos de 1–4B.

## 8. Padrão recomendado para o PyGridPlan (síntese)

### Takeaway
[OPINIÃO] Sequência recomendada: parser de regras → **esquema delta gerado por pedido** (enum de ids) → restrição nativa (llama-server `json_schema` ou Ollama `format`) + esquema descrito no prompt + temperatura 0 → validação Pydantic → reparo determinístico → no máximo uma retentativa → fallback "só regras". Sem bibliotecas novas no primeiro corte.

### Cited Findings
- [FATO] O esquema delta gerado com `Literal` dinâmico usa só palavras-chave suportadas pelo llama.cpp (teste local do esquema + [grammars/README.md](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md)).
- [FATO] A compilação de gramática no llama.cpp custa ~0,05 s em esquemas reais de porte médio — [JSONSchemaBench v3](https://arxiv.org/html/2501.10868v3)
- [FATO] A restrição não piorou a acurácia nas medições controladas — [JSONSchemaBench v3](https://arxiv.org/html/2501.10868v3); [blog dottxt](https://blog.dottxt.ai/say-what-you-mean.html)

### Inferences
- [OPINIÃO] Regras para o esquema delta:
  - nada de `number` com limites (validar no Pydantic);
  - nada de `anyOf` junto com `properties`;
  - nada de `X | None` desnecessário (vira `anyOf`);
  - `maxItems` em toda lista;
  - `maxLength` em toda string livre;
  - `extra="forbid"`;
  - campo de raciocínio opcional como `required` e primeiro, se a medição mostrar ganho.
- [OPINIÃO] Teste de registro: para cada caso de `tests/fixtures/`, verificar que o esquema delta passa no conversor sem avisos e que saídas sintéticas inválidas (id inexistente, relação duplicada) são pegas pelo Pydantic.
- [OPINIÃO] Esboço ilustrativo (**não testado**):

```python
# ILUSTRATIVO — não testado
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError, create_model

class _F(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

def delta_model(ids: tuple[str, ...]) -> type[BaseModel]:
    Id = Literal[ids]  # enum dinâmico: só ids do pedido
    Rel = create_model("Rel", __base__=_F,
        a=(Id, ...), b=(Id, ...),
        kind=(Literal["near", "far"], ...),
        intensity=(int, Field(ge=1, le=5)))
    return create_model("Delta", __base__=_F,
        relations=(tuple[Rel, ...], Field(max_length=2 * len(ids))))

# Ollama:      client.chat(model=..., messages=msgs, format=Delta.model_json_schema(), options={"temperature": 0})
# llama-server: POST /v1/chat/completions {"response_format": {"type": "json_schema", "schema": Delta.model_json_schema()}, ...}
# depois: Delta.model_validate_json(texto) -> mescla no Request -> model_validator -> reparo/retentativa/fallback
```

### Gaps
- Faltam medições locais: latência por pedido no i5-1335U com e sem gramática, taxa de JSON válido e acurácia semântica nos casos de teste. Essas medições ficam com a nota de avaliação ([avaliacao-com-casos-de-teste.md](avaliacao-com-casos-de-teste.md)).
- Não verifiquei se o llguidance vem ligado nos binários distribuídos (llama.cpp releases, Ollama, wheels do llama-cpp-python).
