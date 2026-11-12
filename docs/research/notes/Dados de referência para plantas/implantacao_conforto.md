# Implantação, parâmetros urbanísticos e conforto ambiental para casas no Brasil

> Notas de pesquisa (coletadas em 2026-11-11). Legenda usada ao longo do texto:
> **[NORMA/LEI]** = valor legal ou normativo; **[BOA PRÁTICA]** = recomendação técnica ou acadêmica; **[POPULAR]** = conhecimento difundido sem base normativa; **[NÃO VERIFICADO]** = lembrança do agente que não conseguiu confirmar na fonte primária nesta sessão (ver Gaps). Valores marcados como [NÃO VERIFICADO] **não devem virar default** sem conferência.
>
> Limitação técnica desta rodada: vários PDFs (NBR 15220-3 no site do LabEEE, nota técnica da NBR 15575, artigos do ENTAC) vieram como binário comprimido e não puderam ser lidos (não havia extrator de PDF no ambiente). Por isso, várias tabelas foram obtidas por resumos secundários. As cópias binárias ficaram salvas localmente em `C:\Users\paulo\.claude\projects\c--Users-paulo-AREA-DE-TRABALHO-PyGridPlan\91e87952-46c4-4beb-9b3a-d5183159ee7a\tool-results\` (webfetch-1794440707374-fktq1d.pdf = NBR 15220-3 versão 2004/2005 do LabEEE; webfetch-1794440753685-4a7hma.pdf = NT 15575 do LabEEE; webfetch-1794440769198-p0as0l.pdf = artigo ENTAC 2092) e podem ser extraídas depois com `pdftotext`.

## 1. Orientação solar por cômodo, zonas bioclimáticas (NBR 15220-3) e NBR 15575

### Takeaway
No Brasil (majoritariamente hemisfério sul), a fachada norte recebe mais sol direto ao longo do ano, sobretudo no inverno. A boa prática é pôr os cômodos de permanência prolongada (dormitórios, estar) a norte/leste e os de serviço e curta permanência (cozinha, área de serviço, banheiros) a sul/oeste, com proteção solar na fachada oeste. A NBR 15220-3 mudou: a edição de 2005 tinha 8 zonas, e uma nova edição foi publicada em 12/2024 com outro zoneamento. As fontes divergem sobre o número final de zonas (12 ou 6). Isso afeta qualquer tabela "por zona" que o gerador use.

### Cited Findings
**Orientação por cômodo [BOA PRÁTICA]**
- No Brasil, o Sol percorre o céu com predominância ao norte, então fachadas voltadas para o norte tendem a receber maior incidência solar anual direta, especialmente no inverno. [POPULAR/divulgação técnica] — [Sienge, "Posição solar e andar do imóvel"](https://sienge.com.br/blog/posicao-solar-e-andar-do-imovel/)
- Um projeto de referência do Prêmio Projeteee (GBC Brasil) põe as áreas íntimas na porção norte/leste e as áreas de serviço, de menor permanência, na porção oeste/sul, por serem as fachadas menos favorecidas. — [GBC Brasil, Memorial Descritivo (Prêmio Projeteee), 2018](https://gbcbrasil.org.br/wp-content/uploads/2018/05/Memorial_Descritivo_-2.pdf)
- Cozinha, banheiros e área de serviço podem receber menos sol por serem de menor permanência. Também se recomenda que o imóvel tenha faces que aproveitem o sol da manhã (leste). [POPULAR] — [Portas.com.br, "Como saber a posição solar de um imóvel ou terreno"](https://portas.com.br/morar-bem/dicas-lar/como-saber-a-posicao-solar-de-um-imovel-ou-terreno/)
- Divergência: um fórum (Portugal) sugere áreas técnicas e de serviço a norte. Isso contradiz as fontes bioclimáticas brasileiras e deve ser tratado como opinião isolada. — [Fórum da Casa](https://forumdacasa.com/discussion/40366/melhor-exposicao-solar/)
- Em residências de Goiânia (ZB6 no zoneamento de 2005), as orientações norte e sul tiveram melhor desempenho térmico, mas o comportamento do usuário pesa bastante no resultado. — [ENCAC/ANTAC, artigo sobre residências em Goiânia](https://eventos.antac.org.br/index.php/encac/article/download/4303/3195/12762)

**Zoneamento bioclimático, NBR 15220-3 [NORMA]**
- A NBR 15220-3 (edição 2005) divide o território em **8 zonas bioclimáticas**. Traz diretrizes construtivas (tamanho das aberturas para ventilação, sombreamento, tipo de paredes e cobertura) e estratégias de condicionamento passivo para **habitações unifamiliares de interesse social de até 3 pavimentos**. As diretrizes por zona estão nas seções 6.1 a 6.8. — [LabEEE/UFSC, texto da NBR 15220-3 (2004/2005)](https://labeee.ufsc.br/sites/default/files/projetos/normalizacao/Termica_parte3_SET2004.pdf); resumo em [questão de concurso Gran Cursos](https://questoes.grancursosonline.com.br/questoes-de-concursos/legislacao-dos-orgaos-nbr-15220-3-abnt-396469)
- Faixas de abertura para ventilação, em % da **área de piso** do ambiente: **pequenas 10%–15%**, **médias 15%–25%**, **grandes ≥ 40%**. — [ENTAC/ANTAC, artigo que adapta a tabela da norma](https://eventos.antac.org.br/index.php/entac/article/download/1984/1810/6388) (via resumo de busca; o PDF não foi lido)
- Exemplo por zona: a **Z8** (ex.: Rio de Janeiro) pede **aberturas grandes e sombreadas**. A Z2 pede aberturas médias com sombreamento que deixe entrar sol no inverno. — [ENTAC/ANTAC](https://eventos.antac.org.br/index.php/entac/article/download/1984/1810/6388); [Gran Cursos](https://questoes.grancursosonline.com.br/questoes-de-concursos/engenharia-civil-39/3936049)
- Crítica: a norma de 2005 não cobre bem estratégias para clima subtropical e não tem estratégia de controle solar, o que deixa o condicionamento passivo de inverno insuficiente na Z3. — [ENTAC/ANTAC, artigo 2092](https://eventos.antac.org.br/index.php/entac/article/download/2092/1877/6495) (via resumo de busca)
- **Revisão 2024:** o LabEEE informa que o novo zoneamento foi "publicado em 2024 por meio da NBR 15220-3". Ele se baseia nos indicadores da NBR 15575, também vale para edificações não residenciais e foi feito com clustering/árvores de decisão. Os dados de entrada são cargas térmicas de aquecimento e resfriamento, percentual de horas ocupadas dentro da faixa de temperatura operativa e umidade relativa, com dados ERA5-Land, NASA-POWER, CRU e TMYx (2007–2021). Os **5.570 municípios** foram classificados, e o trabalho levou 18 reuniões entre 26/08/2021 e 14/03/2023. — [LabEEE/UFSC, página "Zoneamento bioclimático"](https://labeee.ufsc.br/pt-br/zoneamentobioclimatico)
- O catálogo da ABNT registra nova edição publicada em **12/2024**, com o título "Zoneamento bioclimático por desempenho". Há também uma ABNT TR 15220-3-1 com a lista de cidades. — [normas.com.br, NBR 15220-3](https://www.normas.com.br/visualizar/abnt-nbr-nm/24361/abnt-nbr15220-3-desempenho-termico-de-edificacoes-parte-3-zoneamento-bioclimatico-por-desempenho); [normas.com.br, TR 15220-3-1](https://www.normas.com.br/visualizar/abnt-nbr-nm/13893/abnt-tr15220-3-1-desempenho-termico-de-edificacoes-parte-3-1-zoneamento-bioclimatico-por-desempenho-lista-de-cidades-brasileiras)
- **Conflito sobre o número de zonas:** um trabalho da UFMS afirma que a revisão de 2024 passou de 8 para **12 zonas** ([UFMS](https://repositorio.ufms.br/retrieve/d202f4fe-0a24-4d86-898b-4f6755a83edb/32354.pdf)). Já o projeto de revisão do LabEEE (jun/2024, sem valor normativo) e o Guia ABRAINC 2025 usam **6 zonas**, de "muito fria" a "muito quente" ([LabEEE, projeto de revisão](https://labeee.ufsc.br/sites/default/files/documents/zoneamento_projeto.pdf); [ABRAINC, Guia de Boas Práticas em Eficiência Energética, 2025](https://cdn.abrainc.org.br/files/2026/4/Guia_de_Boas_Praticas_Eficiencia_Energetica__ABRAINC_2025_compressed.pdf)). Não foi possível resolver o conflito nesta sessão.
- Listas de cidades por região e mapa interativo do novo zoneamento: [LabEEE, mapa](https://labeee.ufsc.br/zoneamento/); [Norte](https://labeee.ufsc.br/sites/default/files/documents/NORTE.pdf), [Nordeste](https://labeee.ufsc.br/sites/default/files/documents/Nordeste.pdf), [Centro-Oeste](https://labeee.ufsc.br/sites/default/files/documents/Centro_Oeste.pdf), [Sudeste](https://labeee.ufsc.br/sites/default/files/documents/Sudeste.pdf), [Sul](https://labeee.ufsc.br/sites/default/files/documents/Sul.pdf); artigos de base: [Energy and Buildings 2024](https://doi.org/10.1016/j.enbuild.2024.114157), [Building and Environment 2024](https://doi.org/10.1016/j.buildenv.2024.112423)

**NBR 15575 (desempenho térmico) [NORMA]**
- A revisão de 2021 da NBR 15575 introduziu novos indicadores de desempenho térmico. Os ambientes avaliados são os **APP (ambientes de permanência prolongada): dormitórios e sala de estar/jantar, inclusive com cozinha integrada**. O **procedimento simplificado** compara as propriedades dos componentes com valores de referência, entre elas o percentual de abertura efetiva para ventilação dos APP, e só comprova o nível **Mínimo** (obrigatório). Os níveis Intermediário e Superior exigem **simulação computacional**. — [LabEEE, emenda NBR 15575-4 (out/2020)](https://labeee.ufsc.br/sites/default/files/documents/DT_NBR-15575-4_Emenda_Out2020.pdf); [Veiga et al., ENTAC 2020](https://labeee.ufsc.br/sites/default/files/documents/2020ENTAC-Proposta_para_as_escalas_dos_niveis_de_desempenho_termico_de_residencias_NBR15575-Veiga_et_al.pdf); [Krelling et al., ENTAC 2020](https://labeee.ufsc.br/sites/default/files/documents/2020ENTAC-Proposta_de_metodo_de_avaliacao_do_desempenho_termico_de_residencias_NBR15575-Krelling_et_al.pdf) (via resumo de busca)
- Em ZB2 (versão 2013), um artigo do ENTAC 2024 cita U ≤ 2,5 W/m²K para paredes e U ≤ 2,3 W/m²K para cobertura. — [ENTAC/ANTAC 5856](https://eventos.antac.org.br/index.php/entac/article/download/5856/4974/22454) (via resumo de busca)
- O procedimento simplificado mostra grande variabilidade de resultados conforme os dados de entrada (Chvatal, 2014). — [Ambiente Construído, "Avaliação do procedimento simplificado da NBR 15575"](https://seer.ufrgs.br/index.php/ambienteconstruido/article/view/45677)
- Um memorial de Curitiba (premiado pelo Projeteee) adota ventilação cruzada e aberturas **maiores que 7% da área de piso**, que podem ser fechadas no frio. Isso coincide com o mínimo da NBR 15575:2013 para ZB1–7 (ver Gaps). — [GBC Brasil, memorial descritivo](https://www.gbcbrasil.org.br/wp-content/uploads/2018/05/Memorial-descritivo-final-1.pdf)

### Inferences
- Default sugerido para o gerador: os pesos de orientação são um **soft constraint** (custo), não uma regra dura. Pesos "preferir N/L" para dormitórios e estar, "aceitar S/O" para serviço, cozinha, banheiros e garagem, e uma penalidade para janelas grandes de APP a oeste sem sombreamento.
- Como o zoneamento de 2024 substituiu o de 2005 e o número de zonas ainda não foi confirmado, o modelo de dados deveria guardar `zona_bioclimatica` com um campo de **versão do zoneamento** (`NBR15220-3:2005` ou `:2024`) e não fixar "8 zonas" no código.
- As faixas de abertura da NBR 15220-3:2005 (10–15 / 15–25 / ≥40% da área de piso) são áreas de **ventilação**, não de iluminação. O gerador deve calcular as duas separadamente.

### Gaps
- **Tabela completa por zona (Z1–Z8, 2005) não verificada na fonte primária**, porque o PDF não pôde ser lido. Pela memória do agente [NÃO VERIFICADO]: Z1–Z3 têm aberturas médias e sol permitido no inverno; Z4–Z6 têm aberturas médias e sombreadas; Z7 tem aberturas pequenas e sombreadas; Z8 tem aberturas grandes e sombreadas, com ventilação cruzada permanente. Só a Z8 e a Z2 foram confirmadas por fonte secundária.
- **NBR 15575 (2013), aberturas mínimas para ventilação em APP:** pela memória do agente [NÃO VERIFICADO], ≥ 7% da área de piso em ZB1–7; em ZB8, ≥ 8% (Nordeste e Sudeste) e ≥ 12% (Norte). Só os 7% aparecem indiretamente (memorial de Curitiba). Também não foram obtidos os valores da versão 2021/2024.
- **Variação por latitude (Norte equatorial):** não foi encontrada fonte citável nesta sessão. Princípio físico conhecido [NÃO VERIFICADO]: perto do Equador, o Sol passa ora ao norte, ora ao sul do zênite, e as fachadas leste/oeste são as mais críticas. A recomendação típica é concentrar aberturas a norte/sul, com beirais, e minimizar oeste. Precisa de fonte (Lamberts, Dutra & Pereira; Projeteee).
- O livro de Lamberts, Dutra & Pereira ("Eficiência energética na arquitetura") não foi consultado diretamente.
- Número de zonas da NBR 15220-3:2024 (12 ou 6) e as diretrizes por zona da nova edição.

## 2. Ventilação cruzada, posição das janelas e ventos predominantes

### Takeaway
A ventilação cruzada depende de diferença de pressão entre aberturas em fachadas **opostas ou adjacentes**. Duas janelas na mesma parede ventilam pouco. As aberturas devem se voltar para os ventos predominantes, e o tamanho segue a zona bioclimática (aberturas grandes no clima quente e úmido, Z8 de 2005).

### Cited Findings
- O Projeteee (MME) explica que diferenças de pressão movimentam o ar naturalmente. A disposição importa: duas janelas próximas na mesma parede funcionam diferente de aberturas em fachadas opostas ou adjacentes. Esquadrias pivotantes redirecionam o fluxo, as de correr não. [BOA PRÁTICA] — [Olhar Digital, citando o Projeteee](https://olhardigital.com.br/curiosidades/?p=36687)
- Projetos que citam a plataforma Projeteee listam como estratégia "aberturas direcionadas para os ventos predominantes" junto com ventilação cruzada. — [GBC Brasil, prancha do projeto de Goiânia](https://www.gbcbrasil.org.br/wp-content/uploads/2018/05/PRANCHA-goiania-1.pdf); [UFES, artigo sobre escola](https://lpp.ufes.br/sites/lpp.ufes.br/files/field/anexo/artigo237942.pdf)
- Ventilação natural pede cautela quando o ar externo está muito poluído. — [Olhar Digital/Projeteee](https://olhardigital.com.br/curiosidades/?p=36687)
- A NBR 15220-3:2005 recomenda, em algumas zonas, ventilação **só na primavera-verão**, e em outras nenhuma ventilação no inverno (abertura que possa ser fechada). — [resumos da NBR 15220-3 via busca](https://edisciplinas.usp.br/pluginfile.php/5660736/mod_folder/content/0/NBR%2015220/NBR15220-3.pdf)
- Simulação acadêmica (não normativa): entre percentuais de abertura de 20% e 40%, o de **20%** foi o que mais contribuiu para o conforto em todos os municípios estudados. — [ENTAC/ANTAC, via resumo de busca](https://eventos.antac.org.br/index.php/entac/article/download/5856/4974/22454)

### Inferences
- Regra implementável: para cada APP, dar bônus quando o cômodo tem janelas em **duas fachadas** (opostas > adjacentes) ou quando uma porta interna liga o cômodo a outro com janela na fachada oposta (ventilação cruzada pela planta). Dar penalidade para APP com uma única janela em clima quente e úmido.
- Entrada `vento_predominante` (direção em graus ou rumo N/NE/…): pontuar janelas de APP na fachada a barlavento e janelas de banheiro e serviço a sotavento, para que odores e umidade não atravessem a casa.

### Gaps
- Não foi obtida uma fonte primária com **rosas dos ventos por cidade**. Pela memória do agente [NÃO VERIFICADO], o Projeteee (projeteee.mma.gov.br) mostra dados climáticos por cidade, inclusive vento, mas a página não foi acessada nesta sessão. Os arquivos climáticos TMYx/INMET são outra via possível.
- Não há fonte para a regra "abertura de saída maior que a de entrada" nem para relações de profundidade máxima do cômodo para ventilação de um lado só.

## 3. Parâmetros urbanísticos (recuos, TO, CA, TP) e afastamento de divisa com aberturas

### Takeaway
A regra **federal** que vale em todo o país é o Código Civil, art. 1.301: nenhuma janela, eirado, terraço ou varanda a menos de **1,5 m** da divisa vizinha em área urbana. Para janelas cuja visão não incide sobre a divisa (perpendiculares), o mínimo é **0,75 m**. Na zona rural, edificações ficam a no mínimo **3 m** da divisa. Recuos, TO, CA e TP são **municipais** e variam por zona. Os valores confirmados nesta sessão (Curitiba e São Paulo) giram em torno de **recuo frontal 5 m, TO 50%, CA 1,0, TP 25%**.

### Cited Findings
**Código Civil, Lei 10.406/2002 [LEI FEDERAL]** — [Planalto, Código Civil compilado](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm)
- Art. 1.299: o proprietário pode construir o que quiser, salvo o direito dos vizinhos e os regulamentos administrativos.
- Art. 1.300: o prédio não pode despejar águas diretamente sobre o vizinho.
- **Art. 1.301:** "É defeso abrir janelas, ou fazer eirado, terraço ou varanda, a menos de metro e meio do terreno vizinho."
  - §1º: janelas cuja visão não incida sobre a linha divisória, e as perpendiculares, não podem ser abertas a menos de **75 cm**.
  - §2º: o artigo não abrange aberturas para luz ou ventilação de no máximo **10 cm × 20 cm** construídas a mais de **2 m de altura** de cada piso.
- Art. 1.302: o vizinho tem **ano e dia** após a conclusão da obra para exigir que se desfaça a janela irregular. O parágrafo único permite ao vizinho construir a qualquer tempo junto a aberturas de luz (seteiras etc.), mesmo vedando a claridade.
- **Art. 1.303:** na zona rural, nenhuma edificação a menos de **3 m** do terreno vizinho.

**Curitiba (PR) [LEI MUNICIPAL]**
- Lei 15.511/2019 (zoneamento): taxa de ocupação 50% e **taxa de permeabilidade mínima de 25%**, que pode ser complementada por mecanismos de contenção de cheias (o contexto exato da zona não foi lido). — [Lei 15.511, PDF via Migalhas](https://www.migalhas.com.br/arquivos/2020/7/29773EB9160F0E_PDF_Apresentacao.pdf)
- Consulta para fins de construção em **Zona Residencial 3 (ZR3)**: **CA 1,0; TO 50%; TP 25%; recuo frontal 5,00 m** (caso concreto, não a lei geral). — [Consulta amarela de imóvel em Curitiba (documento de leilão)](https://static.oleiloes.com.br/oleiloes/docs/1544786074.PDF)
- O Decreto 2.397/2024 exige recuo frontal mínimo de 5 m e permeabilidade mínima de 25% **no recuo frontal** no caso que trata. — [Prefeitura de Curitiba, Decreto 2.397/2024](https://mid.curitiba.pr.gov.br/2024/00427509.pdf)
- Quadro da Zona Central (2010): habitação unifamiliar com recuo de 5 m e permeabilidade de 25% (pode estar desatualizado). — [Prefeitura de Curitiba, 2010](https://mid.curitiba.pr.gov.br/2010/00084665.pdf)

**São Paulo (SP) [LEI MUNICIPAL]**
- Lei 16.402/2016 (LPUOS), Quadro 3: **ZER-1 (Zona Exclusivamente Residencial)** tem CA mínimo 0,05, CA básico e máximo **1**, **TO 0,50**, gabarito **10 m** e **recuo frontal 5 m**. A leitura das colunas do PDF é interpretação do resumo e deve ser conferida. O recuo frontal pode ser facultativo nos casos dos arts. 66/68. A taxa de permeabilidade fica no **Quadro 3A / Quota Ambiental**, e o valor para ZER-1 não foi confirmado. — [Prefeitura de SP, tutorial do zoneamento 2021](https://gestaourbana.prefeitura.sp.gov.br/wp-content/uploads/2021/08/tutorial-zoneamento-2021-com-link.pdf); [Câmara Municipal de SP, Quadro 3](https://saopaulo.sp.leg.br/antigo/wp-content/uploads/dce/zoneamento/redacaofinal/QUADRO_3_FINAL.pdf); [Lei 16.402/2016](https://www.saopaulo.sp.leg.br/iah/fulltext/leis/L16402.pdf)
- O Decreto 63.884/2024 regulamenta a lei com as revisões posteriores, então o Quadro de 2021 pode estar desatualizado. — [LegisWeb, Decreto 63.884/2024](https://www.legisweb.com.br/legislacao/?id=469189)

**Belo Horizonte (MG) [LEI MUNICIPAL]**
- Plano Diretor, Lei 11.181/2019 (em vigor desde 2020): a taxa de permeabilidade é "a % mínima da área do terreno a ser mantida descoberta". A área permeável natural e vegetada no afastamento frontal pode render benefícios urbanísticos. Os parâmetros de edificações horizontais estão na **Tabela 9 do Anexo XII**. O Decreto 19.151/2025 alterou o tratamento do afastamento frontal em certos casos. **Os valores numéricos não foram obtidos.** — [PBH, boletim de monitoramento](https://prefeitura.pbh.gov.br/sites/default/files/estrutura-de-governo/politica-urbana/2024/dmlu_monitoramento_gestaosustentavel_boletim2.pdf); [PBH, cartilha SMPU 2025](https://prefeitura.pbh.gov.br/sites/default/files/estrutura-de-governo/politica-urbana/2025/cartilharepresentacaopbh_smpu_r5.pdf); [LegisWeb, Decreto 19.151/2025](https://www.legisweb.com.br/legislacao/?id=480082)

**Florianópolis (SC)**
- O Plano Diretor é a LC 482/2014, e um novo Código de Edificações saiu em 2026 (LC 786/2026). **Os valores numéricos não foram obtidos.** — [LegJur, decisão do TJSC](https://www.legjur.com/jurisprudencia/eme/713.6438.9809.5439); [LegisWeb, LC 786/2026](https://www.legisweb.com.br/legislacao/?id=493065)

**Generalização [POPULAR]**
- "Geralmente, o recuo frontal é de 5 metros na maioria das zonas, com algumas exceções." — [Sienge, "Normas de recuo para construção civil"](https://sienge.com.br/blog/normas-de-recuo-para-construcao-civil/)

### Inferences
- **Default nacional sugerido** (configurável, rotulado como "valor típico, conferir a lei municipal"):
  - recuo frontal 5 m (há casos de 4 m e 3 m, ver Gaps);
  - afastamentos lateral e de fundos: **0 m sem aberturas** (encosta na divisa, se a lei municipal permitir) e **1,5 m com janela voltada para a divisa** (Código Civil, regra dura federal); 0,75 m para janela perpendicular;
  - TO 50%; CA 1,0; TP 25%.
- O art. 1.301 é a única regra **dura e nacional** do grupo e deve ser checada pelo motor geométrico: janela a menos de 1,5 m da divisa, apontada para ela, gera erro. A exceção é a abertura ≤ 10×20 cm acima de 2 m.
- TO e CA são verificáveis com a planta: TO = projeção da edificação / área do lote; CA = área construída computável / área do lote. A TP depende do paisagismo, e o gerador pode reservar área descoberta e permeável no recuo frontal ou no quintal.

### Gaps
- O objetivo pedia **4 municípios com números**. Só **Curitiba e São Paulo** têm valores confirmados (e parcialmente: SP sem TP). BH, Florianópolis, Porto Alegre e Goiânia ficaram sem números. Há links não lidos com quadros de Joinville ([Anexo VII](https://www.joinville.sc.gov.br/wp-content/uploads/2018/07/Proposta-de-Anexo-VII-Quadro-de-Ocupa%C3%A7%C3%A3o-%C3%A0-LC-n%C2%BA-470-2017-SEI-2039836.pdf)) e Ipatinga ([Anexo II](https://www.ipatinga.mg.gov.br/abrir_arquivo.aspx/PL_-_ANEXO_II?cdLocal=2&arquivo=%7B5DD3BABB-CCBA-DA8B-D1D3-A7DEC33CACCC%7D.pdf)) que poderiam completar a amostra.
- Os afastamentos laterais municipais (ex.: 1,5 m, ou H/6 em edifícios) não foram confirmados em nenhuma lei.
- A faixa "TP 15–30%" do enunciado não foi confirmada além dos 25% de Curitiba.

## 4. Zoneamento funcional (social / íntima / serviço) e adjacências

### Takeaway
A tripartição **social / íntima / serviço** é o modelo dominante da habitação brasileira. Cozinha e área de serviço ficam perto da entrada e longe dos dormitórios, e as áreas molhadas são agrupadas para economizar hidráulica. Há crítica acadêmica recente de que esse modelo não é neutro.

### Cited Findings
- A moradia brasileira se divide em três zonas: "social"/"estar", "íntima"/"repouso" e "serviços". A grande maioria das residências segue esse arranjo, e programas reduzidos precisam dar conta das três zonas. — [Principia/IFPB, artigo](https://periodicos.ifpb.edu.br/index.php/principia/article/download/127/102)
- O "modelo tripartido" atinge quase todos os imóveis residenciais em altura produzidos no Brasil nas últimas décadas, independentemente de localização, renda ou área. — [Ambiente Construído (SciELO), v.20 n.2](https://scielo.br/pdf/ac/v20n2/1678-8621-ac-20-02-0305.pdf)
- A configuração básica aproxima a porta da rua da cozinha e da área de serviço (áreas de trabalho e de maior ruído) e põe os dormitórios no extremo oposto. A cozinha e as demais áreas molhadas aparecem como elementos a agrupar (o trecho recuperado estava incompleto). — [Unisanta, hemeroteca](https://sites.unisanta.br/hemeroteca/arquivos/a743.pdf) (atribuição feita pelo resumo de busca, a confirmar)
- Crítica (2026): a setorização tripartida "não constitui convenção projetual neutra", pois reflete hierarquias de classe, gênero e raça herdadas da casa-grande. — [Revista Arquitetura e Lugar/UFCG](https://revistas.editora.ufcg.edu.br/index.php/arql/article/download/7255/5446/16693) (atribuição pelo resumo de busca, a confirmar)

### Inferences
Matriz de adjacência sugerida. São regras de **boa prática** derivadas das fontes acima e da lógica de zoneamento; os pesos são propostas do agente.

| Par | Relação | Motivo |
|---|---|---|
| Cozinha ↔ área de serviço | adjacente (forte) | zona de serviço, hidráulica compartilhada |
| Cozinha ↔ estar/jantar | adjacente ou integrada | fluxo de servir |
| Entrada ↔ estar | adjacente | acesso social |
| Entrada/garagem ↔ cozinha/serviço | próximo | compras, acesso de serviço |
| Banheiro ↔ dormitórios (circulação íntima) | próximo | zona íntima |
| Dormitórios ↔ cozinha/serviço/garagem | separar | ruído e odor |
| Dormitórios ↔ rua (fachada frontal) | evitar quando possível | privacidade e ruído |
| Áreas molhadas (banho, cozinha, serviço) | agrupar ("parede hidráulica") | custo de tubulação |
| Banheiro social ↔ estar | acessível sem passar por dormitório | privacidade |

### Gaps
- Não foi encontrada fonte primária com uma **matriz de adjacência formal** (organograma funcional quantificado) para o Brasil. A tabela acima é inferência. Neufert e livros-texto de projeto residencial não foram consultados.
- Não há evidência quantitativa sobre a economia de agrupar áreas molhadas.

## 5. Bem-estar e conforto: luz natural, ruído, privacidade, quintal

### Takeaway
A NBR 15575-1:2013 fixa um mínimo de **60 lux** de luz natural (nível Mínimo) em sala, dormitório, copa/cozinha e área de serviço, com 90 e 120 lux para os níveis Intermediário e Superior. A revisão passa para métricas de autonomia de luz diurna (sDA a 60 e 200 lux). A evidência específica sobre acústica entre dormitórios, privacidade e quintal ficou fraca nesta rodada.

### Cited Findings
- **NBR 15575-1:2013, iluminação natural [NORMA]:** iluminância mínima de **60 lux** no plano de trabalho (0,75 m) no centro do ambiente, em dia de nebulosidade média, para sala de estar, dormitório, copa/cozinha e área de serviço. Os níveis são **≥ 60 (M), ≥ 90 (I), ≥ 120 lux (S)**. — [UnB, artigo "Validação do desempenho lumínico"](https://repositorio.unb.br/bitstream/10482/50851/1/ARTIGO_ValidacaoDesempenhoLuminico.pdf); [ENTAC 2020, luz natural em dormitórios de conjunto habitacional](https://eventos.antac.org.br/index.php/entac/article/download/757/447/1581) (os valores vieram do resumo de busca, e a atribuição exata entre os dois artigos não foi checada)
- A revisão da seção 13 (citada como 15575-1:2024) propõe avaliar a **autonomia espacial de luz diurna (sDA)** para 60 lux e 200 lux e aumenta a exigência em relação ao limiar pontual de 60 lux. — [Ambiente Construído (SciELO), "Daylight challenges in Brazilian social housing: lessons from recent standards"](https://www.scielo.br/j/ac/a/MpgNc5LCbNK83ryQXtzBkTd/?lang=en) (a página deu erro 500 no fetch; informação do resumo de busca)
- Iluminação inadequada na habitação aparece associada a alterações no padrão de sono e no nível de alerta, em estudo da USP com foco na pandemia de COVID-19. — [Gestão & Tecnologia de Projetos (USP)](https://periodicos.usp.br/gestaodeprojetos/article/download/178708/176516/520332)
- Em habitação de interesse social, a iluminação natural afeta o conforto e a saúde dos usuários. — [PARC/Unicamp](https://periodicos.sbu.unicamp.br/ojs/index.php/parc/article/download/8661759/27271/107869)
- Pesquisa da UFSC (ENSUS 2025, 473 respostas) sobre o uso de venezianas em dormitórios e a percepção de conforto, o que indica a relevância de escurecer o quarto. — [ENSUS 2025/UFSC](https://conferencias.ufsc.br/index.php/ensus/ensus2025/paper/download/3001/1739)
- [POPULAR/divulgação] Trabalhadores com luz natural no escritório dormiriam cerca de 46 min a mais por noite. É divulgação jornalística sem o artigo original verificado. — [Correio Braziliense](https://www.correiobraziliense.com.br/cbradar/tenha-uma-noite-de-sono-profundo-e-reparador-mudando-so-isso-no-seu-dia-a-dia/)

### Inferences
- Default: todo APP (dormitório, estar) precisa de janela para o exterior. Cozinha e área de serviço também precisam de luz natural pela NBR 15575. Banheiros podem ter ventilação indireta ou mecânica, conforme o código de obras local (não verificado).
- Privacidade e ruído: as regras de adjacência da seção 4 (dormitórios longe da rua, da garagem e da zona de serviço; banheiro social sem passar por dormitório) são a forma mais simples de modelar acústica no 2D, sem cálculo acústico.

### Gaps
- **Desempenho acústico (NBR 15575-4/-3):** não foram obtidos valores de D2m,nT,w de fachada por classe de ruído nem de isolamento entre ambientes.
- **Áreas mínimas de janela dos códigos de obras** (ex.: 1/6 da área de piso para permanência prolongada e 1/8 para transitória) [NÃO VERIFICADO]: são frações comuns na memória do agente, mas não foram confirmadas em nenhum código nesta sessão.
- **Quintal/área verde e saúde:** nenhuma fonte encontrada. Faltam também evidências biofílicas quantitativas para o contexto residencial brasileiro.
- Não foi encontrada evidência específica sobre privacidade visual em relação à rua (ex.: peitoril, recuo, muro).
