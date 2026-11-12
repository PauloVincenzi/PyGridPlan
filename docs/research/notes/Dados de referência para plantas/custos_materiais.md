# Custos de materiais de construção no Brasil (casa unifamiliar convencional) e estrutura de um dataset por classe de acabamento

> Notas de pesquisa. Pesquisa feita em 2026-11-11. Toda informação abaixo tem fonte e data. Preços de varejo vêm de buscas ou agregadores e quase nenhum mostra data de coleta: tratar como **indicativos** e nunca como referência oficial. Valores SINAPI "média nacional" vêm do espelho Orçamentor (orcamentor.com), que replica a base oficial da Caixa: conferir na planilha oficial antes de usar em produção.

## 1. Referências oficiais e públicas: SINAPI, CUB/m² e TCPO (o que são, como acessar, licença)

### Takeaway
O SINAPI (Caixa + IBGE) é a única referência pública e gratuita que publica, todo mês e por UF, **preços de insumos** e **composições de serviços com coeficientes de consumo** (material por m², mais horas de mão de obra), em XLSX e PDF. Ele serve como núcleo do dataset. O CUB/m² (Sinduscon, NBR 12721) é só um custo global por m² de projeto-padrão. Serve para calibrar ou validar o total, não para orçar a partir de quantidades.

