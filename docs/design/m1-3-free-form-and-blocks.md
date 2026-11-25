# M1.3 — Forma livre, blocos destacados e edícula

Versão: 1.0 · Criado em: 2026-11-24 · Status: **design aprovado pelo responsável (S09, DEC-0152 a DEC-0160)**; implementação por etapas depois da calibração 2 do M1.1
Base: DEC-0145 (pedido), DEC-0144, DEC-0146 a DEC-0148 (conferência da S08), DEC-0108 (norma é referência, não teto), DEC-0059 (implantação), DEC-0019 a DEC-0021 (retrocesso) no [DECISOES.md](../../DECISOES.md); [mvp.md](mvp.md), seções 6, 8, 9 e 20 a 23; [m1-2-furniture-sizing.md](m1-2-furniture-sizing.md); [teoria do gerador](../theory/cpsat-generator.md).
Desenhos: [mockups/m1-3-form-families.html](mockups/m1-3-form-families.html).
Sem plano de implementação: ele vem depois da calibração 2 do M1.1.

Marcas usadas: **[R]** decisão do responsável; **[A]** proposta do agente aprovada na conversa; **[X]** número ou regra do agente sem fonte, configurável; **[construtor]** fica para quem implementar. O que não tem marca é fato do código ou dos documentos.

---

## 1. Intenção e o porquê

Na conferência da S08, as 4 alternativas da casa grande repetiam o mesmo retângulo na frente do lote, ocupavam uma fração pequena dele e deixavam cômodos sem parede externa. O responsável quer que a forma e a implantação variem entre as alternativas e que a planta possa ter mais de um bloco.

**O porquê [R]:** mais cômodos com janela, para dispensar duto e claraboia, e um lote mais bem usado. Numa casa média ou grande, o que se quer ganhar com o terreno que sobra é **área externa**: quintal, lazer, oficina, hobbies, esporte, academia, céu aberto.

**O que se mediu nas 16 plantas da conferência** (contando como "sem fachada" o cômodo inteiramente no interior da caixa da casa):

- 7 das 16 têm, fora a circulação, algum cômodo sem fachada: 4 de 4 na casa grande, 2 no programa básico, 1 nos 3 quartos, 0 no lote pequeno. A circulação não conta, porque nenhum tipo exige janela nela;
- na casa grande, a casa tem 11,4 a 11,8 m de largura numa faixa edificável de 12 m, por 9,5 a 10,4 m de profundidade, numa área de 22 m. São **três cômodos de espessura** nos dois sentidos: os do meio ficam sem janela;
- ela ocupa 24 a 27 % do lote, porque as áreas pedidas somam pouco perto de 450 m².

**O que os esquemas mostram** (os mesmos 12 cômodos, desenhados à mão pelo agente, exceto o 1º, que é saída real):

| Forma | Parede externa | Cômodos sem fachada, fora a circulação |
|---|---|---|
| Largo (alt-1 da conferência) | 42 m | 2 banheiros |
| Comprido | 45 m (+7 %) | nenhum |
| L | 50 m (+18 %) | nenhum |
| U com pátio | 67 m (+60 %) | nenhum |
| Casa + bloco com cômodos já pedidos | 60 m (+42 %) | nenhum |

A conclusão é que o perímetro não é o objetivo: **7 % a mais bastam no esquema comprido**, e o U custa 60 %. Os esquemas são ilustração, não prova de que o gerador os alcança. O da última linha separa o escritório, o que a regra 4.1 depois proibiu, e vale só como desenho.

**Cuidado:** ser comprido não basta. Três plantas da conferência (a alt-2 dos 3 quartos e as alt-3 e alt-4 do programa básico) são mais profundas que largas e têm banheiro sem janela. Quem garante a janela é a regra da janela (7.2), não a proporção.

## 2. Objetivos, não-objetivos e anti-objetivos

### Objetivos
1. As 4 alternativas mostram **ideias diferentes de casa**: uma por família de forma, quando o lote permite.
2. Os cômodos que pedem janela têm fachada real, sem duto nem claraboia, sempre que o programa e o lote permitirem, em **todas** as alternativas (7.2).
3. O usuário pede blocos (edícula, oficina, rancho), áreas com medida (piscina, quadra, horta) e quintal mínimo, com relações entre eles ("oficina perto da piscina").
4. A planta guarda blocos, áreas e caminhos, sem quebrar as plantas e os pedidos atuais e sem impedir o 3D.
5. A nota compara formas pelo que elas entregam, e não pela compacidade.
6. Não passar do tempo de hoje para 4 alternativas (linha de base medida logo antes da E1, depois do M1.2).

### Não-objetivos
- Chegar à meta de ~20 s (design 8). Nenhuma das abordagens consideradas promete isso.
- Pátio fechado dos quatro lados (forma em O). O MCMV proíbe sala e dormitório ventilando por poço, e o tipo `patio` pedido já existe.
- Casa girada em relação à frente (paredes não paralelas), cômodos em L, lote não retangular, mais de um pavimento.
- Portão, carro na rua, calçada pública, paisagismo e relevo.
- Escolher a família antes de gerar e "quero mais como esta": ficam para o M2.
- Portas e janelas (M4). O M1.3 só garante fachada e passagem possível, como o M1.

### Anti-objetivos (fracasso mesmo funcionando)
- **Quatro vezes a mesma forma.** É o problema que originou o marco.
- **Cômodo inventado sem o usuário saber.** Só com o modo surpresa ligado, e sempre marcado.
- **Bloco pedido que some em silêncio.** Se não couber, o app diz por quê.
- **Perímetro por perímetro.** Recorte sem utilidade, que encarece a obra.
- **Medida inventada** de piscina, quadra ou oficina.
- **Aumentar a casa além dos m² pedidos** só para encher o lote.

## 3. Restrições

