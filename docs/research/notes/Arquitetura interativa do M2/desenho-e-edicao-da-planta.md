# Desenho e edição interativa da planta 2D no navegador (TypeScript)

> Notas de pesquisa, 2026-11-22. Escopo: escolher a abordagem de renderização e interação do M2 (SVG x Canvas 2D x WebGL x bibliotecas), com pan/zoom, snapping, cotas e arrasto, avaliadas contra o caso de teste da seção 23.3 do design (portas e passagens sugeridas, "aceitar todas", porta que segue o cursor ao longo da parede, snap no ponto sugerido, clique abre a porta).
> Convenção: **FATO** = verificado em fonte citada nesta rodada. **HIPÓTESE/OPINIÃO** = inferência do pesquisador ou conhecimento prévio que não foi reconferido. Versões e datas vêm do registro npm (`registry.npmjs.org/<pacote>`, campo `time`) e da API pública do GitHub, consultados em 2026-11-22.

## 1. SVG x Canvas 2D x WebGL na escala do PyGridPlan (centenas a poucos milhares de formas)

### Takeaway
Na escala do PyGridPlan (8–20 cômodos, paredes, cotas, depois portas, janelas e móveis: algumas centenas de elementos, no máximo uns 2 mil), o desempenho não decide a escolha. Os benchmarks com metodologia só mostram SVG e Canvas perdendo fluidez acima de ~1–5 mil nós, ou ~8 mil elementos gráficos. O que decide são hit-testing, nitidez, texto, temas via CSS, exportação SVG e testes, e nesses pontos o SVG ganha.

