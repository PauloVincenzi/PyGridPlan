# Árvore de estados, desfazer/refazer e navegação entre ramos (M2)

> Notas de pesquisa · 2026-11-22 · escopo: modelar o projeto do PyGridPlan como árvore de estados (estágios com K alternativas irmãs, expansão preguiçosa) com edições finas dentro de um nó, backend Python (pydantic imutável) e interface TypeScript.
> Convenção: **FATO** = afirmação com fonte consultada nesta pesquisa; **HIPÓTESE/OPINIÃO** = inferência do pesquisador, sem fonte direta. Itens que eu conhecia mas **não** consegui verificar nesta rodada estão em "Gaps", não em "Cited Findings".

## 1. Padrões: qual combinação serve para "árvore de alternativas + edições finas dentro de um nó"?

### Takeaway
Os sistemas maduros combinam duas camadas: um **grafo/árvore imutável de estados** (commits/microversões, cada nó aponta para o pai) para ramificação e restauração, e uma **pilha linear de passos com marcas** (diffs ou patches inversos) para o desfazer fino. Para o PyGridPlan, o encaixe natural é: árvore de nós de estágio com **snapshot completo** (padrão memento, viável porque o modelo é pydantic congelado) + histórico fino linear dentro do nó, que ao ser "fechado" vira um novo nó filho.