- O M1.2 e a calibração 2 mexem no `cpsat.py`. Nenhuma etapa do M1.3 corre junto com elas.
- Reprodutibilidade: o contrato da seção 22.5 do mvp.md continua (mesmo pedido, semente e orçamento dão as mesmas plantas).
- Hoje cada alternativa da casa grande leva ≈ 38 s (151 s para 4, DEC-0149).
- **Calibração 2 (em andamento quando este documento foi escrito).** O plano dela, ainda sem o ok do responsável, já inclui a fachada só a 1,50 m da divisa (a rua conta), as janelas como restrição antes de relaxar, o banheiro social, a entrada e o corredor sem sobra. O M1.3 **usa** o que ela entregar e não repete. Antes da E1, conferir o que foi de fato entregue e ajustar as seções 7, 9 e 10.
- `src/`, `tests/`, `data/` e `mvp.md` não mudam com este documento. A seção 14 lista o que muda depois.

## 4. O que é pedido e o que é proposto

### 4.1 As três origens de um bloco ou cômodo [R]

| Origem | Quando | Regra |
|---|---|---|
| **Pedido pelo usuário** | "quero uma edícula com passagem coberta até a casa e uma oficina perto da piscina" | as formas em que ele não cabe saem da lista; se não couber em nenhuma, saem as plantas **sem** ele, com o motivo em destaque [R: B1]. O mesmo vale para uma área pedida |
| **Separação do que foi pedido** | um cômodo já pedido e destacável sai da casa | no máximo 1 das 4 alternativas, sem cômodo novo |
| **Acréscimo do gerador** | só com o modo surpresa ligado pelo usuário, que sabe do risco | pode ser bloco ou cômodo interno (a despensa perto da cozinha); sai marcado como "sugerido"; desligado por padrão |

Com o modo surpresa desligado, sobra de lote vira só um **texto** no relatório: "cabe uma edícula de até X m² no fundo".

Se vários elementos pedidos não couberem juntos, a ordem de retirada é: áreas, depois blocos, sempre os últimos do pedido primeiro [X]. A planta sem um elemento pedido forma um grupo à parte na nota (7.3).

**Destacáveis por padrão [A]:** `lavanderia`, `deposito`, `area_gourmet` e `garagem`, com três limites:
- `deposito` e `area_gourmet` só saem se o usuário informou a área (o catálogo não tem medida deles);
- `garagem` só sai depois que a D4 disser a largura do acesso de carro;
- sai **um** cômodo por planta.

O `escritorio` **não** sai sozinho da casa [R]; só a pedido. Quarto, sala, cozinha e banheiro, só a pedido. O usuário muda isso por cômodo.

**O modo surpresa** (que cômodos, quantos, em que ponto do fluxo) tem brainstorming próprio antes da E5. Este documento fixa só o consentimento, a marcação e o grupo separado na nota.

### 4.2 Três tipos de elemento no lote [A]

| Tipo | Exemplos | Como entra |
|---|---|---|
| Bloco construído | casa, edícula, oficina, rancho, academia | tem cômodos e paredes; o gerador desenha por dentro |
| Área com medida | piscina, quadra, horta, deck | retângulo sem paredes, posicionado pelo gerador; o usuário dá a medida; medida pronta só quando houver fonte (D4) |
| Sobra com nome | quintal, jardim | o que fica livre; aceita um mínimo em m² |

Uma área gourmet ou varanda coberta é **cômodo externo** do catálogo, dentro de um bloco. Uma quadra coberta é um bloco.

### 4.3 Posição padrão dos anexos [R]

Edícula, oficina e rancho pedidos ficam **encostados no fundo, numa lateral ou no canto**, salvo menção específica.

- **Encostado** tem o mesmo sentido do encosto da casa hoje: a face externa da parede fica na divisa, com o eixo no primeiro múltiplo de 100 mm, e a parede do bloco faz o papel do muro naquele trecho.
- O lado encostado não tem janela (Código Civil, art. 1.301), e o bloco abre as janelas para o quintal.
- O encosto zera o recuo recomendado daquele lado por decisão do responsável; a planta leva o aviso "confira a lei do seu município".
- No fundo e nas laterais, o anexo não segue os recuos da casa: ou encosta, ou deixa pelo menos 0,90 m até a divisa [X]. O recuo frontal vale para todos os blocos.
- O bloco que o **gerador** formou com um cômodo destacado não encosta por padrão: fica perto da casa (4.4).

### 4.4 Ligação entre a casa e um bloco [R: opção B]

| Bloco | Ligação padrão |
|---|---|
| formado pelo gerador com cômodo de **uso diário** (`lavanderia`) | **passagem coberta curta** (até 3,0 m [X]); se não der, a lavanderia fica na casa |
| formado pelo gerador com os demais (`deposito`, `garagem`, `area_gourmet`) | caminho aberto |
| pedido pelo usuário (edícula, oficina, rancho) | caminho aberto, salvo `link: covered` |

Todo bloco tem um caminho, coberto ou não, até a casa ou até a frente do lote. O caminho que parte da casa sai de um **cômodo atravessável**, coberto ou não.

### 4.5 Modelos prontos [A]

Preenchem o pedido e são editáveis. As medidas dos cômodos vêm do catálogo; onde ele não tem (área gourmet, depósito, oficina), o modelo **pede a área** até a D4 trazer fonte.

| Modelo | Cômodos | Pede área? |
|---|---|---|
| Edícula de hóspedes | quarto, banheiro | não |
| Edícula completa | sala, cozinha, quarto, banheiro | não |
| Área de lazer | área gourmet, lavabo | sim |
| Rancho | área gourmet, depósito [X] | sim |
| Oficina | oficina | sim |

A edícula completa leva um aviso: em alguns municípios (Curitiba, Decreto 2.397/2023), a edícula não pode ser moradia independente.

### 4.6 Casa maior ou mais área externa [R]

Os m² pedidos são respeitados. A preferência `space_priority`, de −2 (casa maior) a +2 (mais área externa), com padrão **+1 [A]**, decide o resto:

| Valor | Cômodo sem área informada | Peso do critério `outdoor` [X, calibrar] |
|---|---|---|
| −2, −1 | alvo no fim da faixa de conforto | 0 |
| 0 | alvo atual (início da faixa) | 0,5 |
| +1 | alvo atual | 1,0 |
| +2 | alvo atual | 2,0 |

Área informada pelo usuário nunca muda.

## 5. Abordagens consideradas

