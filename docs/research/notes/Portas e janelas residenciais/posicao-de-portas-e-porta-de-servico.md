# Posição de portas na planta e porta de serviço (trilha D3, notas de pesquisa)

> Data: 2026-11-22 · Escopo: Brasil para normas e prática; internacional só em fontes acadêmicas, computacionais e livros clássicos, rotuladas como tal.
> Rótulos: [N] ABNT · [L-fed] lei federal · [L-est] lei ou decreto estadual · [F] programa federal · [L-mun] código municipal · [A] acadêmico · [P] prática, blog ou manual · [X] inferência. Também se indica se a fonte é primária (texto da própria norma, lei ou artigo) ou secundária.
> Já coberto por outras notas e **não repetido aqui**: duas portas de acesso no MCMV, 1,20 m livre à frente das portas, aproximação de 0,60/0,30 m, 0,60 m ao lado da maçaneta (NBR 9050), círculo de 1,50 m entre portas em sequência, porta de correr no canto (Eclisse), zoneamento de Vespucci & Saboya 2020.
> Método: 21 consultas (buscas e leituras). Quatro PDFs foram baixados e lidos por extração de texto local: NBR 9077:2001 (cópia do MPRJ), Merrell et al. 2010, dissertação da PUC-Rio sobre banheiros para idosos, e a página do Decreto SP 12.342/1978 na ALESP (lida até o caractere 100.000 de 525.836).

## 1. Porta junto ao canto ou centrada, e a "boneca" (retorno de parede entre o batente e o canto)

### Takeaway
Nenhuma norma brasileira encontrada fixa uma boneca mínima nem manda pôr a porta no canto. A regra "porta junto ao canto" tem base sólida em fonte acadêmica e teórica internacional: Merrell et al. 2010 implementam a regra citando o padrão de Alexander et al. 1977. O único número normativo brasileiro próximo é o da NBR 9077, que admite até 75 mm de cada lado do vão para contramarco, marco e alizares. Esse valor serve como piso físico da boneca.