### Cited Findings
- **FATO** — O Onshape guarda cada estado de um Part Studio como "an eternal, immutable object that we internally call a microversion"; cada nova microversão "stores a reference to the previous (parent) microversion and the actual definition change", ou seja, guarda só o delta relativo ao pai. — [Onshape: Under the hood, how collaboration works](https://www.onshape.com/en/blog/under-the-hood-how-collaboration-works)
- **FATO** — O próprio Onshape descreve o modelo como inspirado no git: "microversions corresponding to git 'commits' and workspaces corresponding to branches"; como cada workspace aponta para sua última microversão, as microversões formam uma **árvore**, e o "version graph" é uma visão simplificada dela. — [Onshape: Under the hood](https://www.onshape.com/en/blog/under-the-hood-how-collaboration-works)
- **FATO** — No Onshape, **desfazer e restaurar são coisas diferentes**: desfazer "cannot simply take the Part Studio back to an earlier microversion"; ele cria uma nova microversão aplicando o inverso da mudança do usuário sobre a mais recente. Restaurar do histórico é "a complementary capability to undo" e volta de fato a um estado anterior (podendo apagar edições de colaboradores). — [Onshape: Under the hood](https://www.onshape.com/en/blog/under-the-hood-how-collaboration-works)
- **FATO** — O Blender usa uma pilha única que mistura tipos de passo; distingue passos **stateful** (guardam o estado e podem ser carregados em qualquer direção) de **differential** (guardam só a mudança em relação ao anterior); a pilha atual é "fully relative" (chegar a um passo exige reaplicar os intermediários); os passos de undo global "effectively store the whole data". A página está marcada como em construção. — [Blender Developer Docs: Undo](https://developer.blender.org/docs/features/core/undo/)
- **FATO** — O tldraw grava mudanças do store como diffs pendentes até uma **marca** (`markHistoryStoppingPoint`); a marca é o ponto de parada para que "complex operations can be undone in one step"; `bailToMark` descarta mudanças (não vão para o redo), usado para cancelar um arrasto; `squashToMark` funde tudo desde uma marca em um passo. — [tldraw docs: History](https://tldraw.dev/sdk-features/history)
- **FATO** — Immer gera, para cada `produce`, patches de ida e patches inversos; `applyPatches` com os inversos reverte a mudança; o formato lembra JSON Patch (RFC 6902) com `op` `replace/add/remove`, mas `path` é um **array** de segmentos, não string (conversão para JSON Pointer RFC 6901 é juntar com `/` e escapar). Immer garante patches corretos, **não mínimos**. — [Immer: Patches](https://immerjs.github.io/immer/patches/)
- **FATO** — Heer et al. (2008) modelam históricos como movimento por um grafo de estados ou de ações; uma decisão central do espaço de design é se o histórico grava **ações** ou **estados resultantes**, e isso determina quais operações de histórico ficam possíveis; o trabalho cobre desde undo/redo básico até "branching timelines". — [Heer, Mackinlay, Stolte, Agrawala — Graphical Histories for Visualization (InfoVis 2008, PDF)](https://www.cs.tufts.edu/comp/250VA/papers/heer2008graphical.pdf)

### Inferences
- **HIPÓTESE** — Mapeamento de padrões para o PyGridPlan:
  - *Command pattern*: já é a fronteira do sistema (site.set, rooms.set, …). Mas **não** precisa implementar `undo()` por comando: com estado imutável, desfazer = voltar ao nó/estado anterior (memento). Comandos com inverso só seriam necessários em colaboração multiusuário (caso Onshape/Figma), que está fora do escopo.
  - *Memento/snapshot*: casa diretamente com modelos pydantic `frozen`; cada nó guarda o `Plan` inteiro. É o padrão mais simples e o único robusto diante de solver não reprodutível (ver seção 3).
  - *Event sourcing com replay*: **inadequado como fonte única**, porque reexecutar `stage.generate` não reproduz a mesma solução quando o CP-SAT para por tempo. Útil só como **log de auditoria** (lista de comandos aplicados) ao lado dos snapshots.
  - *Estruturas persistentes com compartilhamento estrutural*: o ganho de memória só importa com estados grandes ou muitos passos; com ~dezenas de nós de poucas dezenas de KB, compartilhamento estrutural é otimização prematura.
  - *Patches (Immer / RFC 6902)*: bons para **transporte** servidor→navegador (enviar só o diff do estado derivado) e para o histórico fino no cliente, não para a árvore de alternativas.
  - *Undo tree (Emacs/Vim)* vs *pilha linear*: a árvore de estágios do PyGridPlan **já é** uma undo tree explícita e nomeada; o histórico fino dentro do nó pode ser linear.
- **HIPÓTESE** — Separação recomendada em duas camadas, espelhando Onshape (microversões vs versões nomeadas) e tldraw (diffs vs marcas):
  1. **Árvore de estágios (grossa)**: nós imutáveis `{id, parent_id, stage, plan_snapshot, assumptions, solver_meta, status: expanded|unexpanded}`. `stage.generate` cria K irmãos; `stage.choose` marca um; `tree.goto` muda o cursor.
  2. **Edições finas (lineares) dentro do nó**: cada edição (travar cômodo, mover porta, ajustar peso) gera um novo estado; a pergunta é se cada edição vira **um nó filho** (tudo é árvore, mais simples de raciocinar) ou um **passo numa pilha local** do nó (árvore mais limpa, mas duas estruturas). Opinião: começar com "toda edição que muda o plano cria um nó filho do tipo `edit`" e oferecer na UI uma visão compacta que colapsa cadeias de `edit` (como o `squashToMark` do tldraw, mas só de visualização). Isso evita duas semânticas de undo e dá redo/ramos de graça.
- **HIPÓTESE** — Desfazer na árvore = mover o cursor para o pai; refazer = mover para o último filho visitado (precisa guardar `last_visited_child` por nó, como fazem as undo trees). Nada é destruído; "descartar ramo" pode ser uma ação explícita separada.

### Gaps
- Não consegui ler a documentação primária do **Emacs undo-tree** (certificado expirado em dr-qubit.org; EmacsWiki retornou HTTP 402) nem do `:undolist`/`undotree` do **Vim**. O que sei de memória (ambos guardam a árvore de alterações e permitem navegar ramos; o Emacs tem visualizador e persistência opcional em arquivo) fica **não verificado**.
- A documentação do Blender não detalha a deduplicação de datablocks inalterados no memfile undo nem limites de memória da pilha.
- Não verifiquei o texto do **RFC 6902** diretamente; a relação com Immer vem da documentação do Immer.

## 2. Onde mora o histórico (servidor x cliente) e como desfazer operações longas/assíncronas

### Takeaway
Quando o servidor é a autoridade, os sistemas consultados aplicam mudanças **otimistas** no cliente mas tratam o servidor como verdade final, e separam explicitamente o que entra no undo (ações do usuário) do que não entra (atualizações remotas, inicialização, estado efêmero). Para o PyGridPlan, o histórico/árvore deve morar **no Python** (é parte do projeto salvo e precisa ser acessível por testes e pelo futuro MCP); o cliente guarda no máximo estado efêmero de UI.

### Cited Findings
- **FATO** — No Figma, o servidor é autoritativo: clientes "can't reject changes from the server because the server is the ultimate authority"; o cliente aplica as próprias mudanças imediatamente (otimista) e descarta mudanças do servidor que conflitem com mudanças locais ainda não confirmadas, para evitar "flicker". Conflitos são resolvidos por propriedade, estilo last-writer-wins. — [Figma: How Figma's multiplayer technology works](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)
- **FATO** — Princípio de undo do Figma: "if you undo a lot, copy something, and redo back to the present (a common operation), the document should not change"; e "an undo operation modifies redo history at the time of the undo". O texto admite que undo multiusuário é "inherently confusing". — [Figma blog](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)
- **FATO** — tldraw tem três modos de histórico em `editor.run`: `record` (empilha e limpa o redo), `record-preserveRedoStack` (empilha sem limpar redo; usado para seleção, para permitir desfazer–selecionar–copiar–refazer) e `ignore` (não empilha; usado para posição de ponteiro). Mudanças remotas nunca são gravadas; só registros do store participam do undo, estado externo não. `clearHistory()` deve ser chamado após carregar um documento. — [tldraw docs: History](https://tldraw.dev/sdk-features/history)
- **FATO** — No tldraw, `bail()`/`bailToMark()` revertem para a marca e **descartam** as mudanças (não vão para o redo); é o mecanismo usado para cancelar um arrasto. — [tldraw docs: History](https://tldraw.dev/sdk-features/history)
- **FATO** — Yjs `UndoManager` grava por padrão só mudanças locais sem `origin`; `trackedOrigins` restringe as origens rastreadas; `captureTimeout` (padrão 500 ms) funde edições próximas em um passo; `stopCapturing()` força passo novo; `stackItem.meta` guarda metadados (ex.: posição do cursor). — [Yjs docs: Y.UndoManager](https://docs.yjs.dev/api/undo-manager)
- **FATO** — Excalidraw: o changelog do multiplayer undo/redo (PR #7348) introduz um componente `Store` e recomenda `CaptureUpdateAction.NEVER` para atualizações remotas e inicialização de cena, que ficam fora das pilhas locais. Um commit do mesmo trabalho registra um trade-off aceito: desfazer e refazer pode perder elementos em certos cenários colaborativos. Fontes secundárias/espelhos, não o repositório oficial. — [Changelog @dwelle/excalidraw (jsDelivr)](https://cdn.jsdelivr.net/npm/@dwelle/excalidraw@0.5.0-61258ed/CHANGELOG.md); [commit "feat: multiplayer undo / redo (#7348)" (espelho)](https://gitea.maison43.duckdns.org/gilles/excalidraw/commit/530617be90df8d41f93c7c885d3097565c4c7f6d)

### Inferences
- **HIPÓTESE** — Arquitetura sugerida: **árvore e cursor no servidor Python** (`ProjectTree` + `cursor`), comandos como única via de mudança (já decidido). O navegador recebe estado derivado do nó corrente + um resumo da árvore (ids, estágio, rótulos, métricas) para desenhar o painel de histórico. Undo/redo na UI são apenas comandos `tree.goto(parent)` / `tree.goto(child)`. Isso dá consistência trivial: não há duas cópias do histórico para sincronizar.
- **HIPÓTESE** — Otimismo no cliente só para coisas baratas e locais (arrastar porta antes de soltar, zoom, seleção), à moda do modo `ignore` do tldraw. Nada disso entra no histórico; ao soltar, o cliente envia **um** comando.
- **HIPÓTESE** — Re-solve longo (até dezenas de segundos): tratar como **job** com estado `running|done|cancelled|failed`. Opções:
  1. *Cancelar*: um novo comando de edição ou um undo durante o job cancela o job (CP-SAT aceita parada externa; não verificado nesta rodada) e descarta o resultado — análogo ao `bail` do tldraw.
  2. *Enfileirar*: arriscado; edições em fila sobre um estado que ainda não existe geram confusão.
  3. *Nó pendente*: a edição cria imediatamente um nó filho `pending` com as **entradas** (o pedido de edição); quando o solver termina, o nó recebe a solução e vira `ready`. Undo durante o job = `goto(parent)` + cancelar o job do nó pendente (ou mantê-lo como ramo "abandonado"). Opinião: a opção 3 é a mais coerente com a árvore, porque o que se desfaz é a **edição** (o nó), não a execução do solver.
- **HIPÓTESE** — Regra de UX derivada do princípio do Figma: navegar na árvore (goto) **não** deve alterar nenhum nó; só comandos de mudança criam nós. Assim "desfazer muito, olhar algo, refazer" sempre volta ao mesmo estado.

### Gaps
- Não verifiquei na documentação do OR-Tools como interromper um `CpSolver.Solve` em andamento a partir de outra thread (`StopSearch`/callback); confirmar antes de desenhar o cancelamento.
- Não encontrei fonte primária sobre como ferramentas de design generativo (Autodesk etc.) tratam undo durante uma geração em andamento.

## 3. Armazenamento: snapshots x deltas x entradas+semente; formato do arquivo; versionamento do schema

### Takeaway
Como o CP-SAT só é reprodutível sob condições restritas (1 worker ou modo determinístico mais lento, mesma versão), o nó deve guardar a **solução** (snapshot) e, ao lado, as entradas e metadados do solver para auditoria. Pelo tamanho provável do modelo, snapshot completo em JSON é suficiente; deltas (como Onshape) só se justificam com estados muito maiores.

### Cited Findings
- **FATO** — Onshape guarda deltas por microversão ("Each microversion only stores the changes relative to its parent") e mantém "the entire evolution of the Document"; o artigo não traz números de tamanho. — [Onshape: Under the hood](https://www.onshape.com/en/blog/under-the-hood-how-collaboration-works)
- **FATO** — O undo global do Blender guarda essencialmente os dados inteiros por passo ("effectively store the whole data"), via o código de leitura/escrita do `.blend`. — [Blender Developer Docs: Undo](https://developer.blender.org/docs/features/core/undo/)
- **FATO** (fonte comunitária) — Em discussões do OR-Tools, um usuário relata que com `num_workers = 1` "the results are always the same", porém com menos soluções que o modo padrão; outra resposta descreve um modo paralelo determinístico (busca intercalada em lotes com sincronização) que é "usually way slower than the non deterministic version"; usuários relatam que `max_time_in_seconds` nem sempre é respeitado exatamente. — [or-tools-discuss: Randomness in CP-SAT search](https://groups.google.com/g/or-tools-discuss/c/nmor0kQc7-8); [or-tools-discuss: Deterministic execution time for CP Sat](https://groups.google.com/g/or-tools-discuss/c/ZGj5vhhZX48); [or-tools-discuss: max_time_in_seconds is not always adhered to](https://groups.google.com/g/or-tools-discuss/c/T5OY3cEqbws)
- **FATO** — CP-SAT aceita *hints* (`model.add_hint(x, v)`), prática chamada "warm-starting"; "Some workers will try to follow these hints"; hints ruins podem atrasar; `fix_variables_to_their_hinted_value = True` força os valores sugeridos. — [CP-SAT Primer: Parameters](https://d-krupke.github.io/cpsat-primer/parameters.html)
- **FATO** — Patches do Immer são corretos mas não mínimos; achar o conjunto mínimo é "potentially computationally very expensive". — [Immer: Patches](https://immerjs.github.io/immer/patches/)
- **FATO** — Heer et al. observam que históricos de interação crescem rápido e os mecanismos precisam escalar. — [Graphical Histories (PDF)](https://www.cs.tufts.edu/comp/250VA/papers/heer2008graphical.pdf)

### Inferences
- **HIPÓTESE** — Conteúdo mínimo de um nó: `plan` (snapshot completo, `model_dump(mode="json")`), `assumptions` (pedido + preferências vigentes, ou referência a elas se não mudaram), `command` que o criou, `solver_meta` (status OPTIMAL/FEASIBLE, objetivo, tempo, `num_workers`, semente, versão do OR-Tools), `score`/métricas para comparar irmãos, `created_at`. A solução guardada permite reabrir o projeto sem re-solve; as entradas permitem re-solve opcional ("tentar de novo") e usar a solução antiga como **hint** de warm start numa edição fina.
- **HIPÓTESE** — Estimativa de tamanho (não medida): uma planta com ~10–20 cômodos, aberturas e paredes, serializada em JSON, deve ficar na ordem de 10–100 KB. Com K = 4 por estágio, ~6–10 estágios visitados e algumas dezenas de edições finas, a árvore teria ~50–100 nós → ~1–10 MB sem compressão; JSON comprime bem (gzip/zip costuma reduzir várias vezes). **Medir no primeiro protótipo** antes de decidir por deltas.
- **HIPÓTESE** — Formato de arquivo, em ordem de simplicidade:
  1. **JSON único** (`.pygridplan.json`): `{schema_version, app_version, nodes: [...], cursor, root_id}`. Legível, diffável, testável com fixtures. Suficiente até alguns MB.
  2. **Zip** (`.pgp`) com `manifest.json` + `nodes/<id>.json` (+ DXF exportados opcionais): mesma estrutura, compressão de graça, permite guardar anexos.
  3. **SQLite**: só se houver necessidade de salvar incrementalmente nós durante sessões longas ou consultar a árvore; adiciona complexidade de migração.
  Opinião: começar com JSON único (com escrita atômica: arquivo temporário + rename) e migrar para zip só se o tamanho incomodar.
- **HIPÓTESE** — Versionamento do schema: campo `schema_version` inteiro no topo; ao abrir, uma cadeia de funções `migrate_vN_to_vN+1(dict) -> dict` antes de validar com pydantic; testes com fixtures de cada versão antiga em `tests/fixtures/`. Snapshots completos tornam a migração mais simples que deltas (cada nó migra sozinho; deltas exigiriam migrar operações).
- **HIPÓTESE** — Alternativa a considerar: reduzir a não reprodutibilidade usando `num_workers = 1` ou limite de tempo determinístico em testes/fixtures, mantendo paralelismo na UI. Mesmo assim, guardar a solução continua necessário (versões diferentes do OR-Tools podem mudar o resultado).

### Gaps
- Não encontrei documentação oficial do OR-Tools sobre `max_deterministic_time` combinado com `num_workers` e reprodutibilidade; consultar `sat_parameters.proto` antes de decidir.
- Não verifiquei na documentação do pydantic detalhes de `model_dump`/`model_validate` com `frozen=True` (comportamento conhecido do projeto, mas não pesquisado aqui).
- Nenhuma medição real do tamanho do JSON de um `Plan` do PyGridPlan; a estimativa acima é hipótese.

## 4. Bibliotecas existentes (Python e TypeScript) — e se precisa de biblioteca

### Takeaway
No Python, não há biblioteca de "árvore de undo" que valha a dependência: o modelo pydantic congelado + um dicionário `id -> Node` resolve em ~100–200 linhas. No TypeScript, Immer (patches) e zundo existem e são mantidos, mas só fariam sentido se o histórico morasse no cliente — o que esta pesquisa não recomenda.

### Cited Findings
- **FATO** — **Immer** 11.2.10 é a versão `latest` no registro npm (data de publicação inferida do metadado ≈ 2026-11-10, não rotulada). Patches exigem `enablePatches()` desde o Immer 6; `produceWithPatches` devolve `[nextState, patches, inversePatches]`. — [npm registry: immer/latest](https://registry.npmjs.org/immer/latest); [Immer: Patches](https://immerjs.github.io/immer/patches/)
- **FATO** — **zundo** (middleware de undo/redo para Zustand): uma única exportação `temporal`, < 700 B segundo o README, licença MIT; versão mais recente encontrada 2.3.0; requer zustand ≥ 4.3.0 com TypeScript; `wrapTemporal` permite persistir o histórico. Sinais de saúde divergentes entre Snyk ("Healthy") e depscope (61/100). — [zundo no GitHub](https://github.com/charkour/zundo/releases); [npm: zundo](https://npmjs.com/package/zundo); [Snyk Advisor: zundo](https://snyk.io/advisor/npm-package/zundo)
- **FATO** — **tldraw** expõe histórico com marcas, `bail`, `squashToMark`, modos `record/record-preserveRedoStack/ignore` (é parte do SDK do tldraw, não biblioteca de undo isolada). — [tldraw docs: History](https://tldraw.dev/sdk-features/history)
- **FATO** — **Yjs** `UndoManager`: undo por origem, `captureTimeout` 500 ms, metadados por item. Pressupõe documento CRDT do Yjs. — [Yjs docs](https://docs.yjs.dev/api/undo-manager)
- **FATO** — **pyrsistent** (Python): versão mais recente 0.20.0, `requires_python >=3.8`, "Persistent/Functional/Immutable data structures". Data da release não lida. — [PyPI JSON: pyrsistent](https://pypi.org/pypi/pyrsistent/json)
- **FATO** — **immutables** (Python): 0.21, lançada em 2024-10-10; mapa imutável baseado em HAMT (a mesma estrutura usada no `contextvars` do CPython 3.7, PEP 567); cadência de releases desacelerou (0.20 em ago/2023, 0.21 em out/2024); classificadores só até Python 3.12 (wheels para 3.13). — [PyPI: immutables](https://pypi.org/project/immutables/)

### Inferences
- **HIPÓTESE** — Python: `pyrsistent`/`immutables` não acrescentam nada relevante, porque o pydantic `frozen` já dá imutabilidade e a árvore é pequena; compartilhamento estrutural só ajudaria em memória, que não é gargalo. Recomendação: **código próprio** (`Node`, `ProjectTree` com `add_children`, `goto`, `parent`, `children`, `path_to_root`, `to_json/from_json`), testado com TDD. Isso segue o princípio "não adicionar dependências sem justificativa" do projeto.
- **HIPÓTESE** — TypeScript: se a UI usar Zustand, o zundo poderia servir para undo **puramente local de UI** (ex.: desfazer zoom/pan ou rascunho de arrasto), mas isso pode ser feito sem biblioteca. Immer é útil se o servidor enviar patches do estado derivado; aplicar RFC 6902 também é simples sem Immer.
- **HIPÓTESE** — Yjs/Automerge (CRDTs) são desproporcionais: resolvem colaboração concorrente, que o PyGridPlan offline e monousuário não tem.

### Gaps
- Não encontrei, nesta rodada, pacote Python mantido e relevante especificamente de "undo/redo" (procurei pouco; nomes como `undo` e `transitions` não foram verificados). Não citar sem checar o PyPI.
- Não verifiquei versão atual nem estado do **Automerge** e de **redux-undo**; não citar versões.
- Data exata da release 0.20.0 do pyrsistent não lida.

## 5. Como ferramentas reais fazem e lições de UX (visualizar árvore, histórico compacto, comparar irmãos)

### Takeaway
Ferramentas de CAD/design separam **histórico automático fino** (microversões, passos de undo) de **marcos nomeados/ramos** (versões, workspaces), e mostram ao usuário uma visão **simplificada** da árvore. Para comparar alternativas, a literatura de exploração de design favorece desenvolver e ver alternativas **lado a lado** em vez de só voltar no tempo.

### Cited Findings
- **FATO** — Onshape: microversões formam uma árvore e o "version graph" é "a simplified view of this"; merge cria nova microversão no destino, com a regra "the 'from' workspace will win" e a meta de que "Merge conflicts should never happen". — [Onshape: Under the hood](https://www.onshape.com/en/blog/under-the-hood-how-collaboration-works)
- **FATO** — Onshape descreve versões como registros imutáveis do projeto, úteis para auditoria e IP, e introduziu "Workspace Protection" para manter workspaces críticos inalterados. (Fonte de marketing do fabricante.) — [Onshape: Branching & merging for mechanical engineers](https://www.onshape.com/en/blog/branching-merging-building-mechanical-engineers-use-cloud-native-cad); [Onshape: versioning workflow features](https://www.onshape.com/en/blog/versioning-workflow-features)
- **FATO** — Figma: undo deve preservar o documento no ciclo desfazer–copiar–refazer; undo multiusuário é confuso porque "refazer" pode sobrescrever edições posteriores de outros. — [Figma blog](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)
- **FATO** — tldraw: seleção é gravada sem limpar o redo, posição de ponteiro não é gravada; operações compostas (crop) são fundidas em um passo com `squashToMark`. — [tldraw docs: History](https://tldraw.dev/sdk-features/history)
- **FATO** — Heer et al. construíram históricos gráficos no Tableau (miniaturas de estados em linha do tempo com ramos) e argumentam que histórico visível apoia análise e comunicação (montar relatórios/apresentações). — [Graphical Histories (PDF)](https://www.cs.tufts.edu/comp/250VA/papers/heer2008graphical.pdf); [Tableau whitepaper](https://tableau.com/whitepapers/graphical-histories-visualization)
- **FATO** — Parallel Paths (Terry, Mynatt, Nakakoji, Yamamoto, CHI 2004): modelo de interação para "generating, manipulating, and comparing alternative solutions", que enfatiza "the active, simultaneous development of multiple, alternative solutions" em contraste com ferramentas de captura automática de histórico; demonstrado no protótipo Parallel Pies. — [CHI 2004 PDF (RWTH)](https://hci.rwth-aachen.de/materials/conferences/CHI2004/1p711.pdf)
- **FATO** — Side Views (Terry & Mynatt, UIST 2002): pré-visualizações "on-demand, persistent, and dynamic" de comandos para usuários experientes em tarefas abertas. — [Terry UIST02 PDF](https://www.lri.fr/~mbl/FundHCI/papers/Terry-UIST02.pdf)
- **FATO** — Hartmann et al. (UIST 2008), "Design as Exploration": criação de alternativas de interface por autoria paralela e ajuste em tempo de execução (Juxtapose). — [Stanford HCI: Design As Exploration](https://hci.stanford.edu/publications/paper.php?id=16)

### Inferences
- **HIPÓTESE** — Lições de UX para o M2:
  1. **Painel de árvore compacto**: mostrar estágios como linhas e as K alternativas como miniaturas (thumbnails do plano) lado a lado; ramo escolhido destacado, irmãos não expandidos em cinza com o rótulo "não explorado". Cadeias de edições finas colapsadas em um item ("5 ajustes") expansível — a "visão simplificada" do Onshape.
  2. **Comparar irmãos lado a lado** (Parallel Paths/Juxtapose) com métricas (pontuação, área, violações aceitas) em vez de exigir ir e voltar com undo.
  3. **Atalhos de undo/redo = navegação na árvore**, nunca destrutivos; "descartar ramo" é ação explícita e confirmada.
  4. **Estado efêmero fora do histórico** (zoom, seleção, hover), como o `ignore` do tldraw.
  5. **Rótulos automáticos** nos nós a partir do comando ("Travou Cozinha", "Peso privacidade 0,6→0,8") para o histórico ser legível e servir de relatório (argumento de comunicação de Heer et al.).

### Gaps
- Não consegui verificar fontes primárias sobre **Photoshop** (painel History + Snapshots), **Grasshopper**, **Houdini** (grafo de nós como histórico paramétrico), **Autodesk Generative Design** (galeria de resultados filtráveis) nem **Design Galleries** (Marks et al., SIGGRAPH 1997). São referências relevantes conhecidas, mas sem fonte consultada nesta rodada; não afirmar detalhes sem verificar.
- O conteúdo do Excalidraw veio de espelhos/fontes secundárias; o código atual (`packages/excalidraw/history.ts`) não foi lido.

## 6. Trabalho acadêmico sobre modelos de undo e históricos de exploração de design

### Takeaway
A literatura distingue undo **linear**, **seletivo** (desfazer uma operação antiga mantendo as posteriores) e **regional** (desfazer só numa região/objeto), além de históricos em **árvore/grafo** para exploração. Para o PyGridPlan, o undo seletivo tem análogo natural: reaplicar as mesmas edições finas sobre um irmão diferente ("rebase" de edições), mas isso exige re-solve e é candidato a fase posterior.

### Cited Findings
- **FATO** — Myers et al., "Selective Undo Support for Painting Applications" (CHI 2015): o undo linear "is not useful if the user has performed desired operations after undesired ones"; o protótipo Aquamarine usa o **modelo de script** (operações desfeitas seletivamente são puladas e o histórico é reexecutado) em vez do modelo de inversos; dois estudos informais sugerem que o undo seletivo é usável e desejado. — [CMU Aquamarine](https://www.cs.cmu.edu/~marmalade/aquamarine.html); [DOI 10.1145/2702123.2702543 via Unpaywall](https://unpaywall.org/10.1145%2F2702123.2702543)
- **FATO** — A lista de referências de Myers et al. cita undo regional: Kawasaki & Igarashi (2004, planilhas), Li & Li (2003, edição de texto) e Seifried et al. (CHI 2012, superfícies interativas grandes). Um artigo posterior sobre undo em VR multiusuário classifica conceitos de undo em global, pessoal e seletivo/regional. — [HAL: referências](https://hal.archives-ouvertes.fr/hal-01185805v2/html_references); [Just Undo It (arXiv 2403.11756)](https://arxiv.org/pdf/2403.11756)
- **FATO** — Heer et al. (2008): espaço de design de históricos — gravar ações x estados; históricos em ramos; necessidade de escalar. — [Graphical Histories (PDF)](https://www.cs.tufts.edu/comp/250VA/papers/heer2008graphical.pdf)
- **FATO** — Terry et al. (CHI 2004) posicionam "Parallel Paths" contra a captura automática de histórico: o objetivo é desenvolver alternativas simultaneamente. — [CHI 2004 PDF](https://hci.rwth-aachen.de/materials/conferences/CHI2004/1p711.pdf)

### Inferences
- **HIPÓTESE** — O "modelo de script" de Myers corresponde, no PyGridPlan, a guardar a **lista de comandos de edição** de um ramo e poder reaplicá-la em outro ponto da árvore. Como cada reaplicação dispara CP-SAT (não determinístico), o resultado seria um **novo ramo**, não uma restauração — compatível com a árvore, mas é funcionalidade a deixar para depois do M2.
- **HIPÓTESE** — Gravar **estados** (snapshot) e **ações** (comando) em cada nó combina as duas opções de Heer et al.: estados para restaurar e comparar sem re-solve; ações para rotular, auditar e eventualmente reaplicar.
- **HIPÓTESE** — Undo regional ("desfazer só o que mudei neste cômodo") é difícil num plano gerado por otimização global: mudar um cômodo pode deslocar os outros. Não recomendado para o M2.

### Gaps
- Não li os textos completos de Berlage (1994, selective undo em GUIs), Kurlander & Feiner (históricos editáveis), nem de Seifried et al. (2012); citações vêm de listas de referências e resumos.
- Não encontrei, nesta rodada, estudo acadêmico específico sobre **árvores de alternativas geradas por solver** (design generativo com histórico de exploração) além dos trabalhos de exploração paralela citados.