| | 1. Solver único | **2. Implantação primeiro, planta depois (escolhida [R])** | 3. Casa montada por alas |
|---|---|---|---|
| Ideia | uma malha do lote inteiro decide tudo junto | um modelo pequeno posiciona envelopes; o solver atual desenha cada bloco; um ajuste fecha | cada ala é uma minicasa com malha própria, coladas depois |
| Forma | recortes livres | a família define a silhueta e o formato da malha | L e U naturais |
| Qualidade | vê tudo ao mesmo tempo | a casa não renegocia espaço depois de implantada | fixa quem mora em cada ala antes da planta |
| Tempo [hipótese] | tende a piorar | casa perto de hoje ou menos; bloco pequeno em segundos (4 cômodos: 1,8 s por 4 alternativas hoje) | o mais rápido |
| Código | reescreve o gerador | reaproveita | reescreve acesso e adjacência entre malhas |
| Pedido inviável | não diz qual parte falhou | diz qual elemento não coube | diz, mas pode ser culpa da divisão |

O responsável escolheu a 2 e pediu que ela incorpore o ponto forte da 1: **que o solver veja as escolhas futuras** (seção 6). A 3 fica como plano B para o U.

## 6. Algoritmo: implantação que enxerga a planta

```
pedido
  │
  ▼
0. CONTAS RÁPIDAS     por bloco e família, descarta o que não cabe
  ▼
1. IMPLANTAÇÃO        esquemas de envelopes no lote, comparados por uma previsão
  │  ▲
  │  └── volta com motivo (nº fixo de voltas)
  ▼
2. PLANTA DA CASA     solver atual, dentro do envelope, sabendo o que há em cada lado
  ▼
3. PLANTA DOS DEMAIS BLOCOS
  ▼
4. AJUSTE             implantação de novo, com as medidas reais e a topologia fixa
  ▼
validação e nota da planta inteira
```

### 6.1 Contas rápidas

Para cada bloco e família, sem solver:

1. **Área (descarta):** a soma dos mínimos (na regra atual: o maior entre o mínimo do tipo e 0,7 × o alvo) cabe no envelope máximo, descontado o vazio mínimo da família.
2. **Lados (descarta):** todo cômodo cabe em algum sentido. Depois do M1.2, com a escada de medidas.
3. **Fachada (só previsão):** soma das menores larguras de quem pede janela ÷ perímetro com janela possível. Não descarta, porque um cômodo pode tomar janela por um canto vazio com contato de só 0,90 m, ou através de um cômodo externo.

As duas primeiras são condições necessárias: reprovar é prova de inviabilidade. Passar não garante nada.

### 6.2 Implantação

Um modelo CP-SAT pequeno, na mesma grade de 100 mm e com a mesma configuração reprodutível da seção 22.5 do mvp.md.

- **Envelope da casa:** a silhueta da família, e não só a caixa. Largo e comprido são um retângulo; o L são dois e o U são três, com o vazio no lugar escolhido. A área externa pode ficar **dentro do vazio**. Os demais blocos são um retângulo.
- **Tamanho:** a área bruta do envelope da casa fica entre a soma dos alvos e 1,3 × ela [X, calibrar], mais o vazio da família. O objetivo tem um termo que puxa para o meio da faixa. Sem esse piso, todos os outros termos empurrariam para a menor casa possível.
- **Variáveis:** posição e tamanho dos envelopes; posição e giro de 90° das áreas com medida; caminhos de um trecho reto ou em L, com pelo menos 0,90 m de largura.
- **Restrições:** dentro do lote; recuos (casa) ou encosto (anexos, 4.3); nada se sobrepõe; pelo menos 0,90 m entre blocos, salvo os ligados por passagem coberta; caminho da casa ou da frente até cada bloco; quintal mínimo pedido.
- **Objetivo (a previsão):** tamanho da casa; relações entre blocos e áreas; sol da casa (lado norte livre); lados com janela possível e a conta de fachada; área externa aproveitável (7.3); caminhos curtos.
- **Saída:** um número fixo de esquemas por família, em ordem de previsão [construtor: número].

O que a implantação manda para a planta da casa é um **contrato**: caixa máxima, família, posição da âncora (frente e esquerda, centro ou direita), canto e tamanho mínimo do vazio quando algo foi posto nele, e o contexto de cada lado (6.3).

O quintal mínimo pedido é rígido até a negociação do M6, como os mínimos e os recuos (mvp.md 5.2).

**Na etapa E1 a implantação ainda não existe:** a casa continua na frente e centralizada, e as famílias variam só a forma. Essa implantação continua o padrão quando não há áreas nem blocos a acomodar.

### 6.3 A casa olha para fora

A planta da casa recebe, por lado (frente, fundo, esquerda, direita):
- **o que há ali:** divisa, bloco ou área, com a distância;
- **se o lado aceita janela:** 1,50 m livres até a divisa ou até outro bloco (seção 10). A frente sempre aceita.

Com isso, o objetivo da fase 1 ganha termos por lado, sobre o `on_side` que já existe: uma relação "perto" entre um cômodo e uma área ou bloco premia o cômodo no lado que olha para ela; "longe" premia o lado oposto. Se há um caminho saindo da casa, coberto ou não, um cômodo atravessável toca o lado de onde ele sai.

A calibração 2 planeja comparar cada planta com o espelho dela e ficar com a melhor. Com contexto diferente entre esquerda e direita, essa troca fica **proibida**, porque levaria a piscina para o outro lado.

Sem relação pedida, valem preferências fracas [X]: sala para piscina e jardim; cozinha para área gourmet e edícula; quarto longe da quadra. São critérios, com peso baixo.

### 6.4 Planta por bloco

Cada bloco é resolvido pelo gerador atual (malha, duas fases), com:
- **limites no lugar de medidas:** o envelope é um teto, e o bloco pode sair menor;
- a **família** (seção 7.1), que define os vazios e o formato da malha;
- a **entrada**: na casa, a frente (e as regras da DEC-0148); nos outros blocos, um cômodo atravessável no lado por onde chega o caminho. Num bloco **sem** cômodo atravessável (edícula de hóspedes), a entrada é direto no quarto; a exigência atual de um atravessável na entrada vale só para os blocos que têm algum;
- as regras de circulação, banheiro social e zoneamento **só na casa**. Nos anexos valem mínimos, acesso e janela.