### Cited Findings
- **FATO:** Benchmark da yWorks (28/03/2018, PC i7-6700): com 1 mil nós, SVG simples, Canvas simples e WebGL ficam todos a 60 fps; com 5 mil nós, SVG e Canvas a 23 fps e WebGL simples a 46 fps; com 10 mil nós, SVG a 10 fps, Canvas a 11 fps e WebGL otimizado a 60 fps. Num iPad Air 2013 com 1 mil nós: SVG 17 fps, Canvas 24 fps. "SVG complexo" e "Canvas complexo" aparecem como não recomendados a partir de 1 mil nós. O dado tem 8 anos — [yWorks, SVG, Canvas, WebGL](https://www.yworks.com/blog/svg-canvas-webgl)
- **FATO:** A yWorks recomenda SVG para gráficos vetoriais nítidos com zoom aproximado, Canvas ou WebGL para a visão geral, e SVG para exportação ("crisp, high-quality SVGs and PDFs"). Também diz que o WebGL "doesn't work nearly as well with high-quality text-rendering" e sugere desenhar os rótulos em Canvas por cima — [yWorks](https://www.yworks.com/blog/svg-canvas-webgl)
- **FATO:** Estudo acadêmico de 2018 (Horak et al., pôster): a queda de desempenho começou acima de 400 nós em todas as tecnologias, o que equivale a ~8.000 elementos gráficos, e SVG e Canvas tiveram desempenho "quase igual" — [Horak 2018, pôster](https://mt.inf.tu-dresden.de/cnt/uploads/Horak-2018-Graph-Performance-Poster.pdf) (citado via resumo de busca, PDF não aberto)
- **FATO:** O livro *D3.js in Action* (3ª ed.) diz que o desempenho do SVG pode despencar com mais de ~1.000 elementos no DOM — [Manning, cap. 15](https://livebook.manning.com/book/d3js-in-action-third-edition/chapter-15) (resumo de busca)
- **FATO:** Benchmark antigo de Boris Smus: o custo do SVG cresce com o número de objetos; o do Canvas cresce com a área em pixels e quase não depende do número de objetos — [smus.com](https://smus.com/canvas-vs-svg-performance/) (resumo de busca, datado)
- **FATO:** `vector-effect="non-scaling-stroke"` mantém a espessura do traço independente de transformações e do zoom. É Baseline "Widely available", disponível em todos os navegadores desde julho de 2020, e também existe como propriedade CSS (que prevalece sobre o atributo). Os valores `non-scaling-size`, `non-rotation` e `fixed-position` não têm implementação — [MDN, vector-effect](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/vector-effect)
- **FATO:** O Konva (Canvas 2D) aloca para cada camada um "hit canvas" sempre com razão 1. Cada camada tem custo incremental, e o Konva avisa quando há mais de 5. A detecção de toque fica desligada durante o arrasto (`Konva.hitOnDragEnabled = false` por padrão). `listening(false)` remove o custo de hit-testing de uma forma ou camada — [Konva, Performance Tips](https://konvajs.org/docs/performance/All_Performance_Tips.html)
- **FATO:** O hit-testing do Konva usa um "colorKey" por forma, gerado com `Util.getRandomColor()`, e um `bufferHitCanvas`: cada forma é pintada no canvas oculto com uma cor única, e a cor do pixel sob o cursor identifica a forma — [código-fonte, Shape.ts](https://github.com/konvajs/konva/blob/master/src/Shape.ts)

### Inferences
- **OPINIÃO:** SVG é a escolha natural para o M2. Os motivos:
  - **Hit-testing nativo:** `pointerenter`, `pointerleave` e `click` por elemento, `pointer-events: stroke|fill|none` e CSS `:hover`. Nada disso existe no Canvas, que exige um índice manual ou um hit canvas por cor, como o Konva.
  - **Nitidez em qualquer zoom:** é vetorial e tem `non-scaling-stroke`. No Canvas é preciso redesenhar no `devicePixelRatio` a cada zoom.
  - **Texto das cotas:** `<text>` é nítido e pode ser selecionado ou lido pelo leitor de tela. No WebGL o texto é o ponto fraco documentado.
  - **Tema escuro:** variáveis CSS (`fill: var(--wall)`) trocam o tema sem redesenho.
  - **Acessibilidade:** `role`, `aria-label` e `<title>` por elemento. O Canvas é um bitmap opaco para leitores de tela.
  - **Exportação:** o DOM já é o SVG, coerente com os relatórios SVG que o motor já gera.
  - **Playwright:** localizadores por `data-testid` e `aria` funcionam em elementos SVG. No Canvas só sobram cliques por coordenada e comparação de screenshots.
- **HIPÓTESE:** O orçamento real do PyGridPlan é de ~20 cômodos × (4–8 paredes + rótulo + cota) + grade + contorno do lote + 20–40 portas e janelas + móveis, o que fica abaixo de ~1.500 nós SVG. Fica no regime em que todos os benchmarks citados mostram 60 fps num desktop. A grade infinita **não** deve ser feita de milhares de `<line>`: use um `<pattern>` SVG, ou um único `<path>` recalculado para a área visível, ou um fundo CSS/Canvas atrás do SVG.
- **HIPÓTESE:** O risco de desempenho do SVG está no layout e no restyle quando muitos atributos mudam por quadro (por exemplo, recalcular todas as cotas a cada `pointermove`). Para evitar: mexer só na transformação de um `<g>` de câmera durante o pan/zoom e atualizar um único elemento de prévia durante o hover.
- **OPINIÃO:** O WebGL (PixiJS) só se justificaria com dezenas de milhares de elementos ou no 3D. Para o 2D do M2, ele traz custo (bundle de ~282 kB gzip, texto ruim, sem CSS, sem DOM para testes) sem benefício.

### Gaps
- Não encontrei benchmark recente (2024–2026) com metodologia publicada comparando SVG e Canvas em navegadores atuais. Os números da yWorks são de 2018, e o pôster de Horak foi lido só por resumo.
- O custo de `vector-effect: non-scaling-stroke` com centenas de elementos durante o zoom não foi medido em fonte nenhuma. Medir no protótipo.

## 2. Pan/zoom: viewBox ou matriz própria x d3-zoom x panzoom x svg-pan-zoom; roda, trackpad e pinça

### Takeaway
Para uma única cena SVG com câmera, uma câmera própria (~60–100 linhas: estado `{x, y, k}`, wheel + pointer events, zoom em torno do cursor) ou o `d3-zoom` são as opções sólidas. O `d3-zoom` foi atualizado em novembro de 2026, não depende do DOM e trata roda, arrasto, toque e duplo clique. O `@panzoom/panzoom` e o `panzoom` (anvaka) transformam um elemento via CSS e servem menos para CAD. O `svg-pan-zoom` tem pouca atividade (último release em outubro de 2024).

### Cited Findings
- **FATO (versões e licenças, registro npm, 2026-11-22):**
  - `d3-zoom` 3.0.1, publicado em 2026-11-03, ISC; ~17,7 kB gzip com dependências (Bundlephobia).
  - `d3-selection` 3.0.1, 2026-11-03, ~4,3 kB gzip.
  - `d3-drag` 3.0.1, 2026-11-03, ~5,9 kB gzip.
  - `d3` 7.9.2, 2026-11-03, ISC.
  - `@panzoom/panzoom` 4.6.2, 2026-04-02, MIT, ~3,7 kB gzip.
  - `panzoom` (anvaka) 9.4.4, 2026-03-26, MIT, ~6,5 kB gzip.
  - `svg-pan-zoom` 3.6.2, 2024-10-20, BSD-2-Clause, ~7,9 kB gzip; último push no repositório em 2026-01-16.

  Fontes: [npm d3-zoom](https://www.npmjs.com/package/d3-zoom), [npm @panzoom/panzoom](https://www.npmjs.com/package/@panzoom/panzoom), [npm panzoom](https://www.npmjs.com/package/panzoom), [npm svg-pan-zoom](https://www.npmjs.com/package/svg-pan-zoom), [Bundlephobia](https://bundlephobia.com/package/d3-zoom), [GitHub bumbu/svg-pan-zoom](https://github.com/bumbu/svg-pan-zoom)
- **FATO:** O `d3-zoom` "is agnostic about the DOM, so you can use it with HTML, SVG, or Canvas". Em SVG: `g.attr("transform", transform)`. Em Canvas: `context.translate(t.x, t.y); context.scale(t.k, t.k)`, e a translação vem antes da escala — [d3-zoom](https://d3js.org/d3-zoom)
- **FATO:** O `wheelDelta` padrão do d3-zoom é `-event.deltaY * (deltaMode === 1 ? 0.05 : deltaMode ? 1 : 0.002) * (event.ctrlKey ? 10 : 1)`. A escala é multiplicada por 2^Δ. O filtro padrão é `(!event.ctrlKey || event.type === 'wheel') && !event.button`. Os padrões são `scaleExtent [0, ∞]` e `translateExtent` infinito; os limites são respeitados na interação, mas não ao definir `transform` diretamente. `transform.invert(p) = [(x − tx)/k, (y − ty)/k]` converte tela em mundo. Os listeners de toque só são registrados se `navigator.maxTouchPoints || "ontouchstart" in this` — [d3-zoom](https://d3js.org/d3-zoom)
- **FATO:** No Chrome e no Firefox, a pinça do trackpad chega como evento `wheel` com `ctrlKey = true`, mesmo sem a tecla pressionada. É uma convenção de fato, não um padrão. Para impedir o zoom da página é preciso `preventDefault()` num listener com `{ passive: false }`. Uma proposta de 2025 pede para descontinuar esse comportamento. Um bug antigo do WebKit (2015) relatava que a pinça no Safari não gerava evento JS — [MDN, wheel event](https://developer.mozilla.org/en-US/docs/Web/Events/wheel); [Chromium PSA](https://groups.google.com/a/chromium.org/g/chromium-dev/c/L_kaBhYFi5U/m/RIMFBx12dJoJ); [WebKit bug 145214](https://bugs.webkit.org/show_bug.cgi?id=145214); [W3C public-webapps, 2025-05](https://lists.w3.org/Archives/Public/public-webapps-github/2025May/0106.html)
- **FATO:** O `react-planner` usava `react-svg-pan-zoom` 2.18.0 como câmera do visualizador 2D — [package.json do react-planner](https://github.com/cvdlab/react-planner/blob/master/package.json)

### Inferences
- **OPINIÃO:** Para o PyGridPlan, recomendo uma **câmera própria** com estado `{x, y, k}` aplicado num único `<g transform="translate(x,y) scale(k)">`, ou manipulando o `viewBox`. Os motivos:
  1. O zoom em torno do cursor é uma fórmula de 3 linhas: `k' = clamp(k·2^Δ)`; `x' = px − (px − x)·k'/k`, e o mesmo para `y`.
  2. O snap e as cotas precisam do `k` atual em todo lugar: a tolerância é dividida por `k` (ver seção 4).
  3. Sem dependência nova. Isso segue a regra do CLAUDE.md de não adicionar dependências sem justificativa.

  O `d3-zoom` é a alternativa direta, se a câmera própria ficar complicada: ele já resolve inércia de toque, duplo clique e limites, e custa ~18 kB gzip.
- **HIPÓTESE:** Use `transform` num `<g>`, e não `viewBox`, se o mesmo `<svg>` precisar de camadas em espaço de tela, como uma régua fixa, a mira do cursor ou o HUD. Com `viewBox`, tudo escala junto. Os dois funcionam; a diferença é organizacional.
- **OPINIÃO:** `@panzoom/panzoom` e `panzoom` aplicam `transform` CSS num elemento. Isso é bom para "zoom em imagem", mas ruim para CAD, porque a conversão tela→mundo para snap fica por conta do app, e os textos e traços escalam junto, salvo com `non-scaling-stroke`. O `svg-pan-zoom` está estagnado (último release há ~2 anos), então não vale como dependência nova.
- **HIPÓTESE:** Mapa de gestos sugerido no estilo AutoCAD:
  - roda: zoom em torno do cursor;
  - arrasto com o botão do meio, ou com espaço + arrasto: pan;
  - pinça do trackpad (`wheel` + `ctrlKey`): zoom;
  - dois dedos no trackpad (`wheel` sem `ctrlKey` e com `deltaX`): pan.

  Não dá para distinguir com certeza uma "roda de mouse" de um "trackpad sem ctrl". É uma heurística conhecida, mas imperfeita.

### Gaps
- O comportamento atual (2026) da pinça no Safari macOS não foi verificado nesta rodada. O bug do WebKit citado é de 2015.

## 3. Bibliotecas: versões atuais, licença, manutenção, bundle e recursos prontos

### Takeaway
Nenhuma biblioteca de uso geral traz "porta deslizando ao longo da parede com snap em pontos sugeridos". Esse comportamento é código de domínio em qualquer opção. O Konva (Canvas) é a biblioteca mais completa para arrasto, transformadores e camadas. Fabric e Paper também estão ativos. O tldraw **não** é open source para uso em produção: exige chave de licença desde o 4.0. O Excalidraw é MIT, mas é um app, não uma biblioteca de CAD.

### Cited Findings
- **FATO (registro npm + Bundlephobia + GitHub, 2026-11-22):**

| Pacote | Versão (data) | Licença | min+gzip | Atividade |
|---|---|---|---|---|
| `konva` | 10.10.0 (2026-11-20) | MIT (npm) | ~57 kB | push 2026-11-20, 15,0k estrelas |
| `react-konva` | 19.3.2 (2026-10-15) | MIT | — | ativo |
| `fabric` | 7.4.0 (2026-05-18) | MIT | ~92 kB | push 2026-11-17, 31,6k estrelas |
| `paper` | 0.17.0 (2026-11-03) | MIT (npm) | ~122 kB | push 2026-11-19 |
| `pixi.js` | 8.23.0 (2026-11-11) | MIT | ~282 kB | ativo |
| `two.js` | 0.8.24 (2026-08-29) | MIT | ~49 kB | push 2026-11-17 |
| `@svgdotjs/svg.js` | 3.2.8 (2026-08-04) | MIT (npm) | ~30 kB | push 2026-08-04 |
| `d3` | 7.9.2 (2026-11-03) | ISC | — | ativo |
| `roughjs` | 4.6.6 (2023-11-20) | MIT | — | sem release há 3 anos |
| `jsxgraph` | 1.14.3 (2026-11-06) | MIT ou LGPL-3.0-or-later | — | ativo |
| `makerjs` | 0.19.2 (2026-01-27) | Apache-2.0 | — | ativo, de baixa cadência |
| `tldraw` | 5.6.2 (2026-11-20) | "SEE LICENSE IN LICENSE.md" | — | push 2026-11-20, 51,5k estrelas |
| `@excalidraw/excalidraw` | 0.18.1 (2026-04-20) | MIT | — | push 2026-11-21, 136k estrelas |
| `dxf-viewer` | 1.0.51 (2026-11-11) | MPL-2.0 | — | ativo |
| `replicad` | 1.2.1 (2026-11-06) | MIT | — | ativo |
| `three` | 0.187.0 (2026-10-30) | MIT | — | ativo |
| `@flatten-js/core` | 1.6.15 (2026-10-25) | MIT | — | ativo |

  Fontes: [npm konva](https://www.npmjs.com/package/konva), [npm fabric](https://www.npmjs.com/package/fabric), [npm paper](https://www.npmjs.com/package/paper), [npm pixi.js](https://www.npmjs.com/package/pixi.js), [npm two.js](https://www.npmjs.com/package/two.js), [npm @svgdotjs/svg.js](https://www.npmjs.com/package/@svgdotjs/svg.js), [npm roughjs](https://www.npmjs.com/package/roughjs), [npm jsxgraph](https://www.npmjs.com/package/jsxgraph), [npm makerjs](https://www.npmjs.com/package/makerjs), [npm tldraw](https://www.npmjs.com/package/tldraw), [npm @excalidraw/excalidraw](https://www.npmjs.com/package/@excalidraw/excalidraw), [npm dxf-viewer](https://www.npmjs.com/package/dxf-viewer), [npm replicad](https://www.npmjs.com/package/replicad), [npm three](https://www.npmjs.com/package/three), [npm @flatten-js/core](https://www.npmjs.com/package/@flatten-js/core), [Bundlephobia](https://bundlephobia.com/package/konva)
- **FATO:** A API do GitHub mostra licença "NOASSERTION" para os repositórios konva, paper.js e svg.js, enquanto o npm declara MIT. Isso indica um arquivo de licença que o GitHub não reconheceu automaticamente, não uma licença diferente; vale ler o LICENSE antes de adotar — [API GitHub konvajs/konva](https://api.github.com/repos/konvajs/konva)
- **FATO:** A licença do tldraw ("The tldraw License", tldraw, Inc.) proíbe uso em "Production Environments" sem chave de licença de teste (trial) ou comercial, e permite uso em desenvolvimento, teste e staging não públicos. A licença inclui medidas técnicas para garantir a exibição da marca d'água — [tldraw LICENSE.md](https://github.com/tldraw/tldraw/blob/main/LICENSE.md)
- **FATO:** Desde o tldraw SDK 4.0 (setembro de 2025), produção exige chave de licença. Sem chave, o editor registra erros e para de renderizar depois de 5 s. A chave "hobby" é concedida a critério da empresa e mostra a marca "made with tldraw". A marca d'água tinha surgido no 3.0. O modelo antigo, "grátis com marca d'água", está desatualizado — [tldraw, License key](https://tldraw.dev/sdk-features/license-key); [tldraw SDK 4.0](https://tldraw.dev/blog/tldraw-sdk-4-0); [AlternativeTo, 2025-09](https://alternativeto.net/news/2025/9/tldraw-sdk-4-0-adds-five-new-starter-kits-cli-tool-and-enforces-licensing-changes); [tldraw, 20 things](https://tldraw.dev/blog/20-things-i-wish-ai-chatbots-knew-about-tldraw)
- **FATO:** O Excalidraw renderiza em Canvas, com componentes `StaticCanvas`, `InteractiveCanvas` e `NewElementCanvas`. Ele depende de `roughjs` 4.6.4, para o traço "à mão", e de `perfect-freehand` 1.2.0 — [repositório Excalidraw, components/canvases](https://github.com/excalidraw/excalidraw/tree/master/packages/excalidraw/components/canvases); [package.json](https://github.com/excalidraw/excalidraw/blob/master/packages/excalidraw/package.json)

### Inferences
- **HIPÓTESE (conhecimento prévio, não reconferido nesta rodada):**
  - O Konva oferece `Konva.Transformer` (alças de redimensionar e girar), `draggable` e `dragBoundFunc` (restringe o arrasto, por exemplo a uma reta), `hitStrokeWidth` (tolerância de clique maior que o traço visível) e camadas (`Layer`).
  - O Fabric tem "controls" por objeto e eventos `object:moving`.
  - O Paper.js tem `project.hitTest(point, {tolerance, stroke, segments})` e `Path.getNearestPoint`.
  - O PixiJS 8 usa `eventMode` e `hitArea`.
  - O SVG.js tem plugins `svg.draggable.js` e `svg.panzoom.js`.

  Confirmar na documentação de cada um antes de usar.
- **OPINIÃO:**
  - `dragBoundFunc` do Konva mapeia bem a "porta presa à parede". Mesmo assim, a projeção, o snap nas sugestões e a abertura da parede continuam sendo código de domínio, e esse código é o mesmo em SVG puro.
  - Uma biblioteca só se paga se trouxer muitos recursos genéricos (seleção múltipla, transformador e camadas). Para o M2, só o arrasto restrito e o hover são essenciais.
- **OPINIÃO:**
  - **Descartar** o tldraw: licença comercial com chave obrigatória, conflitante com um projeto offline de portfólio. Ele é aceitável só como referência de arquitetura, lendo o código.
  - **Descartar** o Excalidraw como base: é MIT, mas é um app de quadro branco, com estética "rough" e modelo de dados de quadro branco. Serve como referência de snapping e de arquitetura com dois canvases.
  - Rough.js, JSXGraph (geometria dinâmica escolar), Maker.js (CAM, peças para corte), replicad (CAD 3D B-rep) e dxf-viewer (visualizador WebGL de DXF, MPL-2.0) não se aplicam ao editor do M2.
  - O `dxf-viewer` poderia servir para pré-visualizar o DXF exportado. Isso é opcional e fica fora do M2.
- **OPINIÃO:** O `@flatten-js/core` (MIT, geometria 2D: segmentos, projeção, distâncias, operações booleanas) é a única dependência de geometria que talvez valha no front. Para o caso 23.3 basta um produto escalar, e é melhor não adicioná-lo.

### Gaps
- Não verifiquei, nas páginas oficiais, o tamanho do `tldraw` e do `@excalidraw/excalidraw` em gzip, nem a data exata do release 4.0 do tldraw. A data de setembro de 2025 vem das notícias de AlternativeTo e x-cmd.
- A versão `latest` do Excalidraw no npm (0.18.1, abril de 2026) é antiga em relação ao repositório, que tem push de 2026-11-21. Não verifiquei quais tags de pré-release estão em uso.

## 4. Snapping e cotas: padrões e como editores open source implementam

### Takeaway
O padrão de mercado está verificado no código do tldraw e do Excalidraw: a **tolerância de snap é fixa em pixels de tela (8 px) e é dividida pelo zoom** para obter a tolerância em unidades do mundo. O react-planner, editor de plantas em SVG, organiza o snap em tipos com prioridade (ponto, reta, segmento, grade, guia) e modela portas e janelas como "holes" com `offset` paramétrico ao longo da parede. Esse é exatamente o modelo de que o caso 23.3 precisa.

### Cited Findings
- **FATO:** O tldraw calcula `getSnapThreshold() = options.snapThreshold / editor.getZoomLevel()`, com `snapThreshold: 8` como padrão. Também usa `hitTestMargin: 4.5` (4 em ponteiro "coarse") e um limiar de arrasto de 4 px (`dragDistanceSquared: 16`; 6 px em touch) — [tldraw SnapManager.ts](https://github.com/tldraw/tldraw/blob/main/packages/editor/src/lib/editor/managers/SnapManager/SnapManager.ts); [tldraw options.ts](https://github.com/tldraw/tldraw/blob/main/packages/editor/src/lib/options.ts)
- **FATO:** O Excalidraw define `SNAP_DISTANCE = 8` e `getSnapDistance(zoom) = SNAP_DISTANCE / zoom`, comentado como "snap distance with zoom value taken into consideration". Usa isso em vários pontos do snapping — [excalidraw snapping.ts](https://github.com/excalidraw/excalidraw/blob/master/packages/excalidraw/snapping.ts)
- **FATO:** O react-planner tem `src/utils/snap.js` com os tipos `SNAP_POINT`, `SNAP_LINE`, `SNAP_SEGMENT`, `SNAP_GRID` e `SNAP_GUIDE`, uma máscara padrão (grade desligada) e classes `PointSnap`, `LineSnap` e `LineSegmentSnap`. Cada classe tem `radius`, `priority` e `nearestPoint(x, y)`, que devolve o ponto mais próximo e a distância; `LineSegmentSnap` usa `closestPointFromLineSegment` — [react-planner snap.js](https://github.com/cvdlab/react-planner/blob/master/src/utils/snap.js)
- **FATO:** O modelo do react-planner tem `Vertex`, `Line` (parede, com listas `vertices` e `holes`), `Hole` (`offset`, `line`), `Area`, `Item`, `Layer`, `Group` e `Scene`. Na renderização 2D (`line.jsx`), cada hole é desenhado num `<g transform="translate(length * hole.offset, 0)">` dentro do `<g>` da parede, que já está transladado e girado (`translate(x1,y1) rotate(angle)`). A parede selecionada mostra uma `Ruler`, a cota. Os elementos carregam `data-prototype`, `data-id` e `data-selected` para o hit-testing por DOM — [react-planner models.js](https://github.com/cvdlab/react-planner/blob/master/src/models.js); [line.jsx](https://github.com/cvdlab/react-planner/blob/master/src/components/viewer2d/line.jsx)
- **FATO:** O visualizador 2D do react-planner tem componentes `ruler.jsx`, `rulerX.jsx`, `rulerY.jsx`, `snap.jsx`, `grids/` e `export.js`, e depende de `three` 0.94 para o 3D — [diretório viewer2d](https://github.com/cvdlab/react-planner/tree/master/src/components/viewer2d); [package.json](https://github.com/cvdlab/react-planner/blob/master/package.json)

### Inferences
- **OPINIÃO:** Para o PyGridPlan, o snap deve ter **prioridades explícitas** (como no react-planner) e **tolerância em pixels de tela** (como no tldraw e no Excalidraw). Ordem sugerida para a porta: ponto sugerido (raio ~12 px) > extremidade ou centro da parede (8 px) > grade de 100 mm ao longo da parede (sempre ativa, sem raio) > posição livre (quando o snap for desligado com Alt ou Shift).
- **OPINIÃO:** Cotas no estilo AutoCAD em SVG:
  - linha de cota deslocada da aresta por um offset fixo **em pixels de tela**, para que a distância visual se mantenha em qualquer zoom: `offset_mundo = offset_px / k`;
  - linhas de extensão;
  - terminadores (tick oblíquo, como no AutoCAD) via `<marker>` ou `<path>`;
  - `<text>` com `paint-order: stroke` para legibilidade no fundo escuro.

  O texto pode ficar em espaço de tela: posicione `x, y` pelo mundo e aplique `scale(1/k)` local, ou ponha numa camada HUD fora do `<g>` da câmera. O valor da cota vem do modelo (mm) e nunca de pixels.
- **HIPÓTESE:** As guias magnéticas no estilo Figma (alinhamento com bordas de outros cômodos) são o mesmo algoritmo com candidatos 1D por eixo: colete os x e y de bordas dos objetos visíveis, ache o mais próximo dentro do limiar/k e desenhe a guia. tldraw e Excalidraw fazem algo desse tipo (o nome `SNAP_GUIDE` do react-planner aponta para isso). Não é necessário no caso 23.3.

### Gaps
- Não li o código de snap do Penpot nem do draw.io. O Penpot é MPL-2.0 e tem push de 2026-11-22; o draw.io é Apache-2.0 e tem push de 2026-11-17 ([API GitHub penpot](https://api.github.com/repos/penpot/penpot), [API GitHub drawio](https://api.github.com/repos/jgraph/drawio)). Não confirmei a tecnologia de renderização atual do Penpot, que segundo conhecimento prévio está migrando para um renderizador WASM/Skia (não verificado).

## 5. Animação "com propósito": SVG + CSS/WAAPI x loop de redesenho no Canvas

### Takeaway
Em SVG, animações curtas de estado (porta surgindo, parede abrindo, sugestão pulsando) saem com CSS transitions ou com a Web Animations API sobre `transform`/`opacity`, sem loop próprio. Em Canvas, toda animação exige um loop de `requestAnimationFrame` com interpolação manual e redesenho da cena ou de uma camada.

### Cited Findings
- **FATO:** A yWorks cita, como vantagem do SVG, "hardware accelerated CSS effects and filters" e CSS3 transitions e animations em elementos SVG — [yWorks](https://www.yworks.com/blog/svg-canvas-webgl)
- **FATO:** O d3-zoom permite transições programáticas de câmera (`zoom.transform` com `transition`, minimizando o movimento em torno de um ponto). Útil para "enquadrar a planta escolhida" — [d3-zoom](https://d3js.org/d3-zoom)

### Inferences
- **HIPÓTESE (técnica proposta, não testada):** Para a parede "abrindo" ao inserir uma porta, há duas opções:
  1. Animar com `transform: scaleX(0→1)` um retângulo da cor do fundo (ou o próprio símbolo da porta) centrado no ponto, com `transform-box: fill-box; transform-origin: center`, em 150–200 ms. Ao fim, trocar pela geometria definitiva (os pedaços de parede já recortados).
  2. Animar o atributo do recorte via WAAPI.

  CSS não interpola o atributo `points` de um polígono. A propriedade CSS `d` é animável no Chromium e no Firefox, mas o suporte não foi verificado nesta rodada. Por isso a opção 1 (transform no overlay) é a mais segura.
- **OPINIÃO:**
  - Sugestões em cor diferente com pulso leve: `@keyframes` de `opacity` ou `stroke-width`, com `prefers-reduced-motion: reduce` desligando a animação.
  - "Aceitar todas": animar em sequência (stagger de 30–50 ms por porta) para mostrar o que mudou. Esta é a animação "com propósito".
- **OPINIÃO:** No Konva há `Konva.Tween` e `node.to()` (conhecimento prévio, não verificado), que resolvem o equivalente no Canvas. Ainda assim, cada quadro redesenha a camada inteira.

### Gaps
- O suporte atual de animação da propriedade CSS `d` em Safari, Chrome e Firefox não foi verificado.

## 6. Editores de planta web open source: o que existe, estado e lições

### Takeaway
Os editores de planta open source conhecidos estão parados ou usam stacks legados: react-planner (SVG + three.js, último push em abril de 2024), blueprint3d (último push em janeiro de 2021) e FloorspaceJS (Vue 2 + d3 v4). O Arcada (React + PixiJS) é o único com atividade em 2026. A lição útil é de modelo de dados, não de código: parede como segmento entre vértices, aberturas com offset paramétrico na parede e cotas derivadas.

### Cited Findings
- **FATO:**
  - `cvdlab/react-planner`: MIT, 1.493 estrelas, último push em 2024-04-20, não arquivado. Usa Redux + Immutable.js, exige React ≥ 16 e parte do 2D para gerar o 3D. Depende de `react-svg-pan-zoom` 2.18.0 e `three` 0.94.0 — [API GitHub](https://api.github.com/repos/cvdlab/react-planner); [README](https://github.com/cvdlab/react-planner); [package.json](https://github.com/cvdlab/react-planner/blob/master/package.json)
  - `furnishup/blueprint3d`: MIT, 2.006 estrelas, último push em 2021-01-20 — [API GitHub](https://api.github.com/repos/furnishup/blueprint3d)
  - `mehanix/arcada`: Apache-2.0, 433 estrelas, último push em 2026-10-14. React + Pixi.js + Zustand + Mantine, backend Express + MongoDB, motor de planta "custom built". Tem paredes, móveis, portas e janelas, ferramenta de medição, vários andares, impressão e salvar/carregar; é um TCC de graduação — [GitHub arcada](https://github.com/mehanix/arcada)
  - FloorspaceJS: editor 2D de geometria para modelagem energética de edifícios (NREL, desenvolvido pela Devetry), com esquema JSON próprio. O repositório oficial agora responde como `NatLabRockies/floorspace.js` (redirecionado de `NREL/floorspace.js`), com último push em 2026-02-09. Usa Vue 2.6, Vuex 2, d3 ^4.4 e d3-selection ^1.1 — [DOE, OpenStudio](https://www.energy.gov/eere/buildings/articles/openstudio-world-flat); [NREL, preprint](https://www.nrel.gov/docs/fy18osti/70491.pdf); [package.json](https://github.com/NatLabRockies/floorspace.js/blob/develop/package.json)
- **FATO:** O GoJS publica um exemplo "FloorPlanner" com ferramenta de desenho de parede. O GoJS é uma biblioteca comercial — [GoJS FloorPlanner (CDN)](https://cdn.jsdelivr.net/npm/gojs@2.1.30/projects/floorplanner/FloorPlanner.html)

### Inferences
- **OPINIÃO:** Lições para o PyGridPlan:
  1. **Abertura = (wall_id, offset ao longo da parede, largura)**, como o `Hole{offset, line}` do react-planner. A geometria do vão é derivada: o motor Python, fonte da verdade, recorta a parede.
  2. **Parede em sistema local** (`translate + rotate`), em que o eixo x é o eixo da parede. A projeção do cursor vira só "pegar o x local", e a porta é desenhada em `translate(offset, 0)`.
  3. Atributos `data-*` em cada elemento SVG para despachar eventos e para testes.
  4. Snap tipado com prioridade.
  5. Cotas como componente derivado, mostradas na seleção.

  O que **não** copiar: estado imutável no front como fonte da verdade (Redux + Immutable). No PyGridPlan o front só guarda o estado transitório (hover, prévia, câmera) e envia comandos.
- **OPINIÃO:** Nenhum desses projetos serve de dependência. Todos estão parados, acoplados a stacks antigas (React 16, three 0.94, Vue 2, d3 v4) ou exigem backend.

### Gaps
- Não verifiquei se o FloorspaceJS desenha em SVG via d3; a dependência de d3 sugere que sim. Também não verifiquei como o Arcada faz snap e cotas, porque o README não descreve isso.

## 7. Caso de teste 23.3 implementado nas 2–3 melhores opções

### Takeaway
As três candidatas são: **(A) SVG puro com câmera própria**, a recomendada; (B) Konva em Canvas 2D, a alternativa viável; e (C) PixiJS em WebGL, não recomendada para o M2. O núcleo do caso 23.3 é idêntico nas três: projeção escalar do cursor na parede, limitação do centro ao intervalo válido, snap com raio em pixels de tela dividido pelo zoom e recorte 1D de intervalos na parede. O que muda é o hit-testing e a forma de redesenhar.

### Cited Findings
- **FATO:** O padrão de raio em pixels de tela dividido pelo zoom é o mesmo de tldraw (8/zoom) e Excalidraw (8/zoom) — [tldraw SnapManager.ts](https://github.com/tldraw/tldraw/blob/main/packages/editor/src/lib/editor/managers/SnapManager/SnapManager.ts); [excalidraw snapping.ts](https://github.com/excalidraw/excalidraw/blob/master/packages/excalidraw/snapping.ts)
- **FATO:** O react-planner posiciona aberturas por `offset` relativo ao comprimento da parede, dentro do grupo local da parede — [line.jsx](https://github.com/cvdlab/react-planner/blob/master/src/components/viewer2d/line.jsx)
- **FATO:** `non-scaling-stroke` mantém a espessura do traço constante em qualquer zoom. Aplicado a um traço invisível de "hit", isso gera uma tolerância de clique constante em pixels de tela — [MDN vector-effect](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/vector-effect)
- **FATO:** No Konva, o hit-testing funciona por cor única num canvas oculto e fica desligado durante o arrasto por padrão — [Konva Performance](https://konvajs.org/docs/performance/All_Performance_Tips.html); [Shape.ts](https://github.com/konvajs/konva/blob/master/src/Shape.ts)

### Inferences

**Núcleo comum (independente da renderização). HIPÓTESE de projeto, conferível por testes unitários:**
- **Dados recebidos do motor:**
  - paredes `{id, a:{x,y}, b:{x,y}, espessura}` em mm;
  - aberturas `{id, wall_id, s, largura, tipo}`, em que `s` é a distância em mm do ponto `a` ao centro da abertura;
  - sugestões `{id, wall_id, s, largura, motivo}`.
- **Projeção do cursor na parede**, com o cursor P já convertido para o mundo:
  - `u = (b − a)/L`, onde L = |b − a|;
  - `s = (P − a)·u`;
  - `d = |(P − a) × u|`, a distância perpendicular.
  - O centro da porta é limitado ao intervalo válido: `s = clamp(s, w/2 + folga, L − w/2 − folga)`, onde `folga` é a distância mínima ao canto, um dado do motor.
  - Na grade de 100 mm, use `s = round(s/100)·100` quando não houver snap de sugestão.
- **Hit da parede:** a parede está sob o cursor se `d ≤ espessura/2 + R_hit/k` e se `s` cru está em `[0, L]`. Aqui `R_hit` ≈ 6–8 px e `k` é o zoom em px/mm.
- **Snap na sugestão:** entre as sugestões da mesma parede, pegue a de menor `|s_i − s|`. Ela vence se `|s_i − s|·k ≤ R_snap`, com `R_snap` ≈ 12 px. Assim, o raio visual é o mesmo em qualquer zoom. Com Alt pressionado, o snap é desligado (posição livre ou grade).
- **Validade da prévia:** a porta não pode sobrepor outra abertura (teste de intervalos `[s−w/2, s+w/2]`) nem o canto. Uma prévia inválida aparece em vermelho e o clique fica bloqueado. A regra final é do motor, que valida o comando.
- **Vão da parede:** subtração de intervalos 1D. `[0, L] − ∪[s_j − w_j/2, s_j + w_j/2]` resulta em pedaços `[t0, t1]`, e cada pedaço vira um retângulo de espessura `e` no sistema local da parede. Isso é determinístico e testável. O motor deve devolver a mesma geometria, que é a fonte da verdade, e o front só a antecipa de forma otimista.
- **Fluxo do clique:** o front envia o comando `AddOpening{wall_id, s, largura, tipo, from_suggestion?}`. Ele aplica uma prévia otimista com a animação de abertura e reconcilia com a resposta do motor; se o motor rejeitar, reverte com a mensagem no console ao vivo. "Aceitar todas" envia um único comando em lote, `AcceptSuggestions{ids}`, e anima em stagger.

**(A) SVG puro + câmera própria (recomendada). OPINIÃO:**
- **Estrutura:**
  ```
  <svg>
    <g id="camera" transform="translate(x,y) scale(k)">
      grade, lote, cômodos, paredes, aberturas, sugestões
    </g>
    <g id="hud">cotas em espaço de tela opcional, tooltip</g>
  </svg>
  ```
- **Cada parede** é um `<g data-wall-id transform="translate(ax,ay) rotate(θ)">` com dois filhos:
  1. os retângulos visíveis dos pedaços, com `fill: var(--wall)`;
  2. um `<line x1=0 x2=L>` de hit com `stroke="transparent"`, `stroke-width` de (espessura em px + 2·R_hit), `vector-effect: non-scaling-stroke` e `pointer-events: stroke`.

  Com isso, o navegador faz o hit-testing com tolerância constante em pixels, sem código. Um detalhe: com `non-scaling-stroke`, a largura é dada em px de tela, então a espessura da parede tem de ser convertida para px a cada mudança de zoom; outra opção é desenhar só o hit em px e checar `d` no código.
- **Eventos:**
  - `pointerenter` e `pointerleave` no hit marcam a parede ativa e definem o estado CSS `.wall--hover`;
  - `pointermove` (delegado no `<svg>`, com `requestAnimationFrame` para limitar a ~60 Hz) converte o cursor para o mundo, projeta, aplica o snap e atualiza **um único** `<rect id="door-preview">`. Essa atualização mexe só no transform `translate(ax,ay) rotate(θ) translate(s − w/2, −e/2)`.
  - A conversão tela→mundo é a inversa da câmera: `(px − x)/k`. A outra opção é `DOMPoint.matrixTransform(el.getScreenCTM().inverse())` (API padrão do DOM; documentação não reconsultada nesta rodada).
- **Estados:**
  - as sugestões são `<rect class="suggestion">` com outra cor (`--suggest`) e pulso CSS;
  - quando o snap engata, a prévia ganha `.preview--snapped` (cor da sugestão e um "clique" visual de escala 1.05→1);
  - um `<text>` pequeno mostra `s` em mm, a distância até a quina mais próxima, como cota temporária.
- **Desempenho:** por quadro, só muda o transform de 1 nó e uma classe CSS; o resto da cena não é tocado. Com menos de ~1.500 nós, sobra margem segundo os benchmarks da seção 1.
- **Testes:**
  - Vitest para a função pura de projeção, snap e intervalos;
  - Playwright com `page.hover('[data-wall-id="w12"]', {position})`, verificando a prévia por `data-snapped="true"` e o clique pelo surgimento de `[data-opening-id]`;
  - screenshot só para a conferência visual.

**(B) Konva / Canvas 2D (alternativa). OPINIÃO:**
- **Estrutura:** `Stage` com 2 ou 3 `Layer`: estática (grade, lote, cômodos e paredes, com `listening(false)` onde possível); interativa (hits das paredes e sugestões); HUD (prévia e cota temporária). Isso respeita o aviso de "no máximo 5 camadas".
- **Câmera:** `stage.scale({x:k, y:k})` e `stage.position()`; a conversão tela→mundo usa `stage.getAbsoluteTransform().copy().invert().point(pointer)` (API conhecida, não reconferida).
- **Hit da parede:** `Konva.Line` com `hitStrokeWidth` largo (conhecimento prévio). Como esse valor está em unidades do mundo, é preciso recalculá-lo a cada zoom (`R_hit/k`). A outra saída é desligar o hit nativo e fazer uma busca linear manual: para ~100–300 paredes, testar a distância ponto-segmento é trivial (menos de 0,1 ms; hipótese).
- **Prévia:** um `Konva.Rect` na camada HUD. A cada `pointermove`, aplique projeção e snap e chame `layer.batchDraw()` só no HUD.
- **Vão:** redesenhe os pedaços da parede na camada estática quando uma abertura é confirmada.
- **Animação:** `Konva.Tween` (conhecimento prévio).
- **Custos em relação à opção A:**
  - texto das cotas rasterizado, com redesenho a cada zoom para ficar nítido;
  - tema via CSS só por leitura de variáveis em JS;
  - sem DOM para acessibilidade nem para testes, o que exige expor o estado em `window.__scene`, ou equivalente, para o Playwright;
  - exportação SVG separada (o Konva exporta imagem, não SVG vetorial; hipótese).
- **Ganhos:** `draggable` + `dragBoundFunc` e `Transformer` prontos, úteis se o M2 incluir arrastar e redimensionar cômodos.

**(C) PixiJS / WebGL (não recomendada para o M2). OPINIÃO:** a estrutura seria `Container` de câmera, `Graphics` para as paredes, `eventMode='static'` e `hitArea` nas paredes (conhecimento prévio). A lógica de projeção e snap é idêntica. Os contras: texto via `BitmapText`/`Text` (o ponto fraco documentado do WebGL), ~282 kB gzip, nada de CSS, acessibilidade e testes só por estado exposto. Só faria sentido se o mesmo canvas fosse depois reaproveitado no 3D, mas o 3D do projeto vem depois e provavelmente usaria three.js, não Pixi.

**Recomendação. OPINIÃO:**
- SVG puro, com câmera própria (ou `d3-zoom`), hit por traço invisível com `non-scaling-stroke` e núcleo geométrico puro em TypeScript testado com Vitest.
- Nenhuma biblioteca de cena no M2.
- Reavaliar o Konva só se o escopo do M2 crescer para edição livre de cômodos com alças de transformação.

### Gaps
- Nenhuma das abordagens foi prototipada nesta rodada. Os tempos por quadro são hipóteses e devem ser medidos num protótipo, com ~20 cômodos, 40 sugestões e o DevTools Performance aberto.
- Não verifiquei se `pointer-events: stroke` com `non-scaling-stroke` usa a largura de tela no hit-testing em todos os navegadores. Testar no Chromium, no Firefox e no WebKit via Playwright antes de depender disso. Plano B: tolerância calculada no código (`d·k ≤ R_hit`).
- A API exata de `hitStrokeWidth`, `dragBoundFunc` e `Transformer` do Konva 10 não foi reconferida na documentação.
