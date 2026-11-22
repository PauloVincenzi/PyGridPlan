# Produtos e artigos sobre geração interativa (human-in-the-loop) de plantas residenciais

Notas de pesquisa para o M2 do PyGridPlan. Data da coleta: 2026-11-22. Convenção: **FATO** = afirmação com fonte citada; **HIPÓTESE/OPINIÃO** = inferência do pesquisador, sem fonte direta. Quando a fonte é secundária (blog de review, agregador, marketing), isso é dito explicitamente.

## 1. Produtos: o que existe em 2026, que interação oferecem e o que se sabe dos algoritmos

### Takeaway
Os produtos comerciais com geração de layout ativos em 2026 (Finch3D, Maket, TestFit, Higharc, Autodesk Forma) seguem o mesmo padrão: o usuário define o programa e pesos/metas, o sistema gera **várias opções pontuadas** e o usuário filtra ou escolhe e depois edita. Nenhum documenta o algoritmo em detalhe. Só o Finch3D se declara "baseado em grafo + otimização", que é o mais próximo da abordagem do PyGridPlan.

### Cited Findings

**Finch3D (Suécia). Status: ativo (2026), com acesso restrito.**
- FATO: nasceu como ferramenta interna do escritório Wallgren Arkitekter. Um review de 2026 descreve a ferramenta como baseada em tecnologia de grafos, e não em geração de imagem. — [illustrarch, review 2026 (secundária)](https://illustrarch.com/articles/75056-finch3d-review.html)
- FATO: a empresa descreve duas tecnologias centrais, "um motor de regras baseado em grafo e um sistema de IA que aprende para analisar e gerar plantas". Segundo o fundador, o grafo é gerado automaticamente (o usuário não o desenha) e os algoritmos de otimização levam em conta as regras do grafo. — [AEC Magazine, "Finch3D starts to sing"](https://aecmag.com/ai/finch3d-starts-to-sing/)
- FATO: a geração de pavimento parte do unit mix, de restrições de escada e de **pesos** (squareness, daylight, área). As opções são pontuadas por daylight, eficiência de CO2, conformidade e adaptabilidade. Clientes enterprise definem bibliotecas próprias de plantas, mobiliário, regras de grafo e checagens de conformidade. — [AEC Magazine](https://aecmag.com/ai/finch3d-starts-to-sing/)
- FATO: a versão "Generate Floor Plate 2.0" saiu em setembro de 2024 e considera profundidade do edifício e dupla orientação. Na época, o acesso era só por convite. — [Architosh, 2024](https://architosh.com/2024/09/finch3d-advances-ai-based-floor-plan-generator/)
- FATO: o fluxo roda como plugin em Rhino, Revit e Archicad. No Revit, o usuário clica numa unidade, escolhe as paredes de entrada e recebe opções pontuadas. — [Finch docs, Revit](https://docs.finch3d.com/courses/finch-101/finch-101-generating-floor-plans-in-revit); [Finch docs, Archicad](https://docs.finch3d.com/courses/finch-101/finch-101-generating-floor-plans-in-archicad)
- FATO (fonte secundária): a geração de plantas de unidade com IA está limitada a "clientes estratégicos" (tier enterprise/AI). O preço citado é a partir de €14.500/ano com 3 assentos. — [tooliverse (secundária)](https://tooliverse.ai/tools/finch3d)
- FATO (secundária, não verificada no material oficial): um blog diz que as opções podem ser filtradas por eficiência líquido/bruto, acesso a luz natural e distância de circulação, e que cada opção sai cotada, com áreas, paredes e portas. — [archgyan (secundária)](https://archgyan.com/finch-3d-ai-floor-plan-generation-architects/)

**Maket.ai (Canadá). Status: ativo (2026).**
- FATO (secundária): gera plantas residenciais a partir de cômodos, área, forma e estilo, em menos de um minuto, com 1 a 4 pavimentos (multipavimento só no plano pago). O plano gratuito dá 30 créditos e cada pavimento gerado custa 20 créditos. O plano "Homeowner" custa US$ 20/mês. — [illustrarch review (secundária)](https://illustrarch.com/articles/design-softwares/73352-maket-ai-review.html); [formas.ai (secundária)](https://www.formas.ai/articles/maket-ai)
- FATO: oferece edição por chat e reconhecimento de planta enviada (upload), só residencial. O próprio Maket diz que o reconhecedor "ainda está melhorando". — [blog Maket](https://www.maket.ai/blog/ai-floorplan-recognizer-upload-an-existing-plan-get-right-to-editing)
- FATO (secundária): o "Maket 2.0" teria sido lançado em outubro de 2026. — [progressiverobot, 2026-10 (secundária)](https://www.progressiverobot.com/2026/10/02/maket-2-0-ai-home-design-floor-plans/). Não confirmei em fonte oficial.
- Algoritmo: não documentado publicamente (lacuna).

**TestFit (EUA). Status: ativo (2026). Foco multifamiliar e estacionamento, não residência unifamiliar.**
- FATO: a empresa se descreve como "motor de configuração em tempo real" para site planning. O recurso "Generative Design" está em beta: o usuário define metas e recebe várias soluções de implantação. — [TestFit, Generative Design](https://www.testfit.io/generative-design)
- FATO: o TestFit 5.2 deixa definir metas de unit mix (tipos por edifício, quartos, área-alvo, percentual por tipo). — [TestFit blog 5.2](https://www.testfit.io/blog/testfit-5-2-better-data-brings-better-generative-design)
- FATO (secundária, alegação não verificada): gera cerca de 3.000 variações em cerca de 3 s e as ranqueia por KPIs do usuário. Ajustar sliders reorganiza todos os pavimentos instantaneamente. — [archgyan (secundária)](https://archgyan.com/testfit-ai-feasibility-studies-architects/)
- FATO: o CEO Clifton Harness deu entrevista expressando "reservas" sobre a própria ferramenta generativa. Não li o conteúdo. — [Architect Magazine](https://www.architectmagazine.com/?p=345648)

**Autodesk Forma (ex-Spacemaker). Status: ativo. Spacemaker adquirida em novembro de 2020.**
- FATO: a Autodesk comprou a Spacemaker (Oslo) por US$ 240 milhões líquidos de caixa e anunciou a conclusão em 24/11/2020. O foco era o planejamento urbano em estágio inicial com IA e design generativo. — [TechCrunch 2020](https://techcrunch.com/2020/11/17/spacemaker-ai-software-for-urban-development-is-acquired-by-autodesk-for-240m/amp/); [Nasdaq press release](https://www.nasdaq.com/press-release/autodesk-completes-acquisition-of-spacemaker-provider-of-ai-and-generative-design)
- FATO (secundária): blogs de 2026 descrevem o Forma como sucessor da Spacemaker, com foco em análise de terreno e ambiental. Os preços citados divergem (cerca de US$ 185 a 400/mês). — [creativetoolsai (secundária)](https://www.creativetoolsai.com/ai-tools/autodesk-forma-site-planning/); [aibuildingtools (secundária)](https://aibuildingtools.com/best-ai-for/architectural-design)
- Observação: a escala do Forma é a implantação urbana, não a planta interna de uma residência.

**Higharc (EUA, homebuilders). Status: ativo. Série C em julho de 2026.**
- FATO: o modelo de IA se chama "Generative Building Model" (GBM) e representa edifícios como tokens ("tokenizing buildings"). — [Higharc blog](https://www.higharc.com/blog/ai-layout-at-higharc-tokenizing-buildings); [Higharc blog, "representing buildings like language"](https://higharc.com/blog/ai-home-design-representing-buildings-like-language?amp=&amp=)
- FATO: segundo reportagem, o GBM hoje **mobilia cômodos** dentro de um modelo BIM existente. A geração de casa BIM completa a partir de linguagem natural está "em desenvolvimento". — [HousingWire](https://www.housingwire.com/articles/higharc-floor-plans-into-intelligent-data/)
- FATO: o valor da Série C diverge entre as fontes: US$ 90M segundo a [SiliconANGLE, 2026-07-01](https://siliconangle.com/2026/07/01/homebuilding-ai-startup-higharc-bags-90m-series-c-funding/) e US$ 95M segundo a [TechTimes, 2026-07-01](https://www.techtimes.com/articles/319480/20260701/homebuilding-ai-raises-95m-floor-plan-vision-tech-moves-lumber-supply-chain.htm).
- FATO: converte croqui ou planta 2D em modelo "vivo" no seu modelo de dados próprio (tipo BIM). — [Bricks & Bytes](https://bricks-bytes.com/ai/higharc-sketch-to-buildable-home-ai-pipeline/)

**Hypar, Snaptrude, Arcol. Status: ativos (2026), só com fontes secundárias.**
- FATO (secundária): Hypar é uma plataforma paramétrica/computacional para equipes que programam, com tier gratuito. Snaptrude é um BIM conceitual no navegador, "mais leve em IA generativa". Arcol é um BIM colaborativo web-native, "promissor, mas em estágio inicial". — [aibuildingtools (secundária)](https://aibuildingtools.com/blog/best-generative-design-tools); [meltflexai (secundária)](https://www.meltflexai.com/blog/ai-tools-for-architecture-studios-2026)

**Outros**
- FATO: o Planner 5D tem uma página em português de "gerador de planta baixa com IA" e converte planta existente em projeto editável. — [Planner 5D PT](https://planner5d.com/pt/use/gerador-ia-planta-baixa)
- FATO: a Arqgen, startup de São Paulo, faz uma plataforma de apoio a decisões para incorporadoras, com análise de viabilidade. Não é um gerador de planta residencial. — [Agência FAPESP](https://agencia.fapesp.br/artificial-intelligence-improves-decision-making-in-architectural-design/53838)
- FATO (marketing, não verificado): o DesignDrafter (Índia) diz que permite **travar zonas** e editar paredes e cômodos depois da geração, e que mudar uma entrada regenera o layout em segundos. — [DesignDrafter](https://designdrafter.com/generate-floor-plan/)
- FATO: a Ideal House tem páginas em português de "Gerador de Plantas de Casas", com sinais de tradução do inglês. A origem da empresa não foi confirmada. — [ideal.house/pt](https://ideal.house/pt/create/housePlan)

### Inferences
- HIPÓTESE: o padrão dominante no mercado é "metas + pesos → N opções pontuadas → filtrar/ranquear → editar/exportar". O pipeline do PyGridPlan (K=4 alternativas com score decomposto) está alinhado com esse padrão. O diferencial possível é **explicar** o score (decomposição por critério) em vez de só ranquear.
- HIPÓTESE: o TestFit e o Finch dependem de feedback em tempo real ou quase. Isso indica que a latência é parte central da experiência. Para o PyGridPlan, com CP-SAT, é melhor mostrar soluções parciais (callback de solução) do que bloquear a UI.
- OPINIÃO: as afirmações "gera milhares de variações em segundos" vêm de reviews secundários e não servem como parâmetro de comparação.

### Gaps
- Não encontrei fontes sobre **Laiout, Rayon, Digital Blue Foam, ArchiStar, Architechtures, qbiq e Floorplanner** nas buscas feitas. O status em 2026 deles fica **não verificado** (não afirmo que existam ou não).
- A renomeação Spacemaker → Forma não foi confirmada em fonte primária nesta pesquisa. Os blogs a tratam como fato.
- Nenhum produto publica o algoritmo ou estudo com usuários. Não encontrei documentação de "travar cômodo e regenerar o resto" em produto além da alegação de marketing do DesignDrafter.
- Não encontrei gerador brasileiro de planta residencial com IA. A busca em português trouxe só a Arqgen (viabilidade) e tradutores de produtos estrangeiros.

## 2. Trabalhos acadêmicos interativos e baseados em restrições

### Takeaway
A literatura se divide em (a) otimização/restrição determinística (Merrell 2010, Bao 2013, Wu 2018 MIQP, GPLAN), mais próxima do PyGridPlan, e (b) modelos generativos aprendidos a partir do RPLAN (House-GAN/++, HouseDiffusion, Graph2Plan, iPLAN, MaskPLAN, Tell2Design, ChatHouseDiffusion e variantes com LLM em 2024–2026). A interação real se resume a quatro formas: edição do grafo de bolhas, entrada parcial que o modelo completa, edição local preservando o resto e exploração de um espaço de soluções boas. **Não encontrei nenhum artigo que combine LLM + CP-SAT/MILP para planta residencial interativa.**

### Cited Findings

**Otimização / restrições (determinísticos)**
- FATO: Merrell, Schkufza & Koltun, "Computer-generated residential building layouts", *ACM TOG* 29(6), art. 181, 2010 (SIGGRAPH Asia). Uma rede bayesiana treinada em dados reais gera o programa arquitetônico (cômodos, adjacências, áreas desejadas). Depois as plantas são otimizadas e viram modelo 3D. O alvo são aplicações gráficas interativas. — [PDF Princeton](https://www.cs.princeton.edu/courses/archive/spring11/cos598A/pdfs/Merrell10a.pdf); [SIGGRAPH history](https://history.siggraph.org/?p=197308)
- FATO: Bao, Yan, Mitra & Wonka, "Generating and exploring good building layouts", *ACM TOG* 32(4), art. 122, 2013. A partir de amostras discretas de layouts bons, o trabalho caracteriza analiticamente o espaço de formas local em volta delas. Um **"portal graph"** permite navegar numa família de soluções, expondo o usuário **apenas a layouts bons**. — [SIGGRAPH history](https://history.siggraph.org/?p=108396); [PDF SIGGRAPH 2013](https://discmaster.textfiles.com/file/16678/SIGGRAPH%202013%20-%20Disc%203.iso/content/papers/122-0372.pdf)
- FATO: Wu, Fan, Liu & Wonka, "MIQP-based Layout Design for Building Interiors", *Computer Graphics Forum* 37(2):511–521, 2018 (Eurographics), DOI 10.1111/cgf.13380. Framework hierárquico em programação inteira mista quadrática. Os cômodos são polígonos decompostos em retângulos. As restrições cobrem área, posição, adjacência e contorno. Os autores dizem ser "várias ordens de magnitude mais rápido" que métodos anteriores e escalável a escritórios e shoppings. — [EG Digital Library](https://diglib.eg.org/items/4bcbcb26-b92e-4646-a486-e4f74f7208f8/full); [PDF Wonka](https://peterwonka.net/Publications/pdfs/2018.EG.Wenming.MIQPFloorplan.pdf)
- FATO: GPLAN (Shekhawat et al., BITS Pilani) gera plantas cotadas com técnicas de teoria de grafos e otimização. A entrada é um grafo de adjacência desenhado numa GUI ou um layout sem dimensões. A saída é um **conjunto de plantas topologicamente distintas** com contorno retangular, preservando adjacências, posições e formas. — [arXiv 2008.01803](https://arxiv.org/pdf/2008.01803); [arXiv 1910.00081](https://arxiv.org/pdf/1910.00081)
- FATO: o grupo publicou em 2024–2025, na *AI EDAM* (Cambridge), trabalhos sobre geração automática de **circulações** dentro da planta e plantas com "mínimo de dobras". — [AI EDAM, circulações](https://www.cambridge.org/core/product/17830B95C3A0B8120CE87C6F8610AA66); [AI EDAM, minimum bends](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/214D14B8D2D263DE4B2D5C97103165F0/S0890060424000179a.pdf/automated-generation-of-floor-plans-with-minimum-bends.pdf)
- FATO: Rodrigues, Gaspar & Gomes (2013), "An evolutionary strategy enhanced with a local search technique for the space allocation problem in architecture, part 2: Validation and performance tests" (estratégia evolutiva híbrida com busca local). Encontrei só a citação, não o texto. — citado em [arXiv 2008.01803](https://arxiv.org/pdf/2008.01803)

**Modelos generativos aprendidos (quase todos sobre o RPLAN)**
- FATO: Graph2Plan (Hu, Huang, Tang, van Kaick, Zhang, Huang), SIGGRAPH 2020 / *ACM TOG*, arXiv 2004.13204. O usuário dá o contorno e o número de cômodos. O sistema **recupera** do RPLAN (cerca de 80K plantas) plantas com seus grafos de layout. O usuário **edita o grafo** (adiciona ou remove nós e arestas, move nós) e uma GNN+CNN gera a planta. Os autores se dizem o primeiro framework de deep learning com usuário no loop. O artigo inclui um estudo com usuários sobre plausibilidade. — [arXiv](https://arxiv.org/abs/2004.13204v1); [GitHub](https://github.com/HanHan55/Graph2plan); [SIGGRAPH history](https://history.siggraph.org/?p=104284)
- FATO: uma crítica de 2024 (TU Delft) diz que o Graph2Plan não gera o grafo, só o recupera de plantas parecidas. — [TU Delft, EC3 2024](https://pure.tudelft.nl/ws/portalfiles/portal/221606617/EC32024_188.pdf)
- FATO: House-GAN (ECCV 2020), House-GAN++ (**ICCV 2021**, não CVPR) e HouseDiffusion (CVPR 2023) usam o **diagrama de bolhas** como entrada. O House-GAN++ acrescenta treino com condicionamento em ground truth e otimização em tempo de teste. O HouseDiffusion gera polígonos vetoriais e quebra a suposição Manhattan. — [Review Liu et al. 2025, arXiv 2504.09694, Tabela 1](https://arxiv.org/html/2504.09694v1)
- FATO: um artigo do EMNLP 2025 diz que esses modelos usam bem o grafo, mas "não conseguem especificar tamanho e forma dos cômodos". Ele reporta FID de 32,45 (Graph2Plan), 34,06 (House-GAN++) e 28,72 (HouseDiffusion). — [Cross-modal Agent Framework, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.473.pdf)
- FATO: iPLAN (He, Huang & Wang, Univ. Leeds), CVPR 2022, arXiv 2203.14412. É um modelo human-in-the-loop **procedural**: gera automaticamente, mas o projetista pode interagir **em cada etapa**. Os dados de processo foram obtidos por engenharia reversa das plantas finais, seguindo princípios usados por projetistas. Foi avaliado em RPLAN e LIFULL. Não lida com contornos muito irregulares. — [CVF open access](https://openaccess.thecvf.com/content/CVPR2022/html/He_iPLAN_Interactive_and_Procedural_Layout_Planning_CVPR_2022_paper.html); [arXiv](https://arxiv.org/abs/2203.14412v2)
- FATO: MaskPLAN (Zhang, Savov & Dillenburger, ETH Zürich), CVPR 2024, pp. 8964–8973. Usa a **entrada parcial** do usuário como prior condicional global, transformando ideias incompletas em layout completo, com autoencoders mascarados em grafo (GDMAE, cinco transformers). O README do repositório dizia que o código viria "em algumas semanas". — [CVF](https://openaccess.thecvf.com/content/CVPR2024/html/Zhang_MaskPLAN_Masked_Generative_Layout_Planning_from_Partial_Input_CVPR_2024_paper.html); [GitHub](https://github.com/HangZhangZ/MaskPLAN)
- FATO: Tell2Design (Leng et al.), ACL 2023 (Area Chair Award). São mais de 80K plantas do RPLAN pareadas com instruções em linguagem natural, com uso restrito a pesquisa. — [ACL Anthology](https://aclanthology.org/2023.acl-long.820/); [arXiv](https://arxiv.org/html/2311.15941v1)
- FATO: ChatHouseDiffusion (Qin et al., Tsinghua), arXiv 2410.11908 (2024, sem venue revisado). Um LLM converte o texto em **JSON de condições**. Um modelo de difusão gera a planta. A edição usa **semente fixa e reaproveita mapas de cross-attention** nos primeiros passos para editar localmente "sem alterar a planta geral". Não tem trava explícita de cômodos. Os autores admitem que "ajustes precisos, como o tamanho exato dos cômodos, não podem ser alcançados". A UI em tkinter tem undo e "regenerar trocando a semente". Drag-and-drop ficou como trabalho futuro. Não houve estudo com usuários nem medição de latência. O código ainda não foi aberto. — [arXiv HTML](https://arxiv.org/html/2410.11908v1)
- FATO: HouseLLM/HouseTune (arXiv 2411.12279, versão no AAAI). Um LLM gera um layout inicial a partir do texto e uma difusão condicional o refina. — [arXiv](https://arxiv.org/html/2411.12279v2); [AAAI](https://ojs.aaai.org/index.php/AAAI/article/download/38417/42379)
- FATO: DStruct2Design (arXiv 2407.15723) propõe dados e benchmarks para gerar plantas a partir de **estruturas de dados** (representação estruturada, não imagem). — [arXiv](https://arxiv.org/pdf/2407.15723)
- FATO: GRE-Diff (arXiv 2607.08086, 2026) descreve o fluxo "gerar vários candidatos → escolher um → refinar" com as operações **Add, Remove, Move, Anchor** e "Repurpose". — [arXiv](https://arxiv.org/pdf/2607.08086). Não li o detalhe da operação Anchor.
- FATO: há trabalhos de 2026 com LLM ajustado por RL com **recompensas verificáveis** para aderência a restrições topológicas e numéricas, sem solver no loop ([arXiv 2605.14117](https://arxiv.org/html/2605.14117v1)), e o "HypergraphFormer" para geração editável ([arXiv 2605.18932](https://arxiv.org/pdf/2605.18932)). Só confirmei os títulos e resumos.
- FATO: o padrão LLM → restrições → solver existe fora de plantas. O Holodeck (arXiv 2312.09067) usa um LLM para produzir restrições espaciais entre objetos 3D e resolve com DFS ou MILP (Gurobi). — [arXiv](https://arxiv.org/pdf/2312.09067)
- FATO: o review de Liu et al. (2025) diz que as entradas suportadas pelos métodos atuais "são limitadas" e cita artefatos e arranjos incorretos como desafio aberto. — [arXiv 2504.09694](https://arxiv.org/html/2504.09694v1)

### Inferences
- HIPÓTESE: a referência acadêmica mais próxima do motor do PyGridPlan é **Wu et al. 2018 (MIQP)**: restrições de área, adjacência e contorno, com cômodos decompostos em retângulos. Vale ler o artigo para comparar a formulação com a malha de linhas de parede em CP-SAT, principalmente a hierarquia (zonas → cômodos) e o tratamento de adjacência.
- HIPÓTESE: o **portal graph de Bao 2013** é o modelo conceitual certo para a galeria de alternativas: navegar só entre soluções boas e vizinhas, em vez de amostrar ao acaso. O equivalente barato no PyGridPlan seria "gerar uma variante próxima desta" (resolver de novo com a solução escolhida como hint e uma restrição de distância mínima/máxima).
- HIPÓTESE: os modelos aprendidos (GAN/difusão) não controlam bem área exata nem restrições duras. Isso é admitido em ChatHouseDiffusion e EMNLP 2025. O PyGridPlan **não deve** trocar o solver por um modelo aprendido. A arquitetura atual (LLM preenche JSON → motor determinístico) é a mesma que ChatHouseDiffusion e HouseLLM usam na primeira metade e, na segunda, troca a difusão por um solver com garantia de restrição.
- HIPÓTESE: iPLAN e GPLAN sugerem que a geração **em etapas** (contorno → zonas → cômodos → aberturas) é natural para o usuário intervir. O PyGridPlan já segue isso nas fases depois da escolha (portas/janelas → mobiliário).

### Gaps
- Não verifiquei o método de otimização interno de Merrell 2010 nem a formulação exata do Wu 2018 (não li os PDFs inteiros).
- Não verifiquei os autores de House-GAN, House-GAN++ e HouseDiffusion em fonte primária. Lembro de Nauata, Furukawa et al. e Shabani et al., mas isso não foi confirmado aqui.
- Não encontrei um artigo "Intelligent home 3D" específico nem nenhum trabalho com CP-SAT/OR-Tools aplicado a planta residencial interativa.
- Não confirmei o acrônimo "EPSAP" para o trabalho de Rodrigues, Gaspar e Gomes.

## 3. Lições de interação: travar e regenerar, alternativas, edição de restrições, latência, explicação e undo

### Takeaway
A evidência publicada sobre interação é **fraca**: quase nenhum artigo traz estudo com usuários detalhado sobre travar e regenerar. Os padrões que aparecem são editar o grafo de bolhas (Graph2Plan), completar a partir de entrada parcial (MaskPLAN), editar localmente preservando o resto (ChatHouseDiffusion), interagir por etapas (iPLAN), Add/Remove/Move/Anchor (GRE-Diff), navegar só entre soluções boas (Bao 2013) e, nos produtos, metas e pesos com opções pontuadas e filtráveis (Finch, TestFit).

### Cited Findings
- FATO: no Graph2Plan, a edição de restrições é feita **no grafo**. O usuário adiciona ou remove nós e arestas ou arrasta nós, e a planta é regenerada a partir das caixas dos cômodos. — [GitHub Graph2Plan](https://github.com/HanHan55/Graph2plan); [arXiv](https://arxiv.org/pdf/2004.13204)
- FATO: o MaskPLAN trata a intervenção do usuário como **entrada parcial** (atributos conhecidos de alguns cômodos) e completa o resto. — [CVF](https://openaccess.thecvf.com/content/CVPR2024/html/Zhang_MaskPLAN_Masked_Generative_Layout_Planning_from_Partial_Input_CVPR_2024_paper.html)
- FATO: o ChatHouseDiffusion preserva o que não foi editado **de forma implícita** (semente e attention fixas), sem trava explícita. Ele oferece undo, "lembrar última entrada" e "regenerar = nova semente", e não garante tamanhos exatos. — [arXiv](https://arxiv.org/html/2410.11908v1)
- FATO: o iPLAN permite interação **ao longo de todo o procedimento** por etapas, não só no fim. — [CVF](https://openaccess.thecvf.com/content/CVPR2022/html/He_iPLAN_Interactive_and_Procedural_Layout_Planning_CVPR_2022_paper.html)
- FATO: o GRE-Diff tem o fluxo "candidatos → escolher → refinar" com **Anchor** (fixar) entre as operações. — [arXiv 2607.08086](https://arxiv.org/pdf/2607.08086)
- FATO: o Bao 2013 expõe ao usuário **apenas layouts bons**, navegando por um grafo de famílias de soluções. — [SIGGRAPH history](https://history.siggraph.org/?p=108396)
- FATO: o GPLAN entrega um **conjunto de plantas topologicamente distintas** para o mesmo grafo, com diversidade por topologia e não por pequenas variações. — [arXiv 2008.01803](https://arxiv.org/pdf/2008.01803)
- FATO: no Finch, o usuário controla **pesos** (squareness, daylight, área) e recebe opções pontuadas por critérios nomeados. — [AEC Magazine](https://aecmag.com/ai/finch3d-starts-to-sing/)
- FATO (secundária): no TestFit, sliders e metas mudam a configuração "instantaneamente" e os esquemas são comparados por métricas como NRSF, eficiência e yield on cost. — [archgyan (secundária)](https://archgyan.com/testfit-ai-feasibility-studies-architects/); [TestFit](https://www.testfit.io/generative-design)
- FATO: segundo o review de 2025, a avaliação de **realismo** costuma ser feita com estudos em que arquitetos ou leigos dão notas ou ranqueiam as saídas. Não são estudos de usabilidade da interação. — [arXiv 2504.09694](https://arxiv.org/html/2504.09694v1)
- FATO: o Graph2Plan relata um estudo com usuários sobre **plausibilidade** das plantas. Não encontrei o número de participantes nem o protocolo. — [academia.edu cópia do artigo](https://www.academia.edu/90868205/Graph2Plan)

### Inferences (todas HIPÓTESE, aplicadas ao PyGridPlan)
- **Travar cômodo = restrição dura no CP-SAT** (fixar as variáveis do retângulo do cômodo na malha). É mais forte que a preservação implícita do ChatHouseDiffusion e é uma vantagem real do solver. Regenerar o resto vira resolver de novo com essas variáveis fixas e, para estabilidade, usar a solução anterior como hint. (O hint e a fixação de variáveis existem na API do OR-Tools; não reverifiquei a documentação nesta pesquisa.)
- **Arrastar parede** = restrição de igualdade numa linha da malha, seguida de nova resolução. Se ficar inviável, mostrar **qual restrição conflita**, como o "interactive repair loop" de [arXiv 2404.11891](https://arxiv.org/pdf/2404.11891), feito para planejamento de viagens. CP-SAT tem suporte a suposições (assumptions) para extrair um núcleo de inviabilidade; não reverifiquei isso aqui.
- **Alternativas:** apresentar as K=4 com diversidade **topológica** (estilo GPLAN: grafos de adjacência realizados diferentes), não só geométrica. Oferecer "variar perto desta" (estilo Bao) como ação secundária. A comparação A vs B com o score decomposto por critério é algo que os artigos não mostram e os produtos mostram só como ranking. É o diferencial a explorar.
- **Editar restrições no diagrama de bolhas** (Graph2Plan, House-GAN): o grafo de relações do PyGridPlan pode ser editável (arrastar para criar "perto/longe", roda do mouse para intensidade 1–5). A ressalva da TU Delft vale como alerta: grafo recuperado ou gerado não é grafo do usuário. O PyGridPlan deve deixar claro o que é pedido do usuário e o que é sugestão do motor (cores diferentes, como já está planejado para portas).
- **Latência:** produtos de referência prometem resposta "instantânea". Com CP-SAT, mostrar a primeira solução viável cedo e as melhorias depois (via callback), com limite de tempo visível no console de eventos.
- **Undo:** só o ChatHouseDiffusion cita undo explicitamente. A árvore de estados do PyGridPlan (com ramificação) vai além do que a literatura descreve. Não encontrei referência que valide ou refute árvore contra pilha linear.

### Gaps
- Não encontrei estudos com usuários publicados que comparem travar e regenerar contra editar à mão, nem estudos sobre galeria de alternativas (quantas mostrar, como agrupar) **em plantas**. A literatura de "design galleries" e exploração de espaço de design em computação gráfica (ex.: [Interactive Diversity Optimization of Environments, arXiv 1801.08607](https://ar5iv.labs.arxiv.org/html/1801.08607)) apareceu na busca, mas não foi lida.
- Não há dados de latência aceitável em ferramentas de planta. As alegações de produto são marketing.

## 4. Datasets e métricas de avaliação (só como ponteiro)

### Takeaway
O RPLAN domina a literatura, mas o uso é restrito a pesquisa. Os candidatos com licença aberta são **Swiss Dwellings (CC BY 4.0)** e **MSD** (CC BY 4.0 no 4TU, CC BY-SA 4.0 no Kaggle, uma divergência). O CubiCasa5K é não comercial. As métricas da área (FID, GED, IoU) servem a modelos de imagem. Para um solver, a métrica mais útil é a **compatibilidade com o grafo pedido** (estilo GED) mais os critérios do próprio score.

### Cited Findings
- FATO: o RPLAN tem mais de 80K residências reais com anotação densa. O LIFULL HOME tem milhões de plantas reais. O CubiCasa5K tem 5.000 plantas com camada de mobiliário vetorizada. — [Review Liu et al. 2025](https://arxiv.org/html/2504.09694v1)
- FATO: o Tell2Design, derivado do RPLAN, restringe o uso a "apenas fins de pesquisa". Não encontrei licença formal do próprio RPLAN. — [arXiv Tell2Design](https://arxiv.org/html/2311.15941v1)
- FATO: o Swiss Dwellings (Archilyse) é CC BY 4.0 segundo o produtor e o Zenodo. O pipeline de código da Archilyse é AGPL. — [Archilyse/Standfest](https://archilyse.standfest.science/swiss-dwellings); [OpenAIRE/Zenodo](https://explore.openaire.eu/search/dataset?pid=10.5281/zenodo.7070951)
- FATO: o MSD (Modified Swiss Dwellings, para autocompletar plantas) aparece como CC BY 4.0 no [4TU.ResearchData](https://data.4tu.nl/datasets/e1d89cb5-6872-48fc-be63-aadd687ee6f9), o que é **contradito** pelo [Kaggle](https://www.kaggle.com/datasets/caspervanengelenburg/modified-swiss-dwellings), que mostra CC BY-SA 4.0.
- FATO: a licença do CubiCasa5K diverge entre espelhos: CC BY-NC-SA 3.0 IGO no [Kaggle](https://www.kaggle.com/datasets/qmarva/cubicasa5k) e CC BY-NC 4.0 (Zenodo) segundo [repositório de terceiros](https://github.com/xmarva/floorplan-detection). Em todas as versões é **não comercial**. Artigo original: [arXiv 1904.01920](https://arxiv.org/pdf/1904.01920).
- FATO: métricas usuais: **FID** (qualidade de imagem), **diversidade** (PRD, Intra-FID), **GED** (se a planta respeita as conexões do grafo de entrada), **Boundary IoU** e estudos de realismo com arquitetos ou leigos. — [Review Liu et al. 2025](https://arxiv.org/html/2504.09694v1)
- FATO: o ChatHouseDiffusion usa Micro-IoU contra o ground truth do RPLAN (60,57 contra 54,34 do T2D). — [arXiv](https://arxiv.org/html/2410.11908v1)

### Inferences
- HIPÓTESE: para o PyGridPlan (portfólio aberto), o Swiss Dwellings ou o MSD seriam a única fonte de **casos de referência reais** com licença compatível, para calibrar distribuições de área e proporção ou montar fixtures. São apartamentos suíços, não casas brasileiras, e isso limita o uso para calibração local.
- HIPÓTESE: FID não faz sentido para saída vetorial determinística. As métricas adequadas são: (1) taxa de satisfação de adjacências pedidas (versão ponderada do GED), (2) erro de área por cômodo, (3) diversidade entre as K alternativas, medida por distância de grafo ou de geometria, e (4) tempo até a primeira solução viável.

### Gaps
- As condições de acesso ao RPLAN e ao LIFULL (formulário, NII-IDR) não foram verificadas em fonte primária.

## 5. O que reusar e o que evitar no PyGridPlan

### Takeaway
Reusar padrões de interação e de avaliação, não modelos. O solver do PyGridPlan já oferece o que os modelos generativos não garantem (área exata, restrições duras, trava real). Falta implementar bem trava e regeneração, edição do grafo, diversidade topológica e explicação do score.

### Cited Findings
- FATO: modelos de grafo para planta (Graph2Plan, House-GAN++, HouseDiffusion) "não conseguem especificar tamanho e forma dos cômodos". — [EMNLP 2025](https://aclanthology.org/2025.emnlp-main.473.pdf)
- FATO: o ChatHouseDiffusion admite não alcançar tamanho exato e preserva regiões só de forma implícita. — [arXiv](https://arxiv.org/html/2410.11908v1)
- FATO: a abordagem MIQP (Wu 2018) trata área, posição, adjacência e contorno como restrições e escala bem. — [EG DL](https://diglib.eg.org/items/4bcbcb26-b92e-4646-a486-e4f74f7208f8/full)
- FATO: o Finch combina grafo de regras com otimização ponderada e opções pontuadas. — [AEC Magazine](https://aecmag.com/ai/finch3d-starts-to-sing/)
- FATO: o padrão "LLM gera restrições → solver resolve" está publicado no Holodeck (3D) e o "repair loop" para inviabilidade em planejamento. — [Holodeck](https://arxiv.org/pdf/2312.09067); [arXiv 2404.11891](https://arxiv.org/pdf/2404.11891)

### Inferences (todas HIPÓTESE)
**Reusar**
1. **Trava como restrição dura + hint da solução anterior** para regenerar o resto (estabilidade visual entre iterações). Mostrar os cômodos travados com um ícone de cadeado e borda distinta.
2. **Diagrama de bolhas editável como editor de restrições** (Graph2Plan), com distinção visual entre relação pedida pelo usuário e relação inferida pelo LLM ou pelo motor.
3. **Pesos de critérios expostos em sliders** (Finch e TestFit), reprocessando só o ranking quando possível. Reordenar as K alternativas por novos pesos não exige resolver de novo se o score é decomposto. Resolver de novo só quando o peso entra na função objetivo.
4. **Diversidade topológica nas K alternativas** (GPLAN), com uma ação "variar perto desta" (Bao 2013).
5. **Explicação de inviabilidade:** ao arrastar uma parede ou travar algo impossível, reportar a restrição em conflito (núcleo de inviabilidade ou relaxação), no espírito do repair loop.
6. **Interação por etapas** (iPLAN): já está no plano (planta → aberturas → mobiliário). Vale permitir voltar a uma etapa anterior na árvore de estados sem perder as seguintes quando forem compatíveis.
7. **Métricas de avaliação próprias** (adjacência satisfeita, erro de área, diversidade, tempo até a 1ª solução) em vez de FID.
8. **Wu et al. 2018** como leitura obrigatória para comparar a formulação. O **Swiss Dwellings** (CC BY 4.0) como possível fonte de casos reais, com a ressalva de tipologia.

**Evitar**
1. Trocar ou complementar o solver com GAN/difusão: exige o RPLAN (só para pesquisa), GPU e treino, e não garante restrições. Viola os princípios "offline" e "geometria determinística".
2. Preservação implícita (semente fixa) como substituto de trava real.
3. Mostrar dezenas de alternativas sem estrutura. Os produtos que geram milhares (TestFit) dependem de ranking e filtro. Com K=4, o valor está na explicação, não no volume.
4. Esconder o score atrás de um número único. Os produtos mostram critérios nomeados, e o PyGridPlan já tem score decomposto.
5. Usar o CubiCasa5K ou o RPLAN como fixtures versionadas no repositório, por conflito de licença (não comercial ou só pesquisa).

### Gaps
- Não há evidência empírica (estudo com usuários) que valide as escolhas acima para plantas. Elas são inferências a partir de padrões de produto e artigos, e precisam de teste com o próprio responsável na conferência visual do M2.
- Não verifiquei a latência típica do CP-SAT para re-solve com trava em problemas do porte do PyGridPlan. Isso deve ser medido no próprio projeto.