### 6.5 Volta com motivo

Se um bloco for **provado** inviável, a implantação recebe uma restrição nova e tenta de novo, até um número fixo de voltas. A restrição proíbe aquela caixa e as menores que ela **com a mesma família e o mesmo contexto** (lados com janela, lado do caminho, vazio reservado). Sem o contexto, o corte eliminaria esquemas viáveis e daria um "não coube" falso.

Se estourar o orçamento sem prova, tenta o esquema seguinte, sem aprender nada. O motivo fica no formato do mvp.md 6.4 (etapa, elemento, tipo, valor, explicação) e vira a mensagem de "não coube".

### 6.6 Ajuste

Com as topologias e os tamanhos reais, a implantação roda uma última vez: ajusta caminhos e passagem coberta e amplia o quintal. O ajuste **não pode** reduzir para menos de 1,50 m um afastamento que contou como fachada, nem mudar o lado em que um vizinho estava.

A casa pode sair menor que o envelope, o que afasta os anexos. A passagem coberta automática (até 3,0 m) é conferida aqui: o bloco destacado pelo gerador se aproxima da casa; se ainda passar de 3,0 m, a alternativa é descartada. Os anexos pedidos continuam encostados, e a passagem coberta pedida pelo usuário tem o comprimento que der.

### 6.7 Sonda curta (condicional)

Uma busca curta da planta em 2 ou 3 esquemas antes do orçamento completo. Só entra se o spike mostrar ganho por um custo menor que uma alternativa.

### 6.8 Custo e reprodutibilidade

- As etapas rodam em ordem fixa, com orçamento em lotes, sementes derivadas da semente do pedido e número fixo de esquemas e voltas. Nenhum relógio.
- **Teto de resoluções da casa por rodada: 8** [X, calibrar na E0], contando famílias descartadas, voltas e vagas completadas. Ao atingir o teto, a rodada entrega o que tem e diz o motivo (DEC-0138).
- O custo da casa é o de hoje, vezes o número de resoluções dela. O dos anexos se soma, com a hipótese de segundos por bloco.
- Os esquemas de casa iguais entre si (mesma família, mesmo envelope) não se resolvem duas vezes.

**O que se perde em relação ao solver único:** a implantação decide com uma previsão e pode deixar passar uma combinação ótima.

## 7. Forma, diversidade e nota

### 7.1 Famílias

| Família | Como o solver a impõe | Malha (confirmar na E0) |
|---|---|---|
| Largo | sem vazio; largura ≥ 1,15 × profundidade [X] | 6 × 6 (hoje) |
| Comprido | sem vazio; profundidade ≥ 1,15 × largura [X] | 6 × 6 ou 4 × 8 |
| L | um vazio num canto, com cada lado ≥ 1,50 m e área ≥ 10 % da caixa [X] | até 8 × 6 |
| U | um vazio no meio de um lado, de preferência o do fundo, com os mesmos limites | até 8 × 8 |
| Casa + bloco | um destacável sai; a casa segue a família de maior nota entre as mantidas | a da casa |

- **Lotes estreitos.** Nos pedidos de até 12 m de frente, a casa só caberia larga com menos área do que hoje (a largura máxima nos eixos é de 8,8 m nos 3 quartos e 6,8 m no básico). Ali as famílias se reduzem, na prática, a comprido e L. É limite do lote, não defeito.
- **Quase quadrada.** Uma planta com proporção abaixo de 1,15 não é de nenhuma família; só aparece como reserva (7.2).
- **Malha.** Uma casa comprida tende a pedir mais faixas na profundidade. O esquema comprido do mockup não prova isso: três pares de linhas dele distam 0,40 m (menos que os 0,90 m da malha) e, juntando-os, ele fica em 4 × 6 e cabe na malha de hoje. O 4 × 8 é uma pergunta do spike S1. O U desenhado usa 9 faixas na profundidade e tem pares perto demais; é o candidato a não caber.
- **Casa + bloco** é a última da fila e só concorre se o pedido tiver um destacável (4.1) que não esteja num bloco pedido. Sem o escritório, o ganho costuma ser pequeno.

**Recorte útil ou inútil [A].** No lote pequeno, o responsável chamou o recorte de "área perdida"; na casa grande, pediu recortes. A regra que concilia as duas observações:
- **útil:** cada lado com pelo menos 1,50 m [X], e dá janela a um cômodo que a pede e não a tem por outro lado, ou contém uma área pedida (piscina, jardim, horta) ou parte do quintal pedido;
- **inútil:** qualquer outro. Continua possível, mas custa nota.

A varanda e a garagem são cômodos e ocupam células da malha; não são recorte. Um recorte entre três paredes mais fundo que largo leva o aviso `deep_recess` (seção 10).

### 7.2 Como saem as K alternativas

A ordem proposta na calibração 2 é mantida: **encosto por fora, janela no meio, forma por dentro** (não se encosta na divisa para ganhar janela). As famílias entram no nível de dentro:

```
para cada encosto (solta; esquerda; as duas; e o fundo)
  para cada nível de janela (todas; só as obrigatórias)
    para cada família (comprido, L, largo, U, casa + bloco): teto 1,5 ×; se nenhuma der planta, 2,0 ×
    se alguma família deu planta: para aqui
    senão, a reserva: a sequência de formas de hoje, com até 2 recortes livres
```

1. As contas rápidas descartam famílias.
2. **Janela antes de variedade [R: A1].** Se alguma família dá janela a todos os cômodos que a pedem, só entram as que também dão. O nível seguinte só é tentado se **nenhuma** conseguir, nem a reserva, e aí vale para todas. Com `window_rule = "relaxed"`, há só o nível relaxado.
3. Cada família mantida gera **uma** planta. Família que esgota o orçamento é pulada com o motivo, sem contar como prova.
4. Sai a família com nota mais de 0,10 [X, calibrar] abaixo da melhor. Uma família que sai não volta para completar vaga.
5. Vagas sobrando são completadas com outros arranjos internos das famílias mantidas, começando pela de maior nota.
6. Com mais famílias mantidas do que K, ficam as de maior nota. No empate, vale a ordem do laço: comprido e L são as preferidas do responsável.
7. As plantas aparecem pela nota, com o nome da família.