### Cited Findings
- [A, primária, internacional] Merrell, Schkufza & Koltun (2010, ACM TOG), seção 6, "Passageways": "It is customary to place passageways near room corners." O artigo cita Alexander et al. 1977: "When [a door] is in the middle of the wall, it almost always creates a pattern of movement which breaks the room in two, destroys the center, and leaves no single area which is large enough to use". A regra implementada coloca a porta "in a location that minimizes the sum of the distances from the door to the nearest corner in each of the adjacent rooms". — [Merrell et al. 2010, PDF Princeton](https://www.cs.princeton.edu/courses/archive/spring11/cos598A/pdfs/Merrell10a.pdf)
- [A, secundária via Merrell; teoria internacional] O trecho citado vem de *A Pattern Language* (Alexander et al., 1977). O texto original não foi lido nesta rodada. O número do padrão, que costuma ser citado como "Corner Doors", não foi conferido. — [Merrell et al. 2010](https://www.cs.princeton.edu/courses/archive/spring11/cos598A/pdfs/Merrell10a.pdf)
- [N, primária] NBR 9077:2001, item 4.5.4.2: nas portas de rotas de saída, admite-se "uma redução no vão de luz [...] das portas em até 75 mm de cada lado (golas), para o contramarco, marco e alizares". O mesmo item fixa a luz mínima de 80 cm para uma unidade de passagem. — [NBR 9077:2001, cópia MPRJ](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [L-mun, primária, Belo Horizonte, manual de obras SUDECAP cap. 12] O manual define o alizar como a peça que cobre a junta entre a parede e o marco, também chamada guarnição ou cobre-junta. Não trata de distância até o canto. Informação lida no resumo da busca; o PDF não foi aberto. — [SUDECAP cap. 12](https://prefeitura-ds.pbh.gov.br/sites/default/files/noticia/sudecap_capitulo_12.pdf)
- [P] Buscas por "boneca" com valores de 10 ou 15 cm só trouxeram anúncios de batedor de porta. No varejo, "boneca" também é o nome desse acessório de proteção da parede, e esse sentido polui a busca. — [Telhanorte, batedor de porta](https://www.telhanorte.com.br/batedor-de-porta-pvc-cinza-fixtil-931241/p)

### Inferences
- [X] Piso físico da boneca: largura do alizar mais a folga de montagem do marco. O valor de 75 mm de golas por lado da NBR 9077 indica a ordem de grandeza: a boneca precisa ter pelo menos cerca de 7,5 cm para o alizar não bater na parede ortogonal. Este é um limite construtivo, **não** uma boneca normativa. A NBR 9077 trata de saídas de emergência, e o item vale para portas de rotas de saída.
- [X] Para o gerador: a posição da porta pode ser um parâmetro contínuo ao longo da parede compartilhada. Um critério flexível (custo, não restrição dura) favorece a porta perto de um canto, como no custo "soma das distâncias ao canto mais próximo nos dois cômodos" de Merrell. A boneca mínima fica como restrição dura configurável, com valor sem fonte normativa: deixar o campo vazio, ou marcar como [X] até achar fonte. Isso converge com a observação do responsável de que a porta no canto encurta o corredor.
- [X] A regra de Merrell também protege a área útil do cômodo. A porta no canto libera a parede maior para cama ou armário, o que liga esta seção à seção 4.

### Gaps
- Não foi achado valor brasileiro (ABNT, código de obras, CDHU ou CAIXA) para a boneca mínima, nem apostila de desenho arquitetônico com número citável. Neufert e Panero & Zelnik não foram acessados nesta rodada; não há prévia online lida.
- Texto original de Alexander 1977 (número do padrão e redação completa) não conferido.

## 2. Sentido de abertura: contra a parede, para dentro do cômodo, porta de banheiro e interruptor

### Takeaway
Nas habitações, a regra de sentido de abertura é convenção de prática, não norma: abrir para dentro do cômodo, com a folha encostando na parede mais próxima. A exigência de "abrir para fora" aparece só em contextos específicos. Na NBR 9077 vale para portas de rotas de saída e salas com mais de 50 pessoas. Em sanitário acessível, a NBR 9050 é citada só por fontes secundárias. Para idosos, há uma recomendação acadêmica. O interruptor do lado da maçaneta, a 1,10–1,30 m, é prática de projeto elétrico citada por blogs e apostilas, não texto lido da NBR 5410.

### Cited Findings
- [N, primária] NBR 9077:2001, item 4.5.4.1: "As portas das rotas de saída e aquelas das salas com capacidade acima de 50 pessoas e em comunicação com os acessos e descargas devem abrir no sentido do trânsito de saída". — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [N, primária] A NBR 9077 inclui as casas unifamiliares no seu escopo: a Tabela 1 traz "A-1 Habitações unifamiliares — Casas térreas ou assobradadas, isoladas ou não" (item 1.3: "se aplica a todas as edificações, classificadas [...] na Tabela 1"). A A-1 é isenta de algumas exigências, como alarme e iluminação de emergência. — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [L-est, primária, SP] No Decreto SP 12.342/1978, as regras de abertura de porta para fora (art. 132, teatros) e de porta que impede a visão do interior (art. 183, III, sanitários industriais) **não se aplicam a habitações**. No trecho lido do capítulo de habitação, não há regra de sentido de abertura. — [Decreto 12.342/1978, ALESP](https://www.al.sp.gov.br/repositorio/legislacao/decreto/1978/decreto-12342-27.09.1978.html)
- [A, primária] Dissertação da PUC-Rio sobre banheiros residenciais para idosos (cap. 10, diretrizes propostas pela autora, não norma): "Porta de acesso ao banheiro deve ter largura mínima de 0,80m e altura mínima 2,10m e sua abertura deve ter a direção para fora". A Apreciação Ergonômica listou entre os problemas de maior gravidade "a direção de abertura da porta de acesso ao banheiro é para dentro". A autora recomenda maçaneta de alavanca entre 0,90 e 1,10 m. — [PUC-Rio, dissertação 0510330, cap. 10](https://www.maxwell.vrac.puc-rio.br/10697/10697_11.PDF)
- [P, secundária sobre a NBR 9050] Em banheiro acessível, a porta "deverá abrir para fora do banheiro, para que a pessoa consiga puxá-la tranquilamente para entrar". O texto da norma não foi lido. — [Sienge, acessibilidade em banheiros](https://sienge.com.br/blog/acessibilidade-em-banheiros-exigencias-solucoes/)
- [P] Segundo um portal de reforma, "em mais de 80% das residências brasileiras, as portas de banheiro abrem para dentro", com risco em emergências num banheiro de 3–4 m². A estatística não tem fonte e deve ser tratada como alegação. — [Lar Pontual, banheiro adaptado para idoso](https://larpontual.com.br/portal/web-stories/banheiro-adaptado-para-idoso)
- [P] Blog de acessibilidade: a porta do banheiro deve ter "no mínimo 80cm de largura e se possível abrir para fora". — [meutudo, banheiro adaptado](https://meutudo.com.br/blog/banheiro-adaptado-para-idoso/)
- [P] Interruptor de porta com eixo entre 1,10 e 1,30 m (um guia cita 1,15 m), "no lado da fechadura", a cerca de 10–15 cm do batente. Um erro comum é instalar a caixa atrás do raio de abertura da folha. Um portal cita 1,10–1,20 m para residências. A NBR 9050 pede 0,80–1,00 m em ambientes acessíveis. As fontes divergem entre si, e a NBR 5410 não foi lida. — [Lar Pontual, altura do interruptor](https://larpontual.com.br/portal/altura-do-interruptor); [Catraca Livre](https://catracalivre.com.br/noticias/a-que-altura-do-chao-sao-instalados-os-interruptores-de-luz-e-por-que-isso-e-importante/); [Apostila UFRJ, instalações elétricas residenciais parte 2](https://www.coe.ufrj.br/~kleber/INST_ELET_RES_PARTE_02.pdf)

### Inferences
- [X] Convenção recomendada para o gerador, como critério e não norma. A folha abre para dentro do cômodo de destino (quarto, banheiro, cozinha) e nunca para dentro do corredor (ver seção 3). A dobradiça fica do lado do canto mais próximo, de modo que a folha aberta encoste na boneca ou na parede ortogonal. A maçaneta fica do lado oposto, que é o lado livre por onde se entra, e o interruptor vai na parede desse lado, junto ao batente. Com isso, o interruptor fica alcançável sem contornar a folha, o que satisfaz "não bloquear o interruptor".
- [X] Com porta junto ao canto (seção 1), a escolha do lado da dobradiça é quase determinada: dobradiça no lado do canto. Isso reduz uma variável de decisão.
- [X] Banheiro: oferecer "abrir para fora" como opção (perfil idoso ou acessível) ou porta de correr, não como padrão obrigatório. Abrir para fora de um banheiro social leva a folha para o corredor, o que conflita com a regra de não invadir o corredor da seção 3. É um conflito real, que o gerador deve expor ao usuário.
- [X] A NBR 9077 inclui a A-1 no escopo, mas o item 4.5.4.1 só vale para "rotas de saída" e salas com mais de 50 pessoas. Numa casa unifamiliar, isso não obriga a porta de entrada a abrir para fora. A prática brasileira de porta de entrada abrindo para dentro não foi contestada por nenhuma fonte encontrada. Esta é uma leitura do texto; não foi encontrada interpretação oficial de Corpo de Bombeiros para A-1.

### Gaps
- Texto da NBR 9050:2020 sobre o sentido de abertura de sanitários não lido (fonte paga; só secundárias). Não confirmado se a exigência vale só para sanitário acessível ou também para o comum.
- Nenhum texto da NBR 5410 sobre posição de interruptor foi lido. A própria NBR 5410 provavelmente não fixa lado nem altura de interruptor (hipótese a confirmar).

## 3. Conflitos porta–porta: folhas que colidem, portas que abrem para o corredor, portas em sequência

### Takeaway
A única regra normativa numérica encontrada sobre portas que invadem circulação é da NBR 9077 e vale para rotas de saída. Uma porta que abre a 180° para dentro da rota não pode reduzir a largura efetiva a menos da metade, mantendo 1,10 m livre. Uma porta que abre a 90° deve ficar em recesso, sem reduzir a largura em mais de 0,10 m. Um corredor residencial de 0,90 m (mínimo do Decreto SP 12.342) não comporta folha aberta dentro dele sem perder a função. Daí a convenção de portas abrindo para dentro dos cômodos.

### Cited Findings
- [N, primária] NBR 9077:2001, item 4.4.3.2: "As portas que abrem para dentro de rotas de saída, em ângulo de 180°, em seu movimento de abrir, no sentido do trânsito de saída, não podem diminuir a largura efetiva destas em valor menor que a metade [...], sempre mantendo uma largura mínima livre de 1,10 m para as ocupações em geral". — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [N, primária] NBR 9077:2001, item 4.4.3.3: "As portas que abrem no sentido do trânsito de saída, para dentro de rotas de saída, em ângulo de 90°, devem ficar em recessos de paredes, de forma a não reduzir a largura efetiva em valor maior que 0,10 m". — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [L-est, primária, SP] Decreto SP 12.342/1978, art. 66: a largura do corredor interno da habitação "não poderá ser inferior a 0.90 m". — [Decreto 12.342/1978, ALESP](https://www.al.sp.gov.br/repositorio/legislacao/decreto/1978/decreto-12342-27.09.1978.html)
- [N, primária] NBR 9077:2001, item 4.5.4.5: portas que dividem corredores de rotas de saída têm exigências próprias. O texto das alíneas não foi conferido. — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [A, primária, internacional] O House-GAN++ inclui, entre os critérios de avaliação, uma checagem semântica de tipo de porta: "The front door should not be connecting two rooms nor an internal door should be connecting to the outside area". Há um critério separado de plausibilidade da posição da porta. Não há regra explícita de colisão de folhas. — [House-GAN++, suplemento CVPR 2021](https://openaccess.thecvf.com/content/CVPR2021/supplemental/Nauata_House-GAN_Generative_Adversarial_CVPR_2021_supplemental.pdf)

### Inferences
- [X] Restrições geométricas determinísticas para o gerador:
  - **(a)** O setor de giro de uma folha (quarto de círculo de raio igual à largura da folha) não pode se sobrepor ao setor de outra folha. Em portas vizinhas, duas folhas abertas a 90° colidem se os setores se intersectam. A solução é afastar as portas, inverter a dobradiça ou trocar uma delas por porta de correr.
  - **(b)** O setor de giro não entra no corredor. Se precisar entrar, o corredor tem de manter a largura livre mínima configurada fora do setor. Aqui a NBR 9077 é só referência por analogia, porque o corredor de uma casa A-1 não é formalmente uma rota de saída dimensionada por população.
  - **(c)** Portas em sequência (antecâmara, closet que leva ao banheiro): a regra do círculo de 1,50 m já coberta pela NBR 9050 vale como critério de acessibilidade.
- [X] A última porta no fim do corredor (observação do responsável: o último quarto pode abrir na cabeceira do corredor) é a configuração que naturalmente evita conflito. A folha abre para dentro do quarto, e o corredor termina na porta.

### Gaps
- Não foi achada regra brasileira residencial (código de obras, CDHU, CAIXA) sobre a distância mínima entre portas vizinhas no mesmo corredor ou sobre folhas que colidem. É tema de prática, sem número com fonte.

## 4. Conflito entre o giro da porta e o mobiliário (cama, armário, bancada, bacia sanitária)

### Takeaway
Não foi encontrada norma brasileira que trate do conflito entre giro de porta e mobiliário em habitação. O tema aparece de forma indireta. A NBR 9050 (já coberta) exige áreas livres de aproximação nas portas. A NBR 9077, item 4.7.3.4, exige patamar dos dois lados do vão, com comprimento igual à largura da folha, em escadas de emergência. Merrell et al. justificam a porta no canto pela área útil livre do cômodo.

### Cited Findings
- [N, primária] NBR 9077:2001, item 4.7.3.4 (escadas): "Em ambos os lados de vão da porta, deve haver patamares com comprimento mínimo igual à largura da folha da porta." — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [N, primária] NBR 9077:2001, item 4.6.2.5 (rampas): "Não é permitida a colocação de portas em rampas; estas devem estar situadas sempre em patamares planos, com largura não-inferior à da folha da porta de cada lado do vão." — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [A, primária, internacional] A porta no meio da parede "leaves no single area which is large enough to use" (Alexander 1977 via Merrell 2010). O argumento é de área útil para mobiliar. — [Merrell et al. 2010](https://www.cs.princeton.edu/courses/archive/spring11/cos598A/pdfs/Merrell10a.pdf)
- [A, primária] O "esforço para sentar-se e levantar-se da bacia" e a porta abrindo para dentro aparecem entre os problemas de maior gravidade em banheiros de idosos no Rio de Janeiro. A dissertação sugere espaço livre de 1,50 × 1,20 m mais 0,90 × 0,90 m para a bacia, como diretriz da autora. — [PUC-Rio, dissertação 0510330](https://www.maxwell.vrac.puc-rio.br/10697/10697_11.PDF)
- [P] Projeto elétrico: um erro comum é pôr o interruptor atrás do raio de abertura da folha. O setor de giro deve ficar livre também na parede. — [Lar Pontual](https://larpontual.com.br/portal/altura-do-interruptor)

### Inferences
- [X] O "setor de giro" deve ser um objeto do modelo, derivado da porta: um quarto de círculo de raio igual à largura da folha, do lado em que ela abre. A regra dura é que **nenhuma peça de mobiliário com altura acima do piso pode intersectar o setor de giro**. As áreas de uso já obtidas na M1.2, como frente de armário, lado de cama e frente de bacia, podem se sobrepor ao setor só se a sobreposição for tolerada por configuração. Exemplo: a frente de armário pode coincidir com o giro, já que não se usam os dois ao mesmo tempo. Isso é decisão de produto, não norma.
- [X] O patamar dos dois lados do vão, com comprimento igual à largura da folha (NBR 9077 4.7.3.4 e 4.6.2.5), dá um número com fonte para a regra "porta não abre direto sobre degrau, escada ou rampa". O texto normativo vale para escadas e rampas de emergência; para casas de dois pavimentos, usar como critério por analogia.
- [X] Casos típicos a testar no gerador:
  - porta de quarto cujo giro bate na cama, o que pede trocar o lado da dobradiça ou mover a porta para o canto oposto;
  - porta de banheiro cujo giro bate na bacia (abrir para fora ou porta de correr);
  - porta de cozinha cujo giro invade a bancada ou a geladeira.

### Gaps
- Neufert e Panero & Zelnik têm figuras de folga entre porta e mobiliário, mas não foram acessados online nesta rodada. Nenhum número dessas obras foi registrado.
- Não foi achado manual CDHU ou CAIXA com regra explícita de giro de porta versus mobiliário.

## 5. Adjacências proibidas via porta (banheiro abrindo para cozinha, copa, sala)

### Takeaway
Foi achada **uma regra estadual primária**: o Decreto SP 12.342/1978, art. 61, diz que a cozinha não se comunica diretamente com dormitórios nem com compartimentos com bacia sanitária. O mesmo decreto, no art. 62, faz da copa, quando existe, passagem obrigatória entre a cozinha e os demais cômodos. Em âmbito federal, a NR-24 proíbe que sanitários de **locais de trabalho** se comuniquem diretamente com locais de refeição, mas não se aplica a habitações. A restrição "banheiro social não abre para sala, cozinha ou copa" encontrada numa dissertação da PUC-Rio é **diretriz proposta pela autora**, não texto do Código de Edificações do Rio. Um resumo de busca a atribuía ao código, e a leitura do PDF desfez o erro.

### Cited Findings
- [L-est, primária, SP] Decreto SP 12.342/1978 (Regulamento da promoção, preservação e recuperação da saúde), art. 61: as cozinhas "não se comunicarão d[i]retamente com dormitórios ou compartimentos providos de bacia sanitárias". O artigo também exige ventilação permanente. — [Decreto 12.342/1978, ALESP](https://www.al.sp.gov.br/repositorio/legislacao/decreto/1978/decreto-12342-27.09.1978.html)
- [L-est, primária, SP] Decreto SP 12.342/1978, art. 62: a copa, quando existir, "deverá ser passagem obrigatória entre a cozinha e os demais cômodos da habitação". — [Decreto 12.342/1978, ALESP](https://www.al.sp.gov.br/repositorio/legislacao/decreto/1978/decreto-12342-27.09.1978.html)
- [L-est, primária, SP] Decreto SP 12.342/1978, art. 64: cada habitação deve ter pelo menos um compartimento com bacia sanitária, lavatório e chuveiro. O art. 36, IX, a fixa 1,20 m² e dimensão mínima de 1,00 m para compartimento só com bacia, quando a norma específica for omissa. — [Decreto 12.342/1978, ALESP](https://www.al.sp.gov.br/repositorio/legislacao/decreto/1978/decreto-12342-27.09.1978.html)
- [L-fed, primária, não residencial] Redação antiga da NR-24 (item 24.1.25.1): os sanitários "não poderão se comunicar diretamente com os locais de trabalho nem com os locais destinados às refeições". A NR-24 atualizada (Portaria SEPRT 1.066/2019) reorganizou o texto, e não se confirmou redação equivalente. Âmbito: locais de trabalho. — [NR-24, eDisciplinas USP](https://edisciplinas.usp.br/pluginfile.php/5564885/mod_resource/content/1/NR%2024.pdf); [NR-24 atualizada, gov.br](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/arquivos/normas-regulamentadoras/nr-24-atualizada-2022.pdf)
- [A, primária; diretriz, não norma] Dissertação da PUC-Rio, cap. 10, "Sugestão de diretrizes", lida no PDF: "O banheiro comum aos moradores deve localizar-se na área central da residência e ter acesso pelo corredor ou circulação, sem no entanto, comunicar-se diretamente com a sala, cozinha ou copa." A diretriz aparece em lista proposta pela autora para eventual incorporação ao código carioca, não como transcrição do código. — [PUC-Rio, dissertação 0510330, cap. 10](https://www.maxwell.vrac.puc-rio.br/10697/10697_11.PDF)
- [Internacional, contexto] Em Portugal, o RGEU, art. 86.º, diz que as retretes "não devem normalmente ter comunicação direta" com os compartimentos de habitação. Isso mostra que a regra existe em códigos de matriz parecida, mas **não** vale no Brasil. — informação vinda de resumo de busca; texto do RGEU não lido.

### Inferences
- [X] A regra paulista do art. 61 é a base mais forte para uma restrição "banheiro ↔ cozinha sem porta direta". Pela regra do projeto (lei municipal ou estadual nunca vira padrão nacional), ela entra como **regra regional opcional (SP)** ou como critério de boa prática ligado por padrão e desligável, e não como restrição nacional dura.
- [X] O art. 61 também proíbe cozinha ↔ dormitório direto em SP. Isso é coerente com a hierarquia do responsável, em que os quartos são acessados pelo corredor. Também limita a "cozinha como ponte": a cozinha pode ligar sala e área de serviço, mas não pode abrir direto para um quarto.
- [X] O art. 62 (copa como passagem obrigatória entre a cozinha e o resto) reflete o programa de 1978. Hoje, com a copa raramente existindo como cômodo separado, só vale quando o usuário pede copa.
- [X] Na hierarquia do responsável, o banheiro social abre para o corredor e a suíte abre para o quarto, o que já evita na prática a porta de banheiro para sala ou cozinha. O lavabo é o caso de borda: em geral abre para a sala ou para o hall social. Não foi achada norma brasileira que proíba lavabo abrindo para sala ou estar; o art. 61 de SP proíbe só para cozinha.

### Gaps
- A vigência atual do capítulo de habitação do Decreto SP 12.342/1978 não foi confirmada. A Lei SP 10.083/1998 (Código Sanitário Estadual) e decretos posteriores podem ter revogado ou mantido o texto, e é comum municípios paulistas remeterem a ele.
- O texto do Código de Obras do Rio (Decreto 7.336/1988 ou o COES, LC 198/2019) e o do Código de Obras de São Paulo (Lei 16.642/2017) não foram lidos para esta regra.
- Não foram lidos manuais CDHU, CAIXA ou SEHAB com regra de adjacência via porta.

## 6. Segunda porta externa (porta de serviço): exigência e prática

### Takeaway
Além do MCMV (já coberto: duas portas de acesso, uma na sala e uma de serviço), não foi achada exigência de código de obras, sanitária ou de bombeiros que obrigue uma segunda porta externa em casa unifamiliar. A NBR 9077 inclui a A-1 no escopo, mas a isenta de vários dispositivos, e o texto lido não exige duas saídas para A-1. O mercado trata a porta de serviço como produto próprio (porta de serviço com veneziana ou grade) para cozinha ou área de serviço.

### Cited Findings
- [N, primária] A NBR 9077:2001 classifica "A-1 Habitações unifamiliares — Casas térreas ou assobradadas, isoladas ou não" e as isenta de exigências como alarme ("exceto casas unifamiliares (A-1)") e iluminação de emergência ("exceto no caso de ocupações A-1"). No trecho extraído, nada exige duas saídas para A-1. — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [N, primária] NBR 9077:2001, item 4.5.4.8: fechaduras em portas de acesso são permitidas "desde que seja possível a abertura pelo lado interno, sem necessidade de chave". O item vale para portas de acesso e descarga das rotas de saída. — [NBR 9077:2001](https://www.mprj.mp.br/documents/20184/74453/nbr_9077_saidas_de_emergencia_em_edificios_2001.pdf)
- [A, primária, internacional] Merrell et al. 2010, custo de acessibilidade: "the entrance, patios, and garage must have access to the outside". O custo conta conexões faltantes e entradas, pátios e garagens enclausurados. A garagem com acesso ao exterior é regra explícita do gerador. — [Merrell et al. 2010](https://www.cs.princeton.edu/courses/archive/spring11/cos598A/pdfs/Merrell10a.pdf)
- [A, primária, internacional] Em Merrell, "In the entrance room, the central window is replaced by the front door". A porta de entrada substitui a janela central do cômodo de entrada, ou seja, aqui a porta externa é centrada. Isso contrasta com as portas internas, que vão no canto. — [Merrell et al. 2010](https://www.cs.princeton.edu/courses/archive/spring11/cos598A/pdfs/Merrell10a.pdf)
- [P] Fabricantes e varejo vendem "porta de serviço" (veneziana, postigo com grade) indicada para "áreas de serviço, cozinhas ou outros ambientes que necessitem de uma solução funcional que combine segurança e a possibilidade de entrada de luz natural". — [Telhanorte, porta postigo com grade](https://www.telhanorte.com.br/porta-postigo-e-alumifort-216x88x5-4cm-com-grade-acetinada-sasazaki-724971/p); [Telhanorte, porta veneziana Pratika](https://www.telhanorte.com.br/porta-veneziana-direita-pratika-217x87cm-branca-sasazaki-1119362/p)
- [P] Conteúdo de construção recomenda a lavanderia perto da cozinha e um desnível na área de serviço para a água não se espalhar pela casa. — [NSC Total, área de serviço](https://www.nsctotal.com.br/noticias/veja-como-tornar-a-area-de-servico-mais-pratica-e-funcional)

### Inferences
- [X] Fora do MCMV, a segunda porta externa é **opção de programa**, não exigência legal. A regra do responsável ("em casas maiores, porta de serviço pela cozinha ou lavanderia") fica como critério de prática, ligado por tamanho ou por escolha do usuário, e obrigatório só se o perfil MCMV estiver ativo.
- [X] Para o gerador: a porta de serviço pertence à zona de serviço (cozinha ou área de serviço) e dá para o quintal ou o recuo lateral ou de fundo. A garagem coberta, quando existir, precisa de acesso ao exterior (Merrell). O acesso garagem → casa, direto pela cozinha, pela área de serviço ou pelo hall, é escolha de projeto, sem fonte normativa brasileira encontrada.
- [X] O contraste em Merrell (porta externa centrada no cômodo de entrada, internas no canto) sugere tratar a posição da porta de entrada por critério próprio, com composição de fachada, separado da regra de canto das portas internas.

### Gaps
- Não foram lidos manuais CDHU (tipologias) nem especificações CAIXA além do que já está coberto, nem códigos municipais sobre a segunda porta. Nenhuma regra municipal foi encontrada nesta rodada.
- Não foram encontrados artigos de segurança patrimonial com dados (não apenas opinião) sobre a porta de serviço como ponto vulnerável.

## 7. Referência computacional: posicionamento automático de portas em geração de plantas

### Takeaway
A literatura computacional trata a porta de três formas:
- **Regra pós-layout:** em Merrell 2010, a porta entra onde há parede compartilhada suficiente, junto ao canto, com tipo de passagem por classe de cômodo.
- **Aresta do grafo de entrada:** no House-GAN++ 2021, a porta interna liga dois cômodos e a porta de entrada liga um cômodo ao "exterior", com máscara de segmentação própria para cada porta.
- **Inferência a partir de mapas de calor ajustados à parede:** é o caso do GFLAN 2025.

Nenhum desses trabalhos traz regras de colisão de folha ou de giro versus mobiliário; esse espaço fica para o motor determinístico do projeto.

### Cited Findings
- [A, primária] Merrell et al. 2010: no programa arquitetônico, cada adjacência é "open-wall or mediated by a door". A rede bayesiana aprende, por exemplo, que "a door (rather than an open wall) between the rooms is more likely given a square footage that is larger still" (relação sala–cozinha). Custo de acessibilidade: "For a connection between two rooms to be possible, they must share a sufficiently long wall segment to accommodate a door." — [Merrell et al. 2010](https://www.cs.princeton.edu/courses/archive/spring11/cos598A/pdfs/Merrell10a.pdf)
- [A, primária] Merrell et al. 2010, tipos de passagem por privacidade: "Ordinary doors are placed in private rooms such as bedrooms. French doors with windows are placed in semi-private rooms such as studies or patios. Wide passageways are placed between public rooms." O artigo também aplica o "privacy gradient": áreas comuns perto da entrada, quartos longe. — [Merrell et al. 2010](https://www.cs.princeton.edu/courses/archive/spring11/cos598A/pdfs/Merrell10a.pdf)
- [A, primária] House-GAN++ (Nauata et al., CVPR 2021): no grafo, a aresta passa a codificar conexão funcional, não adjacência. "An 'interior door' is a connection between two rooms, and a 'front door' is a connection between a room and the outside area". A saída é "a segmentation mask for each room and door". — [House-GAN++, arXiv 2103.02574](https://arxiv.org/pdf/2103.02574); [suplemento CVPR](https://openaccess.thecvf.com/content/CVPR2021/supplemental/Nauata_House-GAN_Generative_Adversarial_CVPR_2021_supplemental.pdf)
- [A, primária] No House-GAN original, as arestas codificavam adjacência espacial; o House-GAN++ mudou para conexão por porta. — [House-GAN++, ar5iv](https://ar5iv.labs.arxiv.org/html/2103.02574)
- [A, secundária, só resumo de busca] GFLAN (arXiv 2512.16275) infere a posição de portas e janelas ajustando picos de mapas de calor à parede mais próxima. Nele, dois cômodos só contam como conectados se houver abertura de porta na parede compartilhada. — [GFLAN, arXiv](https://arxiv.org/pdf/2512.16275)
- [A, secundária, só resumo de busca] Um artigo do eCAADe 2025 aumenta o dataset com parede externa e porta de entrada antes de alimentar dois modelos GNN, o que mostra a porta de entrada como entrada condicionante. — [eCAADe 2025, artigo 272](https://conf.dap.tuwien.ac.at/preprints/ecaade2025/ecaade2025_272.pdf)

### Inferences
- [X] O modelo do House-GAN++ (porta como aresta do grafo de conectividade, com o "exterior" como nó) é compatível com a separação do projeto: a IA ou o usuário define o grafo de portas, e a geometria posiciona cada porta de forma determinística. A escolha "banheiro abre para o quarto (suíte) ou para o corredor (social)" é uma escolha de aresta nesse grafo, como observou o responsável.
- [X] A regra de Merrell (parede compartilhada suficiente + mínima distância ao canto) é diretamente implementável. O comprimento mínimo da parede compartilhada é a largura do vão mais as duas bonecas, e a boneca continua sem valor com fonte (seção 1).

### Gaps
- Os PDFs do GFLAN e do eCAADe 2025 não foram lidos por inteiro; os detalhes vêm de resumos de busca.
- Não foram pesquisados nesta rodada Graph2Plan (Hu et al. 2020), que recebe a porta de entrada como dado, nem trabalhos de CP-SAT ou programação inteira com variáveis de porta.
