# Arquitetura de app local (motor Python + UI TypeScript no navegador): servidor, eventos ao vivo, build do front-end e distribuição

Pesquisa feita em 2026-11-22. Convenção: **FATO** = verificado em fonte primária citada (PyPI/npm JSON, código-fonte, documentação oficial); **HIPÓTESE/OPINIÃO** = inferência do pesquisador, a validar. As versões e datas de PyPI/npm foram lidas diretamente das APIs JSON (`https://pypi.org/pypi/<pacote>/json`, `https://registry.npmjs.org/<pacote>`) em 2026-11-22.

## 1. Servidor: stdlib vs Starlette vs FastAPI (e alternativas)

### Takeaway
A biblioteca padrão não tem WebSocket nem roteamento/validação e a própria documentação desaconselha `http.server` em produção. A pilha mínima realista é **Starlette + uvicorn** (dependências diretas: `anyio`, `click`, `h11`; mais `websockets` ou `wsproto` se usar WebSocket). O **FastAPI** acrescenta pydantic, que o projeto já usa, e tem SSE nativo desde a 0.135.0, mas agora também puxa `opentelemetry-api` como dependência obrigatória.

### Cited Findings
**Versões atuais (FATO)**
- FATO: FastAPI **0.165.0**, publicado em 2026-11-18. Requer Python >=3.11. Dependências obrigatórias: `starlette>=1.6.0`, `anyio>=4.1.0`, `pydantic>=2.9.0`, `typing-extensions>=4.8.0`, `typing-inspection>=0.4.2`, `annotated-doc>=0.0.2` e `opentelemetry-api>=1.44.0`. — [PyPI fastapi JSON](https://pypi.org/pypi/fastapi/json)
- FATO: o ritmo de lançamento do FastAPI é muito alto: 0.162.3 a 0.165.0 saíram entre 2026-11-10 e 2026-11-18. A série segue em 0.x, e a 0.137.0 (2026-06-14) traz uma seção "Breaking Changes". — [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/)
- FATO: Starlette **1.10.0**, publicado em 2026-10-24. Requer Python >=3.11. Dependências obrigatórias: só `anyio>=4.0.0,<5` (e `typing-extensions`, apenas para Python <3.13). O extra `full` traz httpx, jinja2, python-multipart, itsdangerous, pyyaml e opentelemetry-api. A Starlette **1.0.0** saiu em 2026-03-22. — [PyPI starlette JSON](https://pypi.org/pypi/starlette/json)
- FATO: uvicorn **0.54.0**, publicado em 2026-09-25. Requer Python >=3.10. Dependências obrigatórias: `click>=7.0` e `h11>=0.8`. — [PyPI uvicorn JSON](https://pypi.org/pypi/uvicorn/json)
- FATO: `websockets` 17.4 (2026-10-30), sem dependências; `wsproto` 1.3.2 (2025-11-20), que depende de `h11`. — [PyPI websockets](https://pypi.org/pypi/websockets/json); [PyPI wsproto](https://pypi.org/pypi/wsproto/json)
- FATO: anyio 4.16.0 (2026-11-01); pydantic 2.14.4 (2026-11-19, com `pydantic-core==2.50.5`); httpx 0.28.1 (2024-12-06). — [PyPI anyio](https://pypi.org/pypi/anyio/json); [PyPI pydantic](https://pypi.org/pypi/pydantic/json); [PyPI httpx](https://pypi.org/pypi/httpx/json)
- FATO: o extra `full` da Starlette lista ao mesmo tempo `httpx>=0.27,<0.29` e `httpx2>=2.0.0`. O pacote `httpx2` aparece de novo nas dependências do NiceGUI 4.0.0. Esse é o cliente usado pelo `TestClient`. — [PyPI starlette JSON](https://pypi.org/pypi/starlette/json); [PyPI nicegui JSON](https://pypi.org/pypi/nicegui/json)

**Biblioteca padrão (FATO)**
- FATO: a documentação do `http.server` avisa: "`http.server` is not recommended for production. It only implements basic security checks." — [docs.python.org http.server](https://docs.python.org/3/library/http.server.html)
- FATO: a página do `http.server` não menciona WebSocket. `ThreadingHTTPServer` existe desde o 3.7. O padrão é HTTP/1.0, e com `protocol_version='HTTP/1.1'` cada resposta precisa de um `Content-Length` exato. — [docs.python.org http.server](https://docs.python.org/3/library/http.server.html)
- HIPÓTESE (alta confiança): nenhum módulo da stdlib (`http.server`, `wsgiref`, `asyncio`) implementa o handshake nem o enquadramento WebSocket (RFC 6455). `asyncio` só oferece streams TCP. Fazer WebSocket "na mão" significaria implementar o protocolo. Uma resposta SSE com `http.server` é viável: basta escrever `text/event-stream` no `wfile` sem `Content-Length`, com HTTP/1.0 ou fechando a conexão ao final.

**O que cada opção oferece**
- FATO: o SSE do FastAPI foi "Added in FastAPI 0.135.0", e a 0.135.0 saiu em 2026-03-01. A importação é `from fastapi.sse import EventSourceResponse, ServerSentEvent`. O uso é `response_class=EventSourceResponse` numa rota com `yield`. Os itens tipados (`AsyncIterable[Item]`) são validados e serializados pelo pydantic. Geradores síncronos são aceitos sem bloquear o loop. `ServerSentEvent` aceita `event`, `id`, `retry` e `comment`. Há ping de keep-alive a cada 15 s e cabeçalhos `Cache-Control: no-cache` e `X-Accel-Buffering: no`. `Last-Event-ID` pode ser lido como `Header()`. O SSE funciona com qualquer método, inclusive POST (citado para MCP). — [FastAPI SSE tutorial](https://fastapi.tiangolo.com/tutorial/server-sent-events/); [PyPI fastapi JSON (data da 0.135.0)](https://pypi.org/pypi/fastapi/json)
- FATO: o pacote de terceiros `sse-starlette` está na **3.7.0** (2026-11-07) e depende de `starlette>=0.49.1` e `anyio>=4.7.0`. — [PyPI sse-starlette](https://pypi.org/pypi/sse-starlette/json)
- FATO: Litestar 2.25.0 (2026-10-18) tem uma árvore de dependências bem maior: msgspec, polyfactory, rich, rich-click, httpx, multidict, pyyaml, litestar-htmx etc. — [PyPI litestar](https://pypi.org/pypi/litestar/json)
- FATO: aiohttp 3.14.5 (2026-10-11) depende de aiohappyeyeballs, aiosignal, attrs, frozenlist, multidict, propcache e yarl. — [PyPI aiohttp](https://pypi.org/pypi/aiohttp/json)
- FATO: Flask 3.1.3 (2026-02-19). `flask-sock` está na 0.7.0, cuja última versão é de 2023-10-02. — [PyPI flask](https://pypi.org/pypi/flask/json); [PyPI flask-sock](https://pypi.org/pypi/flask-sock/json)
- FATO: Quart 0.23.1 (2026-08-29) requer Python >=3.13 e depende de flask, hypercorn, aiofiles, werkzeug, jinja2 etc. — [PyPI quart](https://pypi.org/pypi/quart/json)
- HIPÓTESE/conhecimento prévio (não reverificado nesta rodada): a Starlette traz roteamento (`Route`, `WebSocketRoute`, `Mount`), `StaticFiles`, `StreamingResponse`, WebSocket nativo, `TestClient` (com `websocket_connect`, exigindo httpx) e `TrustedHostMiddleware`. A Starlette não tem uma classe SSE própria; por isso existe o `sse-starlette`. O FastAPI herda tudo isso e acrescenta injeção de dependências, validação pydantic de corpo e parâmetros e OpenAPI. Confirmar em [starlette.dev](https://www.starlette.dev/).
- HIPÓTESE (a verificar): o uvicorn só fala HTTP/1.1 e WebSocket (sem HTTP/2). O suporte a WebSocket exige `websockets` ou `wsproto` instalados (por exemplo, `uvicorn[standard]`).

### Inferences
- HIPÓTESE/OPINIÃO: a pilha mínima com SSE é `starlette` + `uvicorn` (cerca de 4 pacotes novos: starlette, anyio, idna via anyio, click, h11). Com WebSocket, acrescenta-se `websockets` (sem dependências). O FastAPI acrescenta 4 ou 5 pacotes pequenos mais `opentelemetry-api` e dá validação pydantic automática nas rotas. Como o PyGridPlan já valida comandos com pydantic numa camada própria (compartilhada com testes e MCP), o ganho do FastAPI se resume a OpenAPI e ao SSE embutido. Com Starlette, a validação seria uma chamada explícita `Model.model_validate(await request.json())`, o que é coerente com a camada de comandos ser a fonte da verdade.
- OPINIÃO: a stdlib pura é viável para POST e SSE, mas obriga a reimplementar roteamento, arquivos estáticos e testes, sem WebSocket. Fere "simplicidade" no sentido do código, mesmo poupando dependências.
- OPINIÃO: a cadência 0.x do FastAPI (vários lançamentos por semana, com breaking changes ocasionais) pede fixar a versão no `pyproject.toml`.

### Gaps
- Não verifiquei nesta rodada as notas detalhadas da Starlette 1.x (por exemplo, se a 1.x acrescentou uma resposta SSE nativa) nem o changelog do uvicorn 0.54.
- Não medi o tamanho em disco de cada pilha instalada.

## 2. Console ao vivo: WebSocket vs SSE vs polling

### Takeaway
SSE resolve "eventos para baixo" com reconexão automática nativa e `Last-Event-ID`. Os comandos sobem por HTTP POST. É o mesmo padrão do transporte Streamable HTTP do MCP e o que o Gradio adotou na v4. WebSocket dá um canal único bidirecional, mas exige reconexão e reenvio feitos à mão.

### Cited Findings
- FATO (MDN): SSE "is a one-way connection, so you can't send events from a client to a server". Por padrão, se a conexão cai, o navegador reconecta. O campo `retry` define o tempo de reconexão em ms. O campo `id` define o `lastEventId`. — [MDN Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
- FATO (MDN): sem HTTP/2, o SSE tem limite de **6 conexões por navegador + domínio**, somando todas as abas. Com HTTP/2, o limite é negociado (padrão de 100 streams). — [MDN Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
- FATO (FastAPI): "When a browser reconnects after a connection drop, it sends the last received `id` in the `Last-Event-ID` header". — [FastAPI SSE tutorial](https://fastapi.tiangolo.com/tutorial/server-sent-events/)
- FATO (MCP spec 2025-06-18): o transporte Streamable HTTP usa **POST para cada mensagem JSON-RPC do cliente**. O servidor responde com JSON ou abre um stream SSE. GET abre um SSE para notificações do servidor. Os eventos SSE podem levar `id`, e o cliente retoma com `Last-Event-ID`. Desconexão "SHOULD NOT be interpreted as the client cancelling its request"; para cancelar, o cliente envia uma notificação explícita (`CancelledNotification`). — [MCP Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- FATO (MCP): o stdio é o outro transporte padrão, e os clientes "SHOULD support stdio whenever possible". — [MCP Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- FATO (Gradio): no Gradio 4.0, a fila passou de WebSockets para SSE: "SSE means everything is served over HTTP and has better device support and better scaling than websockets". O changelog do cliente JS registra "Swap websockets for SSE" (#6069). — [Hugging Face post (abidlabs)](https://huggingface.co/posts/abidlabs/528535313265224); [Gradio client CHANGELOG (espelho)](https://huggingface.co/spaces/mindmime/gradio/raw/main/client/js/CHANGELOG.md)
- FATO (Gradio, relato da equipe): depois da migração para SSE, chatbots com streaming passaram a ter atraso, que a equipe atribuiu à prioridade de eventos no navegador. O resumo que obtive não deixa claro qual tipo de evento tem prioridade menor; tratar como incerto. — [Hugging Face post (abidlabs)](https://huggingface.co/posts/abidlabs/540156790542613)
- HIPÓTESE (conhecimento geral, não confirmado na página da MDN lida): `EventSource` só faz GET e não aceita cabeçalhos customizados. Autenticar por cabeçalho exige `fetch()` com leitura de stream, ou token em cookie/query.

### Inferences
- OPINIÃO: para o PyGridPlan, "comandos via POST `/api/commands/<nome>` + eventos via SSE `/api/events`" encaixa bem no desenho de comandos nomeados e validados. Cada comando é uma requisição testável isoladamente com `TestClient`. O formato espelha o futuro MCP (POST + SSE, ou stdio), o que permite reutilizar o mesmo despachante. Os eventos com `id` sequencial e um buffer circular no servidor dão reconexão sem perda de linhas do console.
- OPINIÃO: WebSocket único com JSON-RPC 2.0 também atende (comando sobe, resposta e notificações descem). Os custos: reconexão, correlação de ids e reenvio feitos à mão; testes um pouco mais verbosos; e o cancelamento precisaria de uma mensagem explícita de qualquer forma.
- OPINIÃO: o limite de 6 conexões HTTP/1.1 só incomoda com muitas abas abertas no mesmo `localhost:porta`. Para uma única aba, é irrelevante. Uma regra simples (um stream por aba) basta.
- OPINIÃO: polling (por exemplo, `GET /api/events?after=<id>` a cada 250–500 ms) é o mais simples e funciona até com a stdlib, mas dá latência visível e tráfego ocioso. Serve como fallback, não como desenho principal.

### Gaps
- Não encontrei medição publicada de latência SSE vs WebSocket em localhost.
- Não verifiquei a página de referência `EventSource` na MDN sobre métodos e cabeçalhos.

## 3. CP-SAT (CPU-bound) dentro de um servidor assíncrono

### Takeaway
No OR-Tools 9.15, `solve` **libera o GIL** durante a busca e os callbacks **readquirem o GIL** na thread C++ do solver. Por isso, rodar o solve numa thread (`asyncio.to_thread` / `run_in_executor`) não congela o loop. `stop_search()` pode ser chamado de outra thread e protege o acesso ao wrapper com um `threading.Lock`. Usar um processo separado só se justifica para isolamento ou cancelamento "duro".

### Cited Findings
- FATO (código-fonte v9.15): o método `solve` do `SolveWrapper` (pybind11) executa `::py::gil_scoped_release release; return solve_wrapper->Solve(*model_proto);`, ou seja, solta o GIL durante toda a resolução. — [or-tools v9.15 cp_model_helper.cc (raw)](https://raw.githubusercontent.com/google/or-tools/v9.15/ortools/sat/python/cp_model_helper.cc)
- FATO (código-fonte v9.15): o callback de solução (`PySolutionCallback::OnSolutionCallback`) é uma trampolina que faz `::py::gil_scoped_acquire acquire;` antes de chamar o Python. Os callbacks de log e de best bound fazem o mesmo. Se o callback Python lançar exceção, o wrapper guarda a exceção, chama `StopSearch()` e relança a exceção no `solve`. Comentário no código: "We assume this code is serialized as the gil is held." — [or-tools v9.15 cp_model_helper.cc (raw)](https://raw.githubusercontent.com/google/or-tools/v9.15/ortools/sat/python/cp_model_helper.cc)
- FATO (código-fonte v9.15): `CpSolver.stop_search()` tem a docstring "Stops the current search asynchronously" e chama `self.__solve_wrapper.stop_search()` sob `self.__lock` (`threading.Lock`). `CpSolver` também expõe `log_callback` e `best_bound_callback`. `CpSolverSolutionCallback.stop_search()` existe e chama `StopSearch()`. — [or-tools v9.15 cp_model.py (raw)](https://raw.githubusercontent.com/google/or-tools/v9.15/ortools/sat/python/cp_model.py)
- FATO: ortools **9.15.6755**, publicado em 2026-01-14, requer Python >=3.9. Dependências obrigatórias: absl-py, numpy>=2.0.2, **pandas>=2.0.0**, protobuf>=6.33.1,<6.34, typing-extensions e immutabledict. — [PyPI ortools](https://pypi.org/pypi/ortools/json)
- FATO (histórico): num fio de 2019, um usuário relatou que, com o wrapper SWIG, o interpretador parecia pausado durante o solve e que um `StopSearch` vindo de outra thread só agia na solução seguinte. A resposta foi que "adding threading support to SWIG wrapper" resolvia. O pybind11 entrou na interface Python na v9.3. — [Busca: fios or-tools-discuss e notas de versão](https://developers.google.com/optimization/support/release_notes); [or-tools-discuss: terminating search](https://groups.google.com/g/or-tools-discuss/c/IQVyGoJTe9w)
- FATO (docs Python, conhecimento estável): `asyncio.to_thread()` (3.9+) roda uma função numa thread do executor padrão. `loop.call_soon_threadsafe()` é a forma segura de agendar algo no loop a partir de outra thread. `asyncio.Queue` **não** é thread-safe. No Windows, `multiprocessing` usa o método de início `spawn`, que exige objetos serializáveis (pickle) e a guarda `if __name__ == "__main__"`. — [asyncio event loop: call_soon_threadsafe](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.call_soon_threadsafe); [asyncio.to_thread](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread); [multiprocessing: contexts and start methods](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods)

### Inferences
- HIPÓTESE (forte, apoiada no código): o padrão é: um handler `async` recebe `stage.generate`, captura `loop = asyncio.get_running_loop()` e faz `await asyncio.to_thread(run_solve, ...)`. Dentro de `on_solution_callback` (thread C++ do CP-SAT, com o GIL), o callback extrai uma solução leve e chama `loop.call_soon_threadsafe(queue.put_nowait, evento)`. Uma tarefa assíncrona consome a fila e publica o evento no SSE/WS. O callback deve ser curto, porque segura o GIL e as soluções são serializadas.
- HIPÓTESE: o cancelamento chama `solver.stop_search()` a partir do handler `stage.cancel` (outra thread ou o loop), o que é suportado pelo lock. Ao mudar entradas no meio do solve, o fluxo é cancelar, esperar o `to_thread` retornar e reiniciar com uma nova geração (um id de execução descarta eventos atrasados).
- HIPÓTESE: com 8 workers do CP-SAT numa máquina de 12 threads, o loop asyncio continua responsivo, porque o GIL fica livre na maior parte do tempo. Pode haver contenção breve quando muitas soluções chegam em rajada.
- OPINIÃO: `ProcessPoolExecutor` só vale se for preciso (a) matar o solve à força, quando `stop_search` demora (há relatos no fórum de parada lenta), (b) isolar falhas nativas ou (c) rodar solves em paralelo. Os custos no Windows: `spawn` reimporta ortools, numpy e pandas por processo (memória e tempo de partida); o modelo e os eventos precisam cruzar o processo (`multiprocessing.Queue`); e a meta de 8 GB de RAM fica mais apertada. A thread é o ponto de partida mais simples.
- OPINIÃO: rodar o `solve` direto numa corrotina sem thread bloquearia o loop, mesmo com o GIL liberado, porque a chamada é síncrona.

### Gaps
- Não encontrei documentação oficial em prosa sobre a liberação do GIL; a evidência é o código-fonte v9.15 (primário). Falta um teste empírico local (um `stop_search` vindo de outra thread enquanto um servidor responde a requisições).
- Não verifiquei a latência real do `stop_search` com 8 workers no modelo do PyGridPlan.

## 4. Build do front-end e framework de UI

### Takeaway
Vite está na major 8 (desde 2026-03-12), agora baseado em Rolldown. O TypeScript estável é o **7.0.2** (2026-07-08), distribuído com binários nativos por plataforma. O padrão "proxy do Vite em dev + `vite build` para arquivos estáticos servidos pelo Python em produção" é direto. A escolha de framework de UI é uma troca, não uma necessidade.

### Cited Findings
- FATO: Vite **8.3.8** (2026-11-11) é a versão mais recente. A 8.0.0 saiu em 2026-03-12 e a 7.0.0 em 2025-06-24. As dependências da 8.x são `rolldown`, `lightningcss`, `postcss`, `picomatch` e `tinyglobby`. Engines: Node `^20.19.0 || >=22.12.0`. Há uma beta 8.4.0-beta.1. — [npm vite](https://registry.npmjs.org/vite)
- FATO: rolldown 1.3.3 (2026-11-18). — [npm rolldown](https://registry.npmjs.org/rolldown)
- FATO: TypeScript **7.0.2** (2026-07-08) é o `latest`. A linha 6.0 chegou à 6.0.3 (a 6.0.2 é de 2026-03-23). As tags `beta` 7.1.0-beta e `next` 7.1.0-dev.20261121.1 estão ativas. O pacote 7.0.2 depende de binários por plataforma (`@typescript/typescript-win32-x64` etc.). — [npm typescript](https://registry.npmjs.org/typescript)
- FATO (contexto): o TypeScript 7 é o port nativo do compilador anunciado pela Microsoft ("Project Corsa"). — [TypeScript blog: A 10x Faster TypeScript](https://devblogs.microsoft.com/typescript/typescript-native-port/)
- FATO: esbuild 0.28.2 (2026-08-08); Bun 1.4.5 (pacote npm `bun`, 2026-11-19). — [npm esbuild](https://registry.npmjs.org/esbuild); [npm bun](https://registry.npmjs.org/bun)
- FATO (versões de frameworks em 2026-11-22): Preact 11.2.0 (2026-11-06); Svelte 5.59.1 (2026-11-20); Solid 2.0.3 (2026-11-19); Lit 3.3.3 (2026-05-14); React 19.3.1 (2026-10-14). — [npm preact](https://registry.npmjs.org/preact); [npm svelte](https://registry.npmjs.org/svelte); [npm solid-js](https://registry.npmjs.org/solid-js); [npm lit](https://registry.npmjs.org/lit); [npm react](https://registry.npmjs.org/react)
- HIPÓTESE/conhecimento prévio (não reverificado nesta rodada): o Vite tem `server.proxy` para encaminhar `/api` (inclusive WebSocket com `ws: true`) ao backend em dev, e um guia de "Backend Integration" com manifesto. O `vite build` gera `dist/` com HTML, JS e CSS com hash. — [Vite server options](https://vite.dev/config/server-options); [Vite backend integration](https://vite.dev/guide/backend-integration)

### Inferences
- OPINIÃO: as opções em ordem de complexidade:
  - (a) `tsc` só para checar tipos + ES modules nativos servidos direto, sem bundler. Funciona em navegadores modernos, mas sem HMR, sem minificação e com import maps para dependências.
  - (b) esbuild via CLI: um binário, build em milissegundos, sem dev server com HMR completo.
  - (c) Vite: dev server com HMR, proxy para o Python e build pronto. Puxa Rolldown, lightningcss e postcss (só em dev; nada vai para o pacote Python).
  - (d) Bun: runtime e bundler alternativos, mais um runtime a instalar.
  Node é necessário em (a), (c) e no TypeScript 7 de qualquer forma, salvo com Bun.
- OPINIÃO: o TypeScript 7 é nativo e rápido. Se algum plugin ou ferramenta depender da API JS do compilador 6.x, há risco de incompatibilidade (hipótese a verificar quando o `typescript-lsp` for instalado no M2).
- OPINIÃO (trocas de framework para um app centrado em canvas com painéis laterais):
  - **Vanilla TS**: zero dependências. O canvas e o desenho são imperativos de qualquer jeito. O custo está nos painéis com formulários (site, cômodos), na árvore de alternativas e no console, que exigem sincronizar estado e DOM à mão.
  - **Lit** (Web Components): pequeno, próximo do padrão e bom para painéis isolados.
  - **Preact / Solid**: JSX, baixo peso e reatividade fina (Solid, signals). Adequados para formulário e lista de eventos.
  - **Svelte 5**: compila, com runes. Exige o plugin do Vite.
  - **React 19**: o maior ecossistema e o maior peso; é exagero para o escopo.
  Em todos, o canvas fica fora do framework (um componente "host" que só recebe o modelo).
- OPINIÃO: o build de produção é copiado para dentro do pacote Python (por exemplo, `src/pygridplan/web_dist/`) e servido por `StaticFiles`. Assim o usuário final não precisa de Node.

### Gaps
- Não reverifiquei o texto atual das páginas `server.proxy` e "Backend Integration" do Vite 8.
- Não encontrei comparação publicada de tamanho de bundle entre frameworks com versões de 2026.

## 5. Distribuição e execução local; segurança do servidor local

### Takeaway
O caminho mais simples é um pacote Python com os assets do front-end embutidos e um console script que sobe o uvicorn em `127.0.0.1` e abre o navegador (`webbrowser`). Isso é instalável com `pip`, `pipx` ou `uv tool`. PyInstaller/Nuitka (executável único) e pywebview/Tauri/Electron (janela nativa) são camadas opcionais posteriores. Um servidor em localhost **precisa** checar `Host`/`Origin` por causa do DNS rebinding.

### Cited Findings
- FATO: uv 0.13.9 (2026-11-17); pipx 1.18.19 (2026-11-17); hatchling 1.33.0 (2026-10-28). — [PyPI uv](https://pypi.org/pypi/uv/json); [PyPI pipx](https://pypi.org/pypi/pipx/json); [PyPI hatchling](https://pypi.org/pypi/hatchling/json)
- FATO: PyInstaller 6.22.3 (2026-09-12), com `requires_python <3.16,>=3.8`, ou seja, cobre o Python 3.13. Nuitka 4.3.5 (2026-11-08). — [PyPI pyinstaller](https://pypi.org/pypi/pyinstaller/json); [PyPI nuitka](https://pypi.org/pypi/nuitka/json)
- FATO: pywebview 6.2.1 (2026-04-15). No Windows depende de `pythonnet` e também de `bottle` e `proxy_tools`. "pywebview ships with a built-in HTTP server". No Windows, o renderizador é escolhido na ordem `edgechromium` e depois `mshtml` (este marcado como DEPRECATED). O edgechromium exige ".NET Framework 4.6.2 and Edge Runtime installed". — [PyPI pywebview](https://pypi.org/pypi/pywebview/json); [pywebview guide](https://pywebview.flowrl.com/guide/); [pywebview web engine](https://pywebview.flowrl.com/guide/web_engine.html)
- FATO: Tauri CLI 2.12.6 (2026-11-18); há uma `next` 3.0.0-alpha.6. Para um backend Python, o Tauri usa "sidecar" (`bundle.externalBin`, binário com sufixo `-$TARGET_TRIPLE` e permissão `shell:allow-execute`/`spawn` com `"sidecar": true`). A doc cita como caso comum "Python CLI applications or API servers bundled using `pyinstaller`". — [npm @tauri-apps/cli](https://registry.npmjs.org/@tauri-apps%2Fcli); [Tauri v2 sidecar](https://v2.tauri.app/develop/sidecar/)
- FATO: Electron 45.4.1 (2026-11-19); a 45.0.0 saiu em 2026-10-21. — [npm electron](https://registry.npmjs.org/electron)
- FATO (segurança, MCP spec): "Servers MUST validate the `Origin` header on all incoming connections to prevent DNS rebinding attacks"; "When running locally, servers SHOULD bind only to localhost (127.0.0.1) rather than all network interfaces (0.0.0.0)"; "Servers SHOULD implement proper authentication". "Without these protections, attackers could use DNS rebinding to interact with local MCP servers from remote websites." — [MCP Transports — Security Warning](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- FATO: o Datasette depende de `asgi-csrf`, ou seja, adiciona proteção CSRF mesmo sendo uma ferramenta local. — [PyPI datasette](https://pypi.org/pypi/datasette/json)
- HIPÓTESE/conhecimento prévio (não reverificado): o Jupyter Server tem a opção `allow_remote_access`, cuja descrição explica que requisições com `Host` não local recebem 403 para proteger contra DNS rebinding, além de token de acesso por padrão. — [Jupyter Server config](https://jupyter-server.readthedocs.io/en/latest/other/full-config.html)
- HIPÓTESE/conhecimento prévio: `webbrowser.open(url)` da stdlib abre o navegador padrão; `importlib.resources.files("pygridplan") / "web_dist"` localiza os assets empacotados; hatchling inclui os arquivos não-Python que estão dentro do pacote. — [docs.python.org webbrowser](https://docs.python.org/3/library/webbrowser.html); [importlib.resources](https://docs.python.org/3/library/importlib.resources.html)

### Inferences
- OPINIÃO: o fluxo mínimo é um script `pygridplan = "pygridplan.app:main"` em `[project.scripts]`. Ele (1) escolhe uma porta livre (ou fixa, com fallback), (2) sobe `uvicorn.run(app, host="127.0.0.1", port=...)`, (3) abre `http://127.0.0.1:<porta>/` com `webbrowser.open` depois que o servidor estiver de pé, numa thread ou com um callback de startup. Uma porta só serve a UI estática, a API e os eventos.
- OPINIÃO (mínimo de segurança local): ligar só em `127.0.0.1`; aceitar apenas `Host` em {`127.0.0.1:<porta>`, `localhost:<porta>`} (o `TrustedHostMiddleware` da Starlette faz isso); recusar POST/WS cujo `Origin` não seja o próprio servidor; não habilitar CORS amplo; opcionalmente, um token aleatório na URL aberta pelo `webbrowser`, guardado em cookie, como faz o Jupyter. O WebSocket não segue a política de mesma origem, então a checagem de `Origin` no handshake é obrigatória se o projeto usar WS.
- OPINIÃO (desktop shell): pywebview usa o WebView2, já presente no Windows 11 (hipótese, não confirmada na página lida). Ele adiciona pythonnet e não traz o navegador embutido, então é a camada nativa mais leve para um app Python. Tauri exige toolchain Rust e o backend Python empacotado como sidecar (PyInstaller), ou seja, dois empacotamentos. Electron embute o Chromium e um runtime Node, o maior peso e um segundo runtime. Nenhum deles é necessário para o M2.
- OPINIÃO (executável único): o PyInstaller com ortools leva junto numpy, pandas e protobuf (dependências obrigatórias do ortools). O executável tende a ter centenas de MB (estimativa não medida). O Nuitka compila, mas leva tempo de build. Fica para uma fase de distribuição.

### Gaps
- Não encontrei números verificados de tamanho de instalador para Tauri, Electron ou pywebview em 2026; as afirmações de tamanho acima são estimativas.
- Não confirmei que o WebView2 Runtime vem pré-instalado no Windows 11 (a página do pywebview não diz).
- Não verifiquei o texto atual do `TrustedHostMiddleware` nem da opção `allow_remote_access` do Jupyter nesta rodada.

## 6. Exemplos reais de apps locais Python + web

### Takeaway
Quase todos os apps locais recentes convergiram para **ASGI (Starlette/FastAPI) + uvicorn**. A exceção histórica é o Jupyter (Tornado), e o TensorBoard usa Werkzeug. O Streamlit migrou de Tornado para Starlette em 2026. No transporte, há de tudo: WebSocket (marimo, Streamlit, Jupyter), SSE (Gradio desde a 4.0) e Socket.IO (NiceGUI).

### Cited Findings
- FATO: **Streamlit** 1.67.0 (2026-11-05) depende de `starlette<2,>=0.46.0`, `uvicorn<1,>=0.30.0`, `anyio`, `websockets<18,>=12.0.0`, `python-multipart` e `itsdangerous`, e **não** lista mais `tornado`. Histórico: a 1.50 dependia de `tornado`; na 1.55.0 (2026-03-03) a Starlette era um extra opcional `starlette`; na 1.58.0 (2026-05-28) `starlette` já era dependência obrigatória e `tornado` havia sumido. — [PyPI streamlit 1.67.0](https://pypi.org/pypi/streamlit/json); [PyPI streamlit 1.55.0](https://pypi.org/pypi/streamlit/1.55.0/json); [PyPI streamlit 1.58.0](https://pypi.org/pypi/streamlit/1.58.0/json); [PyPI streamlit 1.50.0](https://pypi.org/pypi/streamlit/1.50.0/json)
- FATO: **marimo** 0.25.2 (2026-10-19) depende de `uvicorn>=0.22.0`, `starlette>=0.37.2`, `websockets>=14.2.0`, `msgspec`, `pyzmq`, `loro` (CRDT) etc. — [PyPI marimo](https://pypi.org/pypi/marimo/json)
- FATO: **Gradio** 6.32.0 (2026-11-12) depende de `fastapi<1.0,>=0.115.2`, `starlette<2.0,>=1.0.1`, `uvicorn`, `httpx`, `orjson`, `pydantic`, `huggingface-hub` etc. Desde a 4.0, a fila usa SSE em vez de WebSocket. — [PyPI gradio](https://pypi.org/pypi/gradio/json); [Hugging Face post (abidlabs)](https://huggingface.co/posts/abidlabs/528535313265224)
- FATO: **NiceGUI** 4.0.0 (2026-11-04) depende de `fastapi>=0.143.1`, `starlette>=1.3.1`, `uvicorn[standard]`, `python-socketio[asyncio-client]>=5.16.2`, `aiohttp`, `httpx2`, `orjson` etc. O transporte é Socket.IO. — [PyPI nicegui](https://pypi.org/pypi/nicegui/json)
- HIPÓTESE/conhecimento prévio: o NiceGUI tem um "native mode" (`ui.run(native=True)`) que abre o app numa janela pywebview. — [NiceGUI docs: configuration & deployment](https://nicegui.io/documentation/section_configuration_deployment)
- FATO: **Jupyter Server** 2.21.1 (2026-09-15) depende de `tornado>=6.2.0`, `pyzmq`, `jupyter-client`, `terminado`, `argon2-cffi` (senha), `prometheus-client` etc. — [PyPI jupyter-server](https://pypi.org/pypi/jupyter-server/json)
- FATO: tornado 6.6.1 (2026-11-09), sem dependências. — [PyPI tornado](https://pypi.org/pypi/tornado/json)
- FATO: **Datasette** 0.65.6 (2026-11-15) é ASGI (`asgiref`), roda em `uvicorn` e depende de `asgi-csrf`, `janus` (fila sync/async), `hupper`, `pluggy`, `aiofiles` etc. — [PyPI datasette](https://pypi.org/pypi/datasette/json)
- FATO: **TensorBoard** 2.21.0 (2026-06-29) depende de `werkzeug>=1.0.1` (WSGI) e `grpcio`. — [PyPI tensorboard](https://pypi.org/pypi/tensorboard/json)

### Inferences
- OPINIÃO: o caso mais parecido com o PyGridPlan, uma UI rica em TS compilada e servida por um pacote Python, é o **marimo** (Starlette + uvicorn + websockets, com o front-end compilado embutido no pacote). O **Gradio** é a referência para o desenho "POST + SSE" com fila de jobs longos. A migração do Streamlit para Starlette/uvicorn reforça que essa pilha virou o padrão de fato para apps locais.
- OPINIÃO: o `janus` (fila com lado síncrono e lado assíncrono) usado pelo Datasette é uma alternativa pronta ao `call_soon_threadsafe` para ligar a thread do solver ao loop. Ainda assim, `call_soon_threadsafe` + `asyncio.Queue` resolve sem dependência.

### Gaps
- Não li write-ups de engenharia dos mantenedores do marimo, do Streamlit ou do NiceGUI sobre por que escolheram cada transporte. As escolhas acima foram inferidas das dependências declaradas no PyPI, exceto no Gradio, que tem justificativa citada.
- Não confirmei se o Streamlit usa WebSocket ou outro transporte depois da migração para Starlette; a dependência `websockets` sugere WebSocket.