**Diversidade.** A regra atual vale entre **todas** as alternativas, inclusive de famílias diferentes: 15 % dos pares, espelho proibido, cômodos iguais intercambiáveis (DEC-0147). Assim, uma mesma topologia esticada não conta duas vezes. A distância usa só os cômodos da casa. Mudar só a posição da casa ou de um anexo no lote **não** é outra alternativa.

**Perdas são medidas, não prometidas.** A reserva mantém as formas de hoje, mas a janela em todas as alternativas e a diversidade entre famílias podem dar menos de K plantas num lote apertado. A E1 compara com a linha de base e explica cada perda. Os motivos de "menos de K" (DEC-0138) passam a valer também por família.

### 7.3 Nota

**O defeito de hoje.** Compacidade = área dos cômodos ÷ caixa envolvente, calculada sobre os esquemas:

| | Compacidade | Efeito com os pesos de hoje (soma 14,5) | Com os pesos propostos na calibração 2 (soma 21,5) |
|---|---|---|---|
| L | 0,75 | −0,052 | −0,035 |
| U | 0,58 | −0,09 | −0,06 |
| 2 de 9 cômodos que pedem janela sem fachada | 1,00 | −0,015 | −0,031 |

Nos dois casos, o L que dá janela a todos perde mais que a casa com dois banheiros no escuro.

**Mudanças:**

| Critério | Mudança |
|---|---|
| `compactness` → `form` | 1 − (área de recortes inúteis ÷ caixa envolvente), por bloco, ponderado pela área do bloco. Recorte útil e retângulo valem 1. Peso a recalibrar, porque o critério fica mais neutro |
| `outdoor` (novo) | área externa aproveitável ÷ **área do lote dentro do muro**. Aproveitável é o que pertence a um quadrado livre de pelo menos 2,0 m de lado [X]; áreas com medida contam. Assim uma casa mais compacta, ou sem tiras perdidas, vale mais. Peso por `space_priority` (4.6) |
| `relations` | "perto" entre cômodos do mesmo bloco continua sendo parede em comum; entre elementos de blocos diferentes ou áreas, 1 − distância ÷ 10 m [X], cortado em 0, com a distância entre os retângulos; "longe" como hoje |
| `relations` com cômodo destacado pelo gerador | "perto" vale **0**, como qualquer par não vizinho. Senão, separar a lavanderia daria nota de graça |
| `area_fit`, `ventilation` | sobre todos os blocos |
| circulação, zoneamento, alinhamento, molhadas, sol, e os critérios da calibração 2 (entrada, banheiro social) | só na casa |

O peso de `ventilation` é assunto da calibração 2; o M1.3 não mexe. O quintal mínimo pedido é restrição da implantação (6.2) e não entra na nota.

**Parede externa** aparece como informação ("45 m, +7 % sobre a mais compacta da rodada"), com peso zero por padrão. O usuário pode dar peso a ela.

**Comparabilidade [R].** A nota só ordena plantas com o **mesmo programa** (os mesmos cômodos e áreas, sem contar em que bloco ficaram). Formam grupos à parte, sem ordem contra as demais: plantas com acréscimos do modo surpresa e plantas sem um elemento pedido que não coube.

**Gabarito.** Os rankings da S08 (DEC-0148) continuam. Entra um teste de coerência a partir da preferência do responsável pelos esquemas 3 (L) e 2 (comprido): com tudo o mais igual, L e comprido não podem ter nota menor que o largo **só por causa da forma**. Os esquemas do mockup servem de plantas de teste do `form`; não precisam caber na malha.

### 7.4 Objetivo do solver

O solver segue aproximando a nota (mvp.md 5.6). Na fase 1, o custo do recorte (`VOID_FIXED`, `VOID_CELL`) some se ele tocar um cômodo que pede janela e não está em nenhum lado externo com janela possível (a mesma regra da nota), ou se contiver uma área reservada. Na fase 2, a "área vazia" descontada é a inútil [construtor: formulação].

## 8. Modelo de dados

### 8.1 Pedido

Campos novos, todos opcionais. Um pedido atual continua válido, com o mesmo significado.

```json
{
  "rooms":  [ {"id": "cozinha", "type": "cozinha"},
              {"id": "sala_ed", "type": "sala", "block": "edicula"},
              {"id": "q_ed", "type": "quarto", "block": "edicula"},
              {"id": "ofic", "type": "oficina", "block": "oficina", "target_area_m2": 14} ],
  "blocks": [ {"id": "edicula", "link": "covered", "attach": ["back"]},
              {"id": "oficina"} ],
  "areas":  [ {"id": "piscina", "type": "piscina", "w_mm": 3000, "d_mm": 6000},
              {"id": "quintal", "type": "quintal", "min_area_m2": 40} ],
  "relations": [ {"a": "oficina", "b": "piscina", "kind": "near", "intensity": 4} ],
  "forms": "auto",
  "space_priority": 1,
  "surprise": false
}
```

| Campo | Significado | Padrão |
|---|---|---|
| `rooms[].block` | bloco do cômodo | `"casa"` |
| `rooms[].detachable` | pode sair sozinho da casa | por tipo (4.1) |
| `blocks[].link` | `covered`, `open` ou `auto` | `auto` (4.4) |
| `blocks[].attach` | divisas onde encostar; lista vazia = solto, com os recuos da casa | ausente: o gerador escolhe fundo, lateral ou canto (4.3) |
| `areas[]` | com medida (`w_mm`, `d_mm`) ou com mínimo (`min_area_m2`), conforme o tipo | nenhuma |
| `forms` | `"auto"` ou lista de famílias aceitas | `"auto"` |
| `space_priority` | −2 a +2 | +1 |
| `surprise` | autoriza cômodos não pedidos | `false` |
| `site_rules` | passagem entre blocos, respiro de janela, profundidade de varanda, limite de ocupação | 900 mm, 1500 mm, 3000 mm, sem limite |