### Cited Findings
**SINAPI: publicação e formatos**
- Os relatórios mensais saem em PDF (Analítico de Composições, Custos de Composições, Preços de Insumos) e em XLSX (Famílias e Coeficientes, Manutenções, **Percentual de Mão de Obra em Composições**, Insumos e Composições de **todas as UF**). — [Caixa SINAPI (via busca)](https://www.caixa.gov.br/sinapi)
- A página da Caixa separa "Relatórios a partir de 2025" (arquivo nacional único) de "relatórios até 2024" (download por estado). O padrão de URL citado num documento de mar/2026 é `caixa.gov.br/Downloads/sinapi-relatorios-mensais/SINAPI-AAAA-MM-formato-xlsx.zip` (ou `-formato-pdf.zip`). O arquivo de jan/2026 saiu em 10/02/2026. — [Caixa SINAPI](https://www.caixa.gov.br/poder-publico/modernizacao-gestao/sinapi/Paginas/default.aspx) (a página bloqueou o fetch direto por excesso de redirects; informação obtida pelo resumo da busca)
- Toda referência mensal sai em duas versões, **desonerada** e **não desonerada**. A diferença está nos encargos patronais sobre a folha de pagamento, então afeta só a mão de obra. — [Caixa SINAPI](https://www.caixa.gov.br/sinapi); [VRI Consulting](https://www.vriconsulting.com.br/indices/cub-sp-r8n-sem-desoneracao.php)
- Preço em branco para uma UF significa que não houve coleta mínima de preços naquele mês. — [Caixa SINAPI](https://www.caixa.gov.br/sinapi)
- Há relatórios mensais desde 2009. A Caixa também publica o "Livro de Metodologias e Conceitos" e os Cadernos Técnicos das composições. — [Caixa SINAPI](https://www.caixa.gov.br/sinapi); [Livro SINAPI Metodologias e Conceitos](https://www.caixa.gov.br/Downloads/sinapi-metodologia/Livro_SINAPI_Metodologias_Conceitos.pdf)
- Divisão de papéis: a Caixa cuida da engenharia (composições) e o IBGE faz a coleta de preços e calcula o índice. — [Conjur, 06/04/2026](https://www.conjur.com.br/2026-abr-06/ditadura-do-sinapi-e-a-sobrevivencia-do-preco-de-mercado/)

**SINAPI: crise de 2025/2026 (risco para a série de dados)**
- No fim de 2025 o IBGE deixou de entregar preços de insumos, e as tabelas de out/nov/2025 saíram com **preços zerados**. Em 22/12/2025 o IBGE enviou os dados e a Caixa retificou os relatórios. — [Marcelo Corghi (Substack)](https://marcelocorghi.substack.com/p/atualizacao-da-situacao-do-sinapi); [Conjur, 06/04/2026](https://www.conjur.com.br/2026-abr-06/ditadura-do-sinapi-e-a-sobrevivencia-do-preco-de-mercado/)
- O Decreto nº 12.867/2026 (março/2026) alterou o Decreto 7.983/2013. Ele permite que a Caixa custeie a pesquisa de preços do IBGE e que "órgãos de pesquisa congêneres" façam a coleta. — [Conjur](https://www.conjur.com.br/2026-abr-06/ditadura-do-sinapi-e-a-sobrevivencia-do-preco-de-mercado/); [Adiel Ferreira Jr.](https://www.adielferreirajr.com/post/sinapifinanciamento)
- As publicações seguem em 2026. O boletim IBGE do SINAPI de setembro/2026 saiu em 09/10/2026, e a referência 09/2026 já aparece em espelhos da base de composições. — [IBGE, Indicadores SINAPI set/2026 (PDF)](https://ftp.ibge.gov.br/Precos_Custos_e_Indices_da_Construcao_Civil/Fasciculo_Indicadores_IBGE/sinapi_202609caderno.pdf); [Orçamentor 87529](https://orcamentor.com/composicao/87529/)
- CBIC e Caixa discutiram (out/2026) a atualização do SINAPI após a redução da jornada de trabalho e a Reforma Tributária. A primeira pesquisa feita inteiramente após a transição da jornada será a de jan/2027. — [CBIC, 26/10/2026](https://cbic.org.br/infraestrutura/2026/10/26/cbic-e-caixa-discutem-atualizacao-do-sinapi-apos-reducao-da-jornada-de-trabalho-e-reforma-tributaria/)
- Os acórdãos TCU 2459/2025 e 1354/2025 tratam a adequação do SINAPI como presunção **relativa**, ou seja, ele pode divergir do mercado. — [Conjur](https://www.conjur.com.br/2026-abr-06/ditadura-do-sinapi-e-a-sobrevivencia-do-preco-de-mercado/)

**SINAPI/IBGE: custo médio por m² com parcela de materiais (dado oficial direto)**
- Setembro/2026: o custo nacional da construção por m² foi **R$ 1.999,73**, dos quais **R$ 1.127,17 em materiais** e **R$ 872,56 em mão de obra**. Em 12 meses, materiais subiram 5,54% e mão de obra 8,53%. — [IBGE, Indicadores SINAPI set/2026, publicado em 09/10/2026](https://ftp.ibge.gov.br/Precos_Custos_e_Indices_da_Construcao_Civil/Fasciculo_Indicadores_IBGE/sinapi_202609caderno.pdf)
- O mesmo boletim traz custos médios por UF e região, calculados considerando a desoneração da folha. — [IBGE set/2026](https://ftp.ibge.gov.br/Precos_Custos_e_Indices_da_Construcao_Civil/Fasciculo_Indicadores_IBGE/sinapi_202609caderno.pdf)
- Exemplo estadual (RN, set/2026): R$ 1.870,25/m², sendo R$ 1.134,45 em materiais e R$ 735,80 em mão de obra. — [Agora RN](https://agorarn.com.br/economia/custo-da-construcao-civil-desacelera-no-rn-e-chega-a-r-1-870-por-metro-quadrado/)

**CUB/m² (NBR 12721:2006)**
- O CUB é calculado conforme a Lei 4.591/64 e a ABNT NBR 12.721:2006, sobre projetos-padrão: residenciais R-1 (unifamiliar), PP-4, R-8, R-16 e PIS, nos padrões Baixo, Normal e Alto. — [Sinduscon-PR, CUB set/2026 (PDF)](https://sindusconpr.com.br/wp-content/uploads/2026/10/2026-9-Tabela-CUB-m2.pdf)
- O CUB **exclui**: fundações, submuramentos, elevadores, equipamentos e instalações (fogões, aquecedores, bombas, ar-condicionado etc.), obras complementares, urbanização, piscinas, ajardinamento, impostos, taxas, emolumentos, projetos, remuneração do construtor e do incorporador. — [Sinduscon-PR set/2026](https://sindusconpr.com.br/wp-content/uploads/2026/10/2026-9-Tabela-CUB-m2.pdf); [Sinduscon-MG abr/2025](https://sinduscon-mg.org.br/wp-content/uploads/2025/05/tabela_cub_abril_2025.pdf)
- **Paraná, setembro/2026** (emitido em 01/10/2026), em R$/m²: R1-B 2.681,59; **R1-N 3.365,21**; R1-A 4.109,51; PIS 1.869,10; RP1Q 2.903,54. — [Sinduscon-PR](https://sindusconpr.com.br/wp-content/uploads/2026/10/2026-9-Tabela-CUB-m2.pdf)
- **Minas Gerais, abril/2025** (dado antigo), em R$/m²: R1-B 2.353,75; R1-N 2.818,52; R1-A 3.511,46. — [Sinduscon-MG](https://sinduscon-mg.org.br/wp-content/uploads/2025/05/tabela_cub_abril_2025.pdf)
- **São Paulo, abril/2026**: R-1 Padrão Normal R$ 2.578,86/m². Setembro/2026: CUB global R8-N R$ 2.238,58/m², alta de 0,13% no mês (materiais +0,15%, mão de obra +0,11%). — [portaldori abr/2026](https://portaldori.com.br/2026/05/05/sinduscon-divulga-tabelas-de-custo-unitario-basico-no-estado-de-sao-paulo-referencia-abril-de-2026/); [Sinduscon-SP](https://sindusconsp.com.br/cub-paulista-sobe-013-em-setembro/)
- O CUB soma materiais, mão de obra, despesas administrativas e equipamentos (locação de betoneiras e máquinas), dividida pela área. — [VRI Consulting](https://www.vriconsulting.com.br/indices/cub-sp-r8n-sem-desoneracao.php)
- Participação citada para o CUB paulista R8-N (data não clara na fonte): 58,22% mão de obra, 38,38% materiais, 3,40% despesas administrativas. — [VRI Consulting (via busca)](https://www.vriconsulting.com.br/indices/cub-sp-r8n-com-desoneracao.php)

**Composições paramétricas e TCPO**
- Desde 2022 o SINAPI publica **composições paramétricas** para estudos de viabilidade antes do projeto básico. — [Caixa SINAPI](https://www.caixa.gov.br/sinapi)

### Inferences
- A parcela de materiais no custo SINAPI/IBGE (set/2026) é 1.127,17 / 1.999,73 ≈ **56%**. No CUB-SP R8-N a fonte cita ≈ 38%. As duas razões não se comparam diretamente: o projeto de referência e os itens incluídos diferem, e o CUB inclui despesas administrativas. Isso precisa ficar documentado no app. Para validação grosseira, o custo de materiais de uma casa média (R1-N) tende a ficar entre ~40% e ~56% do CUB R1-N da UF.
- O CUB serve como **verificação de sanidade** do total. Exemplo: material estimado / área construída comparado com 0,4–0,56 × CUB R1-N da UF. Ele não serve para orçar a partir de quantidades.
- O SINAPI é a base certa para o motor determinístico. Ele dá (a) preço por insumo por UF por mês, (b) coeficientes de consumo por unidade de serviço e (c) horas de mão de obra separadas, o que deixa a mão de obra estimável depois sem mudar o modelo.
- Risco de continuidade: a série 2025 teve meses zerados e retificados. O ETL precisa validar preços nulos ou zerados e permitir fallback para o mês anterior.

### Gaps
- **Licença de reuso do SINAPI:** não achei nenhum termo de licença explícito nas páginas consultadas. Por ser dado público federal, a redistribuição tende a ser permitida, mas isso é hipótese não verificada. Confirmar no portal da Caixa ou via LAI antes de embutir a base no repositório.
- Não consegui abrir as páginas da Caixa diretamente (loop de redirect). A URL exata do ZIP mais recente (out/2026) não foi verificada.
- **TCPO (PINI):** não coletei dados nesta rodada. Até onde sei, é uma base comercial paga de composições, o que a torna inadequada para um app offline gratuito. Fonte não verificada nesta pesquisa.
- Não achei a divisão materiais/mão de obra do CUB R1-N (só R8-N, sem data clara).
- A tabela por UF do boletim IBGE ficou desalinhada na extração do PDF, então não reproduzi valores por UF além do RN.

## 2. Taxas de consumo por serviço (coeficientes SINAPI)

### Takeaway
As composições SINAPI dão consumo de material por m² com **perdas já incorporadas** e regras de medição (área líquida, descontando vãos). Bastam cerca de 10 composições para cobrir alvenaria, revestimentos de parede e teto, contrapiso, piso cerâmico e pintura de uma casa térrea.

### Cited Findings
Todos os coeficientes são por m² de serviço. Fonte: espelho Orçamentor da base SINAPI. Base e data indicadas em cada linha.

**Alvenaria de vedação**
- **SINAPI 103329** (base ago/2024, média nacional), alvenaria de bloco cerâmico 9x19x19 furado na horizontal, argamassa manual, AF_12/2021:
  - bloco 8 furos 9x19x19: **28,31 un/m²**
  - argamassa 1:2:8 (cimento, cal, areia): **0,0091 m³/m²**
  - tela galvanizada: 0,42 m/m²
  - pino de aço: 0,005 cento/m²
  - mão de obra: pedreiro 1,61 h/m², servente 0,805 h/m²
  - custo total R$ 107,14/m², dos quais o bloco é R$ 22,08 (R$ 0,78/un)
  - **perda de blocos de 13,2%**. A argamassa considera junta média real de 10 mm aplicada com bisnaga ou palheta. Com colher de pedreiro, **multiplicar o consumo por 1,76**.
  - medir a área líquida descontando todos os vãos. Válida até 3,00 m de altura.
  — [Orçamentor 103329](https://orcamentor.com/composicao/103329/)
- **SINAPI 103324** usa bloco 14x19x39 com 13,6 un/m² (descrição oficial não confirmada). — [Orçamentor 103324 (via busca)](https://orcamentor.com/composicao/103324/)

**Chapisco**
- **SINAPI 87879** (09/2026, não desonerado), chapisco interno com colher, argamassa 1:3:
  - argamassa: **0,0037 m³/m²**
  - camada de 3 a 5 mm, perdas incluídas
  - custo R$ 5,41/m²
  — [Orçamentor 87879](https://orcamentor.com/composicao/87879/)

**Emboço / massa única (cimento + cal)**
- **SINAPI 87529** (09/2026, não desonerado), massa única 1:2:8 com betoneira, paredes internas, ambientes de 5–10 m², e = 17,5 mm:
  - argamassa: **0,0304 m³/m²**. As notas falam em espessura média real de 20 mm, com perdas incorporadas e por entulho.
  - mão de obra: pedreiro 0,4724 h/m², servente 0,2362 h/m²
  - custo R$ 43,79/m², dos quais a argamassa é R$ 18,59 (R$ 611,69/m³)
  — [Orçamentor 87529](https://orcamentor.com/composicao/87529/)

**Emboço / massa única com argamassa industrializada (projetada)**
- **SINAPI 87783**: argamassa industrializada projetada em fachada com vãos, e = 35 mm, **0,0421 m³/m²** mais tela 0,1388 m²/m². Outra variante tem 0,0393 m³/m². Perdas pela espessura média real (exemplo citado: 25 mm). — [Orçamentor 87783 (via busca)](https://orcamentor.com/composicao/87783/)

**Gesso liso**
- **SINAPI 87433** (09/2026, não desonerado), gesso projetado em paredes, desempenado, 1,0 cm:
  - argamassa de gesso: **0,01712 m³/m²** (comp. 87410, R$ 941,21/m³, já inclui o equipamento de projeção)
  - mão de obra: gesseiro 0,37042 h/m², servente 0,1173 h/m²
  - custo R$ 33,58/m²
  — [Orçamentor 87433](https://orcamentor.com/composicao/87433/)
- A composição auxiliar 87410 consome cerca de **1.094,55 kg de gesso por m³** de argamassa projetada. Insumo gesso projetado 36870, saco de 40 kg. — [Orçamentor (via busca)](https://orcamentor.com/composicao/87410/)
- Variantes existentes: projetado 0,5 cm (87430) e sarrafeado 1,0 e 1,5 cm (87436, 87439); manual desempenado 0,5 cm (87418) e 1,0 cm (87421); manual sarrafeado 1,5 cm (87427). — [Orçamentor, grupo Gesso](https://orcamentor.com/grupo/161/)

**Contrapiso**
- **SINAPI 87630** (09/2026, não desonerado), contrapiso 1:4 aderido sobre laje, área seca, 3 cm nominal:
  - argamassa: **0,0431 m³/m²**, que corresponde a uma espessura real de 4,31 cm (perdas maiores quanto menor a espessura)
  - aditivo adesivo: 0,21 L/m²
  - cimento para ponte de aderência: 0,5 kg/m²
  - custo R$ 44,16/m², dos quais a argamassa é R$ 27,52 (R$ 638,59/m³)
  — [Orçamentor 87630](https://orcamentor.com/composicao/87630/)

**Piso cerâmico / porcelanato**
- **SINAPI 87263** (09/2026, não desonerado), porcelanato 60x60 em ambientes > 10 m²:
  - placa: **1,069 m²/m²**
  - argamassa colante AC III: **9,13 kg/m²**
  - rejunte cimentício: **0,141 kg/m²**
  - mão de obra: azulejista 0,5203 h/m², servente 0,1674 h/m²
  - custo R$ 113,68/m², dos quais a placa é R$ 67,40 (R$ 63,05/m²) e a AC III R$ 20,99 (R$ 2,30/kg)
  - perdas incluídas nos coeficientes; espaçadores de 1–3 mm excluídos
  — [Orçamentor 87263](https://orcamentor.com/composicao/87263/)
- **SINAPI 87261**, mesmo serviço em ambientes < 5 m²: cerca de 1,13 m² de placa por m² e 1,11 h de azulejista. Ambientes pequenos têm perda maior e produtividade menor. — [Orçamentor (via busca)](https://orcamentor.com/composicao/87261/)
- Há composições de cerâmica esmaltada 60x60 (ex.: 87256, com AC I) e rodapé cerâmico 7 cm (88650). — [Orçamentor, grupo CINT](https://orcamentor.com/grupo/156/)

**Pintura**
- **SINAPI 88497** (09/2026), emassamento com massa látex (massa corrida acrílica para interior, NBR 15348), 2 demãos:
  - massa: **1,3389 kg/m²** (R$ 3,99/kg)
  - lixa nº 120: 0,0802 un/m²
  - pintor 0,361 h/m²
  - custo R$ 23,32/m²
  — [Orçamentor 88497](https://orcamentor.com/composicao/88497/)
- **SINAPI 88489** (09/2026), látex acrílica premium em paredes, 2 demãos (selador e massa não inclusos):
  - tinta: **0,2285 L/m²** (inclui uma camada de retoque), ou seja, cerca de 4,4 m²/L de área acabada
  - pintor 0,1631 h/m²
  - custo R$ 15,43/m², dos quais a tinta é R$ 7,35 (R$ 32,19/L)
  — [Orçamentor 88489](https://orcamentor.com/composicao/88489/)

### Inferences
- **Bloco 9x19x19:** 1 / (0,20 × 0,20) = 25 un/m² teórico; 25 × 1,132 ≈ 28,3 confere com o coeficiente 28,31. O dataset pode guardar consumo teórico e fator de perda separados, para recalcular com outros formatos de bloco.
- **Comparação de revestimento de parede interna** (só material, coeficientes SINAPI 09/2026):
  - cimento + cal: chapisco 0,0037 + massa única 0,0304 = **0,0341 m³/m²** de argamassa ≈ R$ 2,06 + R$ 18,59 = **R$ 20,65/m²** (preço de argamassa produzida, que inclui o preparo; não é material puro)
  - gesso projetado 1 cm: **0,01712 m³/m²**, ≈ 18,7 kg de gesso/m² (0,01712 × 1.094,55), ≈ R$ 16,11/m² de argamassa projetada (inclui equipamento)
  - o gesso dispensa a massa corrida em parede seca. Isso não foi confirmado na composição, que não diz se dispensa chapisco ou emboço; o insumo 36870 é descrito como dispensando chapisco, emboço e reboco.
  - o gesso não serve para áreas molhadas nem para fachadas (conhecimento de prática, não verificado aqui)
- **Tinta por classe:** a cartilha ABRAFATI define o rendimento declarado como área acabada por embalagem (todas as demãos). O consumo teórico fica então em 18 / 70 = 0,257 L/m² (econômica), 18 / 90 = 0,200 L/m² (standard), 18 / 110 = 0,164 L/m² (premium) e 18 / 150 = 0,120 L/m² (super premium). O SINAPI premium prático (0,2285 L/m²) é cerca de 1,39 × o teórico premium. Aplicar o mesmo fator às outras classes é hipótese.
- Teto: os coeficientes de parede são aproximação razoável, mas o SINAPI tem composições próprias para teto, com produtividade pior e às vezes espessura diferente (ver Gaps).

### Gaps
- Não coletei as composições SINAPI de **teto** (chapisco, emboço e gesso em teto), de **revestimento cerâmico de parede** (azulejo), de **fundo selador** nem a desagregação das argamassas auxiliares em insumos puros (kg de cimento, kg de cal, m³ de areia por m³ de 1:2:8, 1:3 e 1:4). Isso vem do relatório "Analítico de Composições" ou "Famílias e Coeficientes" (XLSX) da Caixa.
- Orçamentor mostra "média nacional". A Caixa publica por UF, então a origem dessa média (cálculo do espelho?) não foi verificada.
- **Reboco fino (camada separada do emboço):** o SINAPI atual trabalha com "massa única" ou "emboço". Não verifiquei se ainda existe composição de reboco separado.
- TCPO não consultado (base paga).

## 3. Classes de acabamento: normas e amostras de preço por classe (2025–2026)

### Takeaway
A tinta é o único item com classificação normativa que mapeia direto para as 3 classes do usuário. A **ABNT NBR 15079:2019** define Econômica, Standard, Premium e Super Premium, com rendimento teórico mínimo. Para os demais itens a classe tem de ser definida pelo projeto, por especificação técnica (PEI, retificado, tipo de AC) e por faixa de marca ou preço. O próprio SINAPI já codifica algumas classes na descrição do insumo (ex.: "tinta látex acrílica premium", "porcelanato retificado extra", "cerâmica esmaltada PEI ≥ 4").

### Cited Findings
**Tintas: NBR 15079 (oficial)**
- A NBR 15079 foi revista em 25/09/2019 e é obrigatória desde 26/03/2021.
  - parte 1: tintas látex foscas Econômica, Standard, Premium e o novo nível Super Premium
  - parte 2: acabamentos acetinado, semiacetinado e semibrilho
  - a embalagem passou a declarar rendimento em m²/embalagem de área efetivamente coberta (NBR 14942:2019, item 7.4)
  — [ABRAFATI, Cartilha sobre Mudanças Normativas](https://abrafati.com.br/wp-content/uploads/2024/12/Cartilha-sobre-Mudancas-Normativas.pdf)
- Rendimento teórico mínimo, látex fosca (m²/18 L): **Econômica 70; Standard 90; Premium 110; Super Premium 150**. Semibrilho, acetinada e semiacetinada: Standard 70 (semibrilho) e 90 para os demais níveis. — [ABRAFATI Cartilha](https://abrafati.com.br/wp-content/uploads/2024/12/Cartilha-sobre-Mudancas-Normativas.pdf). Nota: o layout da tabela no PDF extraído é ambíguo para a parte 2. Os valores da fosca são confirmados pelo texto ("tinta econômica fosca pode ter o rendimento teórico de 70 m²/18L") e pelo resumo da busca.
- O rendimento prático varia com substrato, preparo, aplicador e clima. — [ABRAFATI Cartilha](https://abrafati.com.br/wp-content/uploads/2024/12/Cartilha-sobre-Mudancas-Normativas.pdf)
- Tintas econômicas são indicadas só para uso interno. — [Sienge (resumo ABRAFATI, via busca)](https://sienge.com.br/blog/na-compra-de-tintas-o-planejamento-faz-toda-diferenca/)
- O PSQ Tintas Imobiliárias (PBQP-H) verifica a conformidade com a NBR 15079. — [PBQP-H](https://pbqp-h.mdr.gov.br/wp-content/uploads/2021/09/Fundamentos-do-PSQ-Tintas-IT084.pdf)

**Amostras de preço: referência oficial SINAPI (média nacional, 09/2026 não desonerado, salvo indicação)**

| Insumo (cód.) | Unid. | Preço | Base | Fonte |
|---|---|---|---|---|
| Tinta látex acrílica premium branco fosco (7356) | L | R$ 32,19 | 09/2026 | [Orçamentor 88489](https://orcamentor.com/composicao/88489/) |
| Massa corrida interna (43626) | kg | R$ 3,99 | 09/2026 | [Orçamentor 88497](https://orcamentor.com/composicao/88497/) |
| Porcelanato retificado liso monocolor > 2500 até 6400 cm² (45190) | m² | R$ 63,05 | 09/2026 | [Orçamentor 87263](https://orcamentor.com/composicao/87263/) |
| Argamassa colante AC III (37595) | kg | R$ 2,30 | 09/2026 | idem |
| Rejunte cimentício (34357) | kg | R$ 4,40 | 09/2026 | idem |
| Argamassa 1:2:8 betoneira (comp. 87292) | m³ | R$ 611,69 | 09/2026 | [Orçamentor 87529](https://orcamentor.com/composicao/87529/) |
| Argamassa 1:4 contrapiso (comp. 87301) | m³ | R$ 638,59 | 09/2026 | [Orçamentor 87630](https://orcamentor.com/composicao/87630/) |
| Argamassa de gesso projetada (comp. 87410) | m³ | R$ 941,21 | 09/2026 | [Orçamentor 87433](https://orcamentor.com/composicao/87433/) |
| Cimento CP II-32 (1379) | kg | R$ 0,72 | 09/2026 | [Orçamentor 87630](https://orcamentor.com/composicao/87630/) |
| Bloco cerâmico 8 furos 9x19x19 (7271) | un | R$ 0,78 | **ago/2024 (antigo)** | [Orçamentor 103329](https://orcamentor.com/composicao/103329/) |
| Porcelanato polido retificado liso | m² | R$ 73,16 | mai/2026 | guia citado na busca ([Leroy/guias](https://chamaopro.com.br/blog/melhores-marcas-porcelanato/)), fonte secundária |

**Amostras de varejo (indicativas; nenhuma página mostrava data, coletadas por busca em nov/2026; UF não informada salvo indicação)**
- **Tinta látex fosca 18 L** (lojas online, sem UF):
  - Econômica: Coralar Econômico Fosco R$ 259,90 (Casa Toni); Coralar + Desempenho R$ 209,90–211,90 (Bela Tintas)
  - Standard: Coral Rende Muito Fosco R$ 446 (Casa Toni), R$ 469–470 em outros anúncios; Suvinil Rende e Cobre Muito R$ 444–517 (Zoom, Buscapé)
  - Premium: Suvinil Toque Fosco Completo R$ 568–844; Coral Premium Super Lavável Antimanchas R$ 876,63 (Magazine Luiza); Coral Decora Diamante R$ 846–1.029 (Mercado Livre)
  - — [Casa Toni](https://www.casatoni.com.br/tintas/acrilicos); [Bela Tintas](https://www.belatintas.com.br/coral); [Zoom](https://www.zoom.com.br/busca/tinta+suvinil+18+litros+coral); [Buscapé](https://www.buscape.com.br/busca/tinta+coral+18+litros+tinta+acr%C3%ADlica); [Magazine Luiza](https://www.magazineluiza.com.br/busca/tinta+coral+18+litros/); [Mercado Livre](https://lista.mercadolivre.com.br/tintas-coral-18-litros)
- **Bloco cerâmico 9x19x19:**
  - guia 2026: R$ 650–1.050/milheiro
  - Telhanorte (Nova Conquista): R$ 1,25/un (R$ 1,18 no Pix), ≈ R$ 1.180–1.250/milheiro; site com seleção de região, provavelmente SP
  - anúncio OLX (Anápolis/GO): R$ 1.150/milheiro
  - — [Lar Pontual](https://larpontual.com.br/portal/preco-do-milheiro-de-tijolo); [Telhanorte](https://www.telhanorte.com.br/bloco-ceramico-09x19x19cm-nova-conquista-219533/p); [OLX](https://www.olx.com.br/anuncios/milheiro-de-blocos)
- **Cimento CP II 50 kg:**
  - guia 2026: R$ 32–48 (CP V ARI R$ 38–58)
  - média citada de R$ 46,00 no 1º bimestre/2026 (atribuída a SINAPI/SNIC, não verificada)
  - exemplo regional: R$ 32 em Contagem/MG contra R$ 46 em Belém/PA (efeito do frete)
  - — [Reforme Construa](https://www.reformeconstrua.com.br/precos/cimento-saco-50kg); [BR104](https://www.br104.com.br/economia/evolucao-preco-cimento-10-anos-brasil-2026/); [Calculobra](https://calculobra.online/blog/preco-do-cimento-2026)
- **Porcelanato** (Leroy Merlin, preço varia por região):
  - categoria vai de cerca de R$ 29/m² a mais de R$ 90/m²
  - Eliane Marmorizado Acetinado 90x90: R$ 76,90/m²
  - Portobello Cimentício 90x90 Hit Off White: R$ 92,97/m²
  - Eliane Cimentício 60x120: R$ 112,71/m²
  - Portobello 120x120: R$ 239,61–244,31/m²
  - guias de marca: Eliane R$ 60–220/m², Portobello R$ 80–300/m²; PEI 3 contra PEI 4 da mesma marca raramente difere mais de R$ 10/m²
  - — [Leroy Merlin](https://www.leroymerlin.com.br/porcelanatos/melhor-preco); [Leroy Eliane](https://www.leroymerlin.com.br/porcelanatos/marca/Eliane); [Chama o Pro](https://chamaopro.com.br/blog/melhores-marcas-porcelanato/)
- **Bacia para caixa acoplada (louça):**
  - Incepa Zip: R$ 214,90 (Telhanorte)
  - Celite Saveiro: ≈ R$ 219,90
  - Deca Izy: R$ 358,90
  - Deca Vogue Plus: R$ 1.199,90
  - kits Celite com caixa e assento: R$ 1.059–1.299 (Obramax)
  - — [Telhanorte](https://www.telhanorte.com.br/loucas/vasos-sanitarios-e-assentos/bacias-para-caixas-acopladas); [Obramax](https://www.obramax.com.br/banheiros/vasos-sanitarios-e-acessorios/vasos-sanitarios-com-caixa-acoplada); [Obramax blog](https://blog.obramax.com.br/acabamento-decoracao/melhores-marcas-de-vaso-sanitario/)
- **Cabo flexível 2,5 mm², 750 V, rolo 100 m:**
  - Cobrecom: R$ 249,90 (Telhanorte)
  - Sil: R$ 247–278 no Pix (Magazine Luiza); terceiros entre R$ 164 e R$ 461,90 conforme cor e vendedor
  - há alerta de cabos com pouco cobre: exigir NBR NM 247-3
  - — [Telhanorte Cobrecom](https://www.telhanorte.com.br/-cabo-flexivel-750-volts-2-5-mm2-100-metros-cobrecom-256013/p); [Magazine Luiza](https://www.magazineluiza.com.br/busca/cabo+flexivel+sil)

### Inferences
- **Mapeamento proposto de classes:**
  - econômica = tinta Econômica (só interna) ou Standard; média = Standard ou Premium; alto padrão = Premium ou Super Premium de marca consolidada
  - preço por litro de varejo (fosca 18 L): econômica ≈ R$ 12–14/L, standard ≈ R$ 25–29/L, premium ≈ R$ 32–57/L
  - combinado com o consumo teórico por classe, o custo de tinta por m² **varia menos do que o preço por litro sugere**. Exemplo: econômica 0,257 L/m² × R$ 13 ≈ R$ 3,3/m² contra premium 0,164 L/m² × R$ 45 ≈ R$ 7,4/m² (só tinta, rendimento teórico; cálculo do agente)
- **Pisos:** econômica = cerâmica esmaltada PEI 4 em formato pequeno ou médio com AC I/AC II; média = porcelanato 60x60 de marca intermediária com AC III; alto = porcelanato retificado em grande formato (90x90 ou mais) de marca consolidada, com AC III e mais perda. Formato maior pede coeficientes de perda e argamassa diferentes (o SINAPI tem composições por formato).
- **Louças e metais:** a dispersão de varejo é de 5x ou mais dentro de uma mesma marca (Deca R$ 359 contra R$ 1.200). A classe deve ser definida por faixa de preço ou linha, não só por marca.
- O preço do bloco no SINAPI (R$ 0,78, ago/2024) está bem abaixo do varejo de 2026 (R$ 0,65–1,25/un). Para o dataset, usar sempre o SINAPI do mês e UF corretos e marcar o varejo como "amostra".

### Gaps
- **Cerâmica (NBR ISO 13006 / NBR 13818: PEI, grupos de absorção BIa porcelanato ≤ 0,5%, classes A/B/C de qualidade):** não verifiquei em fonte primária nesta rodada. A informação existe, mas fica fora das notas por não ter fonte.
- **Hidráulica (PVC soldável vs. PPR vs. PEX), disjuntores, tomadas e interruptores (linhas econômicas vs. premium):** não encontrei preços com fonte nesta rodada.
- **Metais sanitários (torneiras, registros, chuveiros) e argamassa industrializada em saco:** sem preços coletados.
- Nenhum preço de varejo tem data de coleta explícita na página nem UF garantida. Uma coleta sistemática exigiria scraping datado por UF, o que não foi feito.
- O valor de R$ 73,16/m² (porcelanato, SINAPI mai/2026) é citação secundária.

## 4. Itens que dominam o custo de material e esquema de dados recomendado

### Takeaway
As fontes concordam em ordem de grandeza, não em números: **acabamentos (pisos, revestimentos, louças, metais, pintura) ficam com ~30–50%** do custo, **estrutura + alvenaria + cobertura com ~15–45%** e **instalações elétricas e hidráulicas com ~15–20%**. A coleta deve priorizar piso e revestimento cerâmico, argamassas e cimento, blocos, aço e concreto, telhado, louças e metais, tinta e fios.

### Cited Findings
- Faixas por etapa em guias de mercado de 2026 (não padronizadas):
  - estrutura (concreto, aço, alvenaria): 15–25% numa fonte; "estrutura e alvenaria" com fundação, ferro e telhado: 40–45% noutra
  - instalações elétricas e hidráulicas: 15–20%
  - acabamentos: 30–40%, 35–40% (classe média) ou 43–50% ("pisos, louças, metais e pintura")
  - projetos e taxas: 5–12%
  — [resumo de busca: Olhar Digital 2026](https://olhardigital.com.br/curiosidades/2026/05/30/quanto-custa-construir-uma-casa-de-3-quartos-com-acabamento-de-classe-media-em-2026/); [Lar Pontual](https://larpontual.com.br/portal/web-stories/quanto-custa-construir-casa); [Click Petróleo e Gás](https://clickpetroleoegas.com.br/levantamento-mostra-quanto-custa-cada-etapa-de-uma-obra-de-10-mil-m%c2%b2-em-2026-com-o-percentual-do-orcamento-que-vai-para-fundacao-estrutura-alvenaria-cobertura-eletrica-hidraulica-mhbb01/)
- Um artigo sobre casas de 100 m² afirma que o revestimento é a etapa mais cara, à frente de fundação e estrutura. Isso contradiz parcialmente as outras fontes, que não separam o revestimento. — [resumo de busca, Olhar Digital](https://olhardigital.com.br/2026/04/15/curiosidades/quanto-custa-levantar-uma-casa-simples-de-3-quartos/)
- Dentro das composições SINAPI, o material pesa de forma muito diferente:
  - porcelanato 60x60: placa + AC + rejunte = R$ 89,01 de R$ 113,68 (~78%)
  - alvenaria 9x19x19: R$ 29,54 de R$ 107,14 (~28%)
  - pintura premium: R$ 7,35 de R$ 15,43 (~48%)
  - emassamento: R$ 5,44 de R$ 23,32 (~23%)
  — [Orçamentor 87263](https://orcamentor.com/composicao/87263/); [103329](https://orcamentor.com/composicao/103329/); [88489](https://orcamentor.com/composicao/88489/); [88497](https://orcamentor.com/composicao/88497/)
- O SINAPI publica um relatório XLSX de "Percentual de Mão de Obra em Composições", que permite separar material de mão de obra por serviço. — [Caixa SINAPI](https://www.caixa.gov.br/sinapi)

### Inferences
**Esquema de dados recomendado** (proposta do agente; ainda não decidido pelo responsável). Separar *o que* se consome (receita do serviço) de *quanto custa* (preço por UF e data) e de *qual variante* a classe escolhe:

```text
insumo(
  id, codigo_sinapi?, descricao, unidade,          -- kg, L, m², m³, un
  categoria,                                       -- tinta, bloco, cerâmica, louça, fio...
  classe_acabamento?,                              -- economica | media | alto | NULL (neutro)
  norma_ref?,                                      -- "NBR 15079-1 Premium", "PEI 4", "AC III"
  rendimento_teorico?, unidade_rendimento?         -- ex.: 110 m²/18L
)
preco_insumo(
  insumo_id, uf, municipio?, data_referencia (AAAA-MM),
  preco, moeda='BRL',
  fonte_tipo,                                      -- sinapi | varejo | cotacao_usuario
  fonte_nome, fonte_url, desonerado?,              -- desonerado só afeta mão de obra
  coletado_em, observacao
)
servico(                                           -- equivale à composição SINAPI
  id, codigo_sinapi?, descricao, unidade,
  driver_quantidade,                               -- ver lista abaixo
  validade                                         -- ex.: "altura ≤ 3 m", "área > 10 m²"
)
servico_item(
  servico_id, insumo_id | subservico_id,
  coeficiente,                                     -- por unidade de serviço, perdas incluídas
  consumo_teorico?, fator_perda?,                  -- opcional, para recalcular
  tipo                                             -- material | mao_de_obra | equipamento
)
classe_variante(                                   -- qual serviço/insumo cada classe usa
  servico_generico,                                -- ex.: "pintura_parede_interna"
  classe, servico_id, insumo_overrides(json)
)
dataset_meta(versao, sinapi_mes_ref, uf_padrao, gerado_em, licenca/nota_de_fonte)
```

- **Drivers de quantidade** que saem do modelo central da planta:
  - área líquida de parede, por face e por ambiente, descontando vãos
  - área de teto
  - área de piso, por ambiente e por tipo seco ou molhado
  - perímetro, para rodapé
  - área de parede molhada, para azulejo
  - contagens: louças, metais, pontos elétricos (tomadas e interruptores), pontos hidráulicos, portas e janelas
  - comprimento estimado de circuito (fio)
- **Mão de obra:** guardar já as horas de `servico_item` com `tipo = mao_de_obra`. O custo de material é a soma de `coef × preço` só dos itens de material; o custo de mão de obra depois vem dos mesmos coeficientes vezes o salário-hora com encargos (desonerado ou não).
- **Faixa de área:** o SINAPI tem composições diferentes por faixa de área de ambiente (< 5 m², 5–10 m², > 10 m²). O motor pode escolher a composição pela área do cômodo, o que é determinístico e coerente com a planta.
- **Validação:** comparar o material total / área construída com a parcela de materiais do SINAPI/IBGE da UF (≈ 56% do custo médio nacional em set/2026) e com o CUB R1 da classe (B, N, A) da UF.
- **ETL:** importar o XLSX mensal do SINAPI de uma UF, filtrar um subconjunto curado de cerca de 30–60 composições e 80–150 insumos relevantes para casa térrea e guardar como arquivo versionado (CSV ou JSON) no pacote, para manter o app offline. Varejo entra como camada opcional de "amostra", sempre com data, UF e URL.

### Gaps
- Não há fonte primária (estudo acadêmico ou SINAPI paramétrico) com a distribuição percentual de **material** por etapa para uma casa R1. As faixas acima são de guias de mercado e misturam material com mão de obra. As composições paramétricas do SINAPI ou o orçamento discriminado do projeto-padrão R1 da NBR 12721 seriam a fonte melhor, e não foram consultadas.
- Fundação, estrutura (concreto e aço), cobertura (telhado), esquadrias e instalações não tiveram coeficientes coletados nesta rodada. O app talvez não tenha quantidades para estrutura e fundação a partir de uma planta 2D; isso é decisão de escopo pendente.