**Regras:**
- um bloco usado por um cômodo e ausente em `blocks` existe com os padrões;
- ids de cômodos, blocos e áreas são únicos no pedido inteiro, e `relations` aceita qualquer um deles; `"casa"` é reservado;
- uma área com medida sem `w_mm` e `d_mm`, ou um cômodo de anexo sem área-alvo, sem faixa de conforto e sem mínimo de área (oficina, depósito, área gourmet), dá erro que pede a medida. Nada é inventado;
- `blocks` sem cômodos dá erro.

### 8.2 Planta

```
Plan
├── site    Site + rules (os `site_rules` do pedido)
├── rooms   Room + block: str = "casa", origin: "requested" | "suggested"
├── blocks  Block: id, kind ("main" | "annex"), attached_sides
├── areas   SiteArea: id, type, rect
└── paths   Path: id, covered, rects, connects (bloco ou frente, bloco)
```

- `Block.attached_sides` e `Site.rules` ficam na planta porque os validadores e o `export-dxf` só veem o `Plan`. O `Site.attached_sides` atual continua valendo para a casa; o bloco principal não o repete.
- A checagem do quintal mínimo recebe o pedido, como `score_plan` já faz.
- As coordenadas continuam no lote. Paredes continuam derivadas dos cômodos, sem código por bloco.
- Quintal e jardim (sobra) **não** são guardados: derivam do que sobra. Só a área com medida tem retângulo.
- A família, o esquema de implantação e a parede externa são da `Alternative`, não da planta.
- Planta antiga sem os campos novos = um bloco `"casa"`. O `save_plan` grava os campos novos só quando existirem [construtor].

### 8.3 Catálogo (`data/`)

- Tipos de cômodo novos: `oficina`, `academia`. Sem mínimo enquanto não houver fonte.
- Campo novo `detachable` por tipo (4.1), com fonte `agente`. O `RoomType` recusa campos desconhecidos, então o modelo do catálogo muda junto.
- `garagem` não é `exterior` no catálogo, embora o mvp.md 20.1 a chame de externa construída. A divergência é anterior e fica para o responsável.
- Arquivo novo de **tipos de área** (piscina, quadra, horta, deck, quintal, jardim): categoria de cor, se é permeável (vazio até a D4) e se exige medida.
- Modelos prontos de bloco (4.5), só com tipos de cômodo.

### 8.4 3D futuro

O bloco é a unidade de telhado, de altura e de extrusão. O `floor` do cômodo já existe, e cada bloco poderá ter os seus pavimentos. O caminho coberto é um telhado sem paredes; piscina e quadra são faces no terreno. Nada no modelo supõe uma casa só.

## 9. Validação

| Checagem | Hoje | Com blocos |
|---|---|---|
| Sobreposição | entre cômodos | também entre blocos, áreas e caminhos; o caminho pode encostar num bloco e cruzar a borda do quintal |
| Vazio fechado | caixa da planta | por bloco |
| Acesso | da frente da planta inteira | casa: pela regra de entrada vigente; outros: do caminho, que chega à casa ou à frente. Bloco sem atravessável entra por um privativo. Lote encostado dos dois lados chega ao fundo **por dentro** da casa, por um cômodo atravessável: é válido |
| Recuo | todos os cômodos | casa; anexos, só o frontal (4.3) |
| Janela e divisa | aviso | por bloco; o lado encostado avisa uma vez por bloco, não por cômodo |
| Fachada | trecho sem vizinho | um cômodo **externo** (varanda, gourmet) não tapa a fachada do vizinho, se ele próprio tiver um lado para fora. **Defeito de hoje:** a varanda conta como vizinho e tira a janela de quem está atrás. O pátio fechado dos quatro lados **não** dá janela a sala nem a quarto (MCMV: poço) |
| Permeabilidade | lote − muro − cômodos | desconta também áreas não permeáveis e caminhos. Enquanto a D4 não der fonte, piscina, quadra, deck e caminho contam como não permeáveis (lado conservador) [X] |

Regras novas de aviso: `annex_setback` (encosto do anexo), `independent_dwelling` (edícula completa), `missing_requested` (elemento pedido que não coube, com o motivo), `deep_recess` (recorte entre três paredes mais fundo que largo), `occupancy` (só com limite informado), `porch_depth` (varanda com mais de 3,0 m na frente de uma janela obrigatória ou preferida).

## 10. Regras do lote e trilha D4

Vale a DEC-0108. Só são duras a geometria, a lei federal e o que o usuário informou.

| Assunto | O que existe | Comportamento no M1.3 | D4? |
|---|---|---|---|
| Janela a menos de 1,50 m da divisa | Código Civil, art. 1.301 [L-fed]; 0,75 m para janela perpendicular | regra da calibração 2: lado a menos de 1,50 m não conta como fachada; a rua conta. O M1.3 a estende aos anexos. `relaxed` relaxa a exigência da janela, **nunca** o que é fachada. Os 0,75 m ficam para o M4 | não |
| Recuos da casa | informados pelo usuário | rígidos até o M6 | valor padrão municipal |
| Encosto de edícula e oficina | decisão do responsável | 4.3, com aviso | **sim** |
| Distância entre blocos | Rio: 1,50 m em prismas e afastamentos de casa (L-mun; trecho de busca, artigo não localizado) | 0,90 m para passar [X]; vão menor que 1,50 m não conta como fachada [X] | **sim** |
| Largura de recorte e pátio aberto | BH: reentrância com profundidade ≤ largura (multifamiliar e não residencial); Rio: reentrância com mais de 1,50 m de profundidade é calculada como prisma (L-mun). Os círculos de BH são de fosso **fechado** e não servem aqui | menos de 1,50 m = inútil [X]; três paredes e mais fundo que largo = aviso | **sim**, para casa |
| Varanda na frente da janela | BH 3,0 m (multifamiliar); Recife 2,0 m e João Pessoa 2,5 m (secundárias) | não tapa; aviso acima de 3,0 m [X] | parcial |
| Taxa de ocupação | Curitiba e SP 50 % (L-mun) | informação; aviso só com limite do usuário | **o que conta** (beiral, piscina, passagem, varanda) |
| Permeabilidade | 25 % (`curitiba-15511-2019`) | aviso, com a conta da seção 9 | **o que cada piso conta** |
| Edícula completa | Curitiba: não é moradia independente (L-mun) | aviso | **sim** |
| Medidas de piscina, quadra, horta, deck, oficina, rancho, academia | a D1 procurou e não achou com fonte | o usuário informa | **sim** |
| Passagem coberta (largura, altura, distância) | nada | 0,90 m de largura [X]; até 3,0 m quando automática [X] | **sim** |
| Acesso de carro até uma garagem separada | nada | garagem não sai sozinha até haver fonte | **sim** |

**Trilha D4 (implantação e áreas externas) [R: aprovada]:** pesquisa só de documentos, no processo da DEC-0074, sobre as linhas marcadas. Não bloqueia o algoritmo; bloqueia as medidas prontas e os avisos com número. Regra 4 do `data/README.md`: municipal nunca vira padrão nacional.

## 11. Relatório, DXF e interface

- **Relatório:** nome da família, parede externa, ocupação e área externa aproveitável em cada cartão; áreas e caminhos no SVG; grupo separado para plantas com acréscimos, com os cômodos "sugeridos" marcados; texto da sugestão de bloco.
- **DXF:** layers novos para áreas e caminhos (nomes no padrão atual, `A-…`) [construtor]. As 4 cores continuam: piscina, quadra, deck e caminho são externa construída; horta, quintal e jardim, externa verde.
- **M2:** a família como rótulo e filtro; "quero mais como esta"; `space_priority` e `surprise` como controles. Este documento só garante os dados.

## 12. Etapas

| Etapa | Entrega, útil sozinha | Pronta quando |
|---|---|---|
| **E0. Spikes** | as medições da seção 13; código descartável | números para malha, famílias e tempo, com dados brutos em `docs/research/notes/` (DEC-0141), e as decisões que eles destravam registradas |
| **E1. Formas** | largo, comprido e L; seleção por família; `form`; varanda não tapa a fachada; parede externa informada | casa grande: 4 de 4 com janela em todos os cômodos que a pedem, e ≥ 2 famílias entre elas (meta 3, a rever com a E0); nos outros pedidos, toda perda de alternativa em relação à linha de base vem explicada; tempo de cada pedido ≤ o da linha de base |
| **E2. Terreno** | implantação, áreas com medida, quintal mínimo, `outdoor`, casa que olha para fora, permeabilidade | um pedido com piscina e quintal sai sem sobreposição, e "sala perto da piscina" muda a planta |
| **E3. Blocos pedidos** | edícula, oficina e rancho; validação e planta por bloco; caminhos; modelos; avisos | pedido de referência novo (casa + edícula + oficina + piscina) com acesso válido em todos os blocos |
| **E4. U e casa + bloco** | pátio aberto; destacáveis com passagem coberta | U na casa grande, ou a medição de que pede alas (abordagem 3) |
| **E5. Surpresas** | modo surpresa e sugestão escrita, depois de um brainstorming próprio | desligado: plantas idênticas às de antes; ligado: todo acréscimo marcado |

Cada etapa fecha com testes, `pyright`, revisão independente e conferência visual (CLAUDE.md). E1 a E3 cobrem o que o responsável pediu na conferência, menos o U, que é a E4. Em todas, um pedido sem campos novos continua válido.

### Ordem [R: aprovada]

```
calibração 2 ─► E0 ─► M1.2 ─► E1 ─► E2 ─► E3 ─► E4 ─► E5
                │                   └──► M2 (implementação), em paralelo com E3 em diante
                └─ em paralelo, só documentos: D4 e design do M2
```

- **M1.2 antes da E1:** os dois mexem no `cpsat.py`; a escada de medidas alimenta as contas rápidas; calibrar as formas antes obrigaria a recalibrar.
- **M2 depois da E2:** o modelo já tem famílias e áreas. E3 a E5 mexem no gerador; o M2, em servidor e tela. O design do M2 lê a seção 8 desde o começo.
- **Linha de base:** a bancada é medida logo antes da E1, já com o M1.2, e os spikes S1 e S2 se repetem ali, porque o M1.2 muda o modelo e os mínimos depois da E0.
- **Plano de implementação:** depois da calibração 2 e da E0, um plano por etapa (E1 primeiro).

### Testes

| O quê | Etapa |
|---|---|
| Famílias: silhueta, proporção e vazio de cada uma, conferidos na planta | E1 |
| `form`: recorte útil e inútil; L = retângulo na nota; esquemas do mockup como gabarito | E1 |
| Fachada: varanda não tapa; varanda cercada e pátio fechado não dão janela a sala e quarto | E1 |
| Janela antes de variedade: família com cômodo no escuro sai quando outra consegue; relaxa só se nenhuma consegue | E1 |
| Seleção: limiar de 0,10, desempate, vaga completada, reserva, teto de resoluções, mesma topologia esticada não repete | E1 |
| Reprodutibilidade nas duas execuções simultâneas, com famílias | E1, E2, E3 |
| Pedidos e plantas antigos lidos sem mudança | todas |
| Implantação: áreas e caminhos sem sobreposição, encosto, giro de 90°, quintal mínimo, motivo de "não coube" | E2, E3 |
| Contas rápidas 1 e 2: nunca reprovam um pedido que o solver resolve | E1, E2 |
| Elemento pedido que não cabe: formas saem; se nenhuma serve, plantas sem ele com `missing_requested` | E2, E3 |
| Corte da volta com motivo: nunca elimina um esquema de contexto diferente | E3 |
| Validação por bloco: acesso, vazio fechado, recuo de anexo, avisos novos | E3 |
| Modo surpresa desligado não muda nada | E5 |

## 13. Spikes da E0

Só depois do merge da calibração 2 e com a máquina livre (método de medição da DEC-0149). Pedidos: casa grande e 3 quartos; nota medida pelos critérios de então.

| Spike | Pergunta | Decide |
|---|---|---|
| S1 | comprido com malha 4 × 8 contra 6 × 6: tempo, nota, cômodos sem fachada | formato da malha por família |
| S2 | L com o canto vazio fixo contra 2 recortes livres: tempo e nota | se a silhueta reduz a busca |
| S3 | U em malha de até 8 × 8: viável em quanto tempo? | plano B (alas) na E4 |
| S4 | implantação com casa, 2 blocos e 2 áreas: tempo até o ótimo | se cabe em ~1 s por esquema |
| S5 | plantas da calibração 2: quantos cômodos ainda ficam sem fachada, e quantas formas diferentes aparecem? | o ganho real do M1.3 e a meta de famílias da E1 |
| S6 | sonda curta (2 lotes) prevê a nota final da alternativa? | seção 6.7 |

A meta de famílias também depende da A1: se só uma forma der janela a todos na casa grande, as quatro alternativas serão dela.

Se o S1 mostrar que o comprido passa do tempo de hoje, reduzimos a malha ou o número de famílias. Se o S5 mostrar que a calibração 2 resolveu quase todas as janelas, a E1 continua pela variedade, e os objetivos dela são revistos com o responsável.

## 14. O que muda depois no mvp.md e nos outros documentos

Nada disto foi aplicado. Entra quando a etapa correspondente for implementada.

| Onde | Mudança | Etapa |
|---|---|---|
| mvp.md 5.1 | alcançabilidade por bloco, com caminho externo | E3 |
| mvp.md 5.4 e 5.6 | `compactness` → `form`; critério `outdoor`; comparabilidade por programa | E1, E2 |
| mvp.md 6.1 | implantação como etapa própria entre 0 e 1 | E2 |
| mvp.md 6.2 | "o gerador do MVP produz bloco único" deixa de valer; encosto padrão dos anexos | E3 |
| mvp.md 8 | famílias, malha por família e fluxo da seção 6 daqui | E1, E2 |
| mvp.md 9 | uma planta por família; regra dos 15 % entre todas | E1 |
| mvp.md 10 | `Block`, `SiteArea`, `Path`, `Room.block`, `Room.origin` | E2, E3 |
| mvp.md 13 | layers de áreas e caminhos | E2 |
| mvp.md 16 | linha do M1.3 e a ordem M1.2 → M1.3 → M2 | com a aprovação deste documento, quando o mvp.md estiver livre |
| mvp.md 20.1 | itens 1 (bloco cheio), 2 (recortes), 4 (implantação), 7 e 8 (cores e permeabilidade) | E1, E2 |
| mvp.md 21.1 | malha 6 × 6 e até 2 recortes | E1 |
| mvp.md 22.2 | varanda não tapa; janela antes de variedade (a fachada a 1,50 m é da calibração 2) | E1 |
| mvp.md 22.3 | retângulo antes de recorte (DEC-0099, já substituída pela DEC-0145) vira seleção por família | E1 |
| cpsat-generator.md | seções 1.2, 3.4, 4.1, 5 e 7 | E1 em diante |
| m1-2-furniture-sizing.md | 7.3: escada usada nas contas rápidas | E1 |
| data/README.md, README.md | arquivos e trilha novos | conforme nascem |

## 15. Arquivos afetados (mapa) [construtor: detalhe]

| Arquivo | Mudança |
|---|---|
| `model/request.py`, `model/plan.py` | campos da seção 8 |
| `model/walls.py` | fachada ignora cômodo externo |
| `generators/cpsat.py` | família, malha por família, contexto externo, custo do recorte |
| `generators/` (módulo novo) | implantação e ajuste |
| `scoring/score.py`, `diversity.py` | `form`, `outdoor`, relações entre blocos e áreas, distância só com a casa |
| `model/catalog.py`, `model/site_defaults.py`, `__main__.py` | `detachable`, tipos de área, números [X] com fonte `agente`, saída da CLI |
| `validation/*.py` | seção 9 |
| `export/*.py` | seção 11 |
| `data/` | seção 8.3 |

## 16. O que fica a cargo do construtor

- Formulação CP-SAT da implantação, dos caminhos e da família; número de esquemas e de voltas.
- Formulação do recorte útil na fase 1.
- Algoritmo da área aproveitável e das contas rápidas, mantidas as propriedades descritas.
- Calibração dos pesos (`form`, `outdoor`, preferências fracas de 6.3) na bancada, respeitado o gabarito.
- Nomes de módulos, funções, layers e mensagens, no padrão atual.

## 17. Números e regras do agente a conferir

São [X], configuráveis ou calibráveis. O responsável viu na conversa as decisões da revisão; os valores abaixo podem mudar com a E0, a D4 ou a conferência visual.

1. 0,90 m entre blocos e de caminho; 1,50 m de respiro; 1,50 m de recorte mínimo; 3,0 m de varanda; 3,0 m de passagem automática; 0,90 m do anexo solto à divisa.
2. Proporção de 1,15 para largo e comprido; vazio do L e do U com pelo menos 10 % da caixa.
3. Envelope da casa entre 1,0 e 1,3 × a soma dos alvos.
4. Quadrado de 2,0 m para área aproveitável; 10 m de alcance para "perto" entre blocos.
5. Limiar de 0,10 para descartar uma família; teto de 8 resoluções da casa por rodada.
6. `space_priority` em +1 e os pesos da tabela 4.6.
7. Piscina, quadra, deck e caminho não permeáveis até a D4.
8. Ordem de retirada quando vários elementos pedidos não cabem (4.1).
9. Preferências fracas sem relação pedida (6.3); modelo do rancho (4.5); recuo frontal para todos os blocos.

## 18. Revisão independente

Feita sobre a versão 0.1, lendo o código e as 16 plantas congeladas, sem rodar o solver: 11 perguntas e 26 achados. Duas perguntas foram ao responsável (A1 e B1); as demais foram resolvidas aqui, com as principais decisões mostradas a ele antes. O que mudou de mais importante:

- a conta de fachada não era condição necessária e deixou de descartar famílias;
- o objetivo da implantação encolhia a casa;
- "perto" entre blocos premiava separar cômodos;
- o corte da volta com motivo eliminava esquemas viáveis;
- o esquema comprido não provava o limite da malha;
- havia escopo duplicado com a calibração 2;
- as fontes de BH e do Rio estavam mal aplicadas.
