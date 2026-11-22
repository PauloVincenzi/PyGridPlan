# M1.2 — Dimensionamento pelo mobiliário

Versão: 0.1 · Criado em: 2026-11-22 · Status: **Proposta** (aguarda aprovação do responsável)
Base: [mvp.md, seção 20.2](mvp.md#202-m12--dimensionamento-pelo-mobiliário) (DEC-0080 a DEC-0083), [pesquisa D2](<../research/Mobiliário mínimo e folgas por cômodo.md>) e notas, DEC-0105, DEC-0108 (norma é referência, não teto). Decisões propostas: DEC-0113 a DEC-0121 no [DECISOES.md](../../DECISOES.md).
Plano: [docs/plans/m1-2-furniture-sizing.md](../plans/m1-2-furniture-sizing.md) (aguarda a aprovação deste design). Dados: [data/furniture.yaml](../../data/furniture.yaml).

O responsável não acompanhou esta rodada. Por isso, o que não vem dele está marcado: **[X]** é hipótese ou decisão do agente, e **[construtor]** fica para quem implementar. As perguntas que só o responsável responde estão juntas na seção 15.

---

## 1. Intenção e o porquê

Conclusão da D1, aceita pelo responsável na S04: **a área mínima de um cômodo é consequência do mobiliário mínimo mais as circulações.** Hoje o gerador usa mínimos fixos por tipo (`min_width_mm`, `min_area_m2` do catálogo), que vêm de fontes diferentes e não dizem se a cama e o guarda-roupa cabem. O M1.2 troca esses números soltos por uma pergunta verificável: **o mobiliário pedido, com as folgas de uso, cabe neste retângulo?**

O objetivo da seção 20.2 continua: o gerador nunca propõe um cômodo em que o que foi pedido não cabe, **sem** precisar de dezenas de perguntas. A DEC-0108 acrescenta um limite: o "mínimo" não é verdade absoluta. O usuário escolhe o rigor e pode afrouxar ou apertar cada valor.

## 2. Por que um documento próprio, e não uma seção nova do mvp.md

1. **Estado diferente.** O mvp.md tem conteúdo aprovado até a seção 21 e as seções 22 e 23 aguardando aprovação. Uma proposta longa lá dentro criaria um terceiro regime de status no mesmo arquivo.
2. **Tamanho.** Este design tem perto de 300 linhas, e o mvp.md já tem 500. Os marcos anteriores couberam em uma seção porque eram ajustes; o M1.2 tem algoritmo, dados, saídas e personalização próprios.
3. **Simetria com os planos.** `docs/plans/` já tem um arquivo por marco. O par design + plano do M1.2 fica fácil de achar e de aprovar junto.
4. **Sem duplicar.** A seção 20.2 do mvp.md continua como o resumo aprovado e ganhou uma linha apontando para cá. Quando este design for aprovado, a 20.2 recebe só a referência às decisões.

## 3. Objetivos, não-objetivos e anti-objetivos

### Objetivos
1. Dados de mobiliário e folgas com fonte por valor, em perfis que o usuário escolhe (`data/furniture.yaml`).
2. Uma verificação "cabe?" determinística, que devolve também **um arranjo** dos móveis (prova de que cabe).
3. O gerador só propõe cômodos em que o conjunto mínimo cabe, no perfil ativo (por padrão; o usuário pode rebaixar para aviso).
4. A largura e a área mínimas de cada tipo passam a ser **derivadas** do mobiliário, por perfil, e não números soltos.
5. Itens pedidos ("cama king", "mesa para 6", "quarto com duas camas") mudam os mínimos daquele cômodo.
6. O relatório HTML e o DXF mostram os móveis, as folgas e o perfil usado.

### Não-objetivos (ficam para depois)
- **Portas e varredura de folha.** O M1 decide cômodos, não portas (DEC-0109). O M1.2 só reserva uma zona livre de chegada (seção 5, regra 5).
- **Relação entre móveis:** distância sofá–TV, triângulo da cozinha, criado-mudo colado à cabeceira, pia ao lado do fogão.
- **Edição dos móveis pelo usuário** (arrastar e girar): fica para o M2, que vai ler o arranjo guardado no `Plan`.
- **Presets de mercado** além de colchões queen e king: os demais vieram de trechos de busca e precisam de conferência da ficha (D2).
- **Perfil acessível da NBR 9050:** os valores lidos são secundários. Os módulos do MCMV entram no perfil `mcmv`.
- Escritório, closet, garagem, varanda, hall e circulação **sem conjunto de móveis**: não há fonte com lista mínima. Continuam com os mínimos do catálogo.
- Ganchos de rede (N e NE), critério de nota de "folga sobrando", texto livre (LLM).

### Anti-objetivos (fracasso mesmo funcionando)
- **Apresentar um perfil como "a norma".** O perfil padrão é uma escolha do projeto, e o relatório diz qual é.
- **Rejeitar em silêncio.** Todo cômodo que não comporta o mobiliário aparece com o que faltou ("precisa de 2,60 × 3,00; tem 2,50 × 3,20").
- **Inventar valor.** Sem fonte, o campo fica vazio e a exigência não existe naquele perfil.
- **Tornar o gerador visivelmente mais lento.** Meta na seção 7.6.
- **Regra mais rígida que a lei por padrão sem o usuário poder afrouxar** (DEC-0108).

## 4. Perfis de mínimo

### 4.1 O que muda em relação à seção 20.2 [X]

A seção 20.2 previa três perfis: **conservador** (padrão: o maior mínimo entre as fontes), **mediana** e **personalizado**. A D2 mostrou dois problemas nessa definição:

- O "maior mínimo entre as fontes" é quase sempre **Panero e Zelnik** (antropometria norte-americana: 0,91 m em volta da cama, 1,01 m na frente da pia). Como padrão, isso infla todos os cômodos e contraria a DEC-0108.
- A mediana é uma **estatística do agente** sobre 2 a 5 valores medidos de formas diferentes. A D2 recomenda "promover o valor com fonte, não a estatística", porque um número que nenhuma fonte publicou não pode ser citado.

**Proposta:** quatro perfis nomeados pela origem, cada valor com a sua fonte, mais a personalização por cima de qualquer um.

| Perfil | O que é | Quando usar |
|---|---|---|
| `nbr` | Anexo informativo da NBR 15575-1. Perfil-base: todo valor que falta nos outros vem dele | o menor mínimo com fonte nacional; casas compactas |
| `mcmv` | Portaria 725/2023, completada pela NBR onde a portaria é omissa (art. 5º: "regramento mais rigoroso"). Inclui os módulos de manobra livres (1,20 × 1,50 em cada cômodo; Ø 1,50 no banheiro) | empreendimento do MCMV ou casa acessível |
| `ergonomico` **(padrão proposto)** | Folgas de Pedro (LNEC) e Boueri, lidas nas reproduções de Mendonça (2015) e Kapitzky et al. (2019), com as dimensões físicas da NBR | casa comum: a D2 aponta 0,60 m como a folga mais defensável, coincidente com Palermo e com o critério de campo de Reis e Lay |
| `folgado` | Panero e Zelnik, via Mendonça | médio e alto padrão |
| personalizado | qualquer perfil acima com valores trocados pelo usuário (seção 9) | sempre |

O "conservador" da 20.2 vira, na prática, a escolha entre `mcmv` e `folgado`; a "mediana", o `ergonomico` (cada número dele foi escolhido perto da mediana, mas é um valor publicado). **Essa troca reabre um item aprovado e é a pergunta 1.**

### 4.2 Valores principais por perfil

Fonte de cada número em `data/furniture.yaml`. Um traço significa "vem do perfil de fallback"; "nenhuma" significa que nenhuma fonte da cadeia dá o valor e a zona não é exigida.

| Folga (mm) | nbr | mcmv | ergonomico | folgado |
|---|---|---|---|---|
| lateral da cama · pé da cama | 500 · 500 | 500 · 500 | 600 · 600 | 910 · 910 |
| entre camas de solteiro | 600 | 800 | 600 | (600) |
| frente do guarda-roupa | 500 | 500 | 600 | 860 |
| frente do assento · da estante | 500 · 500 | — | 500 · 600 | 760 · 1010 |
| borda da mesa | 750 | — | — | 760 |
| frente da pia · fogão · geladeira | 850 · 850 · 850 | — | — | 1010 · 1010 · 910 |
| frente do vaso · lavatório · box | 400 · 400 · nenhuma | — | 600 · 500 · 600 | (600) · 680 · 760 |
| frente do tanque · máquina | 500 · 500 | — | 600 · 600 | (600) · (600) |
| circulação entre móveis | 500 | 500 | 600 | 760 |
| frente da porta | nenhuma | 1200 | nenhuma | nenhuma |

Dimensões físicas que mudam por perfil: cama de solteiro 0,80 × 1,90 (0,90 no `mcmv`); box 0,80 × 0,80 (0,90 × 0,95 no `mcmv`; 1,37 × 0,91 no `folgado`). Larguras mínimas de cômodo só onde a fonte fixa: sala e sala de jantar 2,40 (`nbr`, `mcmv`); cozinha 1,50 (`nbr`) ou 1,80 (`mcmv`); banheiro 1,10 (`nbr`) ou 1,50 (`mcmv`).

## 5. Regras de composição [X]

A D2 concluiu que o gargalo não são as medidas, e sim as **regras de composição**, que nenhuma fonte define. Elas decidem mais a área do cômodo que a escolha entre 0,50 e 0,60 m. Proposta:

1. **Corpo.** Cada móvel é um retângulo `w × d` dentro da área útil do cômodo, sem sobrepor outro corpo. Gira em 0°, 90°, 180° ou 270°.
2. **Zona de uso.** Retângulo colado a um lado do corpo, com o comprimento daquele lado e a profundidade da folga. Fica dentro do cômodo, não sobrepõe nenhum corpo e **pode sobrepor outras zonas de uso**, a zona da porta e os módulos livres. Base: uso não simultâneo, e o próprio texto da NBR ("0,50 m entre o mobiliário e/ou paredes") trata a faixa entre dois móveis como uma só. Reis e Lay usam 0,60 m entre a cama e o guarda-roupa como uma faixa única.
3. **Encosto.** Itens com `wall: back` (camas pela cabeceira, guarda-roupa, sofá, estante, pia, fogão, geladeira, louças, tanque, máquina) têm o lado de trás numa parede. A mesa é livre.
4. **Lados com zona** (`zones`): cama de casal nos dois lados longos e no pé (Pedro: "dois lados e pé"); cama de solteiro em **um** lado longo, à escolha (Pedro: "acesso por uma face"); mesa nos quatro lados, mas **um lado menor pode encostar na parede sem zona** (a NBR admite, achado da conferência visual da S07); demais itens só na frente.
5. **Zona da porta.** Um retângulo livre de 0,80 m (vão do MCMV, único valor federal) por uma profundidade igual à `frente_porta` do perfil ou, sem ela, à `circulacao`. Fica encostado numa parede. Na pré-computação a parede é qualquer uma; na checagem exata, só uma parede por onde o cômodo pode ter porta (seção 7.4).
6. **Alcance.** Toda zona de uso se liga à zona da porta por espaço livre de corpos com largura de pelo menos `circulacao`. Sem isso, um guarda-roupa "cabe" atrás de uma cama que fecha o quarto de parede a parede.
7. **Criado-mudo** (`nightstand`) pode ficar dentro da zona lateral de uma cama, encostado na parede da cabeceira. É como Pedro desenha (0,60 + cama + 0,60, com o criado-mudo na faixa lateral). Sem essa regra, o quarto de casal da NBR precisaria de 2,90 m de largura, e não dos 2,40 que a própria NBR e a v07 do MCMV dão.
8. **Duas camas de solteiro** (`paired_side`): a zona lateral de cada uma usa a maior entre `lateral_cama` e `entre_camas`. Com as zonas sobrepostas, as camas lado a lado ficam a `entre_camas` uma da outra; encostadas nas paredes, dão 0,90 + 0,80 + 0,90 = 2,60 m no MCMV, a conta da D2.
9. **Módulos do MCMV** (perfil `mcmv`): retângulos livres de corpos (podem sobrepor zonas). O círculo de Ø 1,50 vira o quadrado de 1,50 × 1,50 que o contém, o que é conservador (a NBR 9050 deixa o giro avançar 0,30 sob o lavatório, mas esse valor é secundário e não foi promovido).

**Conferência à mão (caso de teste do plano).** Quarto de casal no perfil `nbr`, com cama de 1,40 × 1,90, criado-mudo de 0,50 × 0,50, guarda-roupa de 1,60 × 0,50, folgas de 0,50 e zona da porta de 0,80 × 0,50:

- **Cabe em 2,40 × 2,90:** cama com a cabeceira na parede do fundo e 0,50 de cada lado; pé com 0,50; guarda-roupa na parede oposta, com a zona sobrepondo a do pé; criado-mudo na faixa lateral, junto da cabeceira; porta nos 0,80 ao lado do guarda-roupa.
- **Não cabe em 2,40 × 2,80**, nem em 2,30 de largura com qualquer profundidade.
- **Largura mínima: 2,40 m.** É o valor da NBR e da v07, o que confirma as regras 2, 4 e 7.

No `ergonomico`, a mesma conta dá cerca de 2,50 × 3,10 ou 2,60 × 3,00 (≈ 7,8 m²) [conta do agente, a confirmar pelo verificador]. A D1 tinha 7,62 m² medidos num MCMV real, e Boueri chega a 8,45 m².

## 6. Mobiliário mínimo por tipo de cômodo

Conjuntos em `room_sets` de `data/furniture.yaml`, todos listados pela NBR (Tabelas 1 e 2 da cópia conferida):

| Tipo | Conjunto padrão | Variantes |
|---|---|---|
| `quarto` | `quarto_casal`: cama de casal, 1 criado-mudo, guarda-roupa de casal | `quarto_duplo`: 2 camas de solteiro, 1 criado-mudo, guarda-roupa de 1,50 |
| `quarto_solteiro` | cama de solteiro, criado-mudo, armário de 1,20 | — |
| `sala` | sofá de 3, poltrona, estante de TV; mais assentos conforme os leitos; mais a mesa de 4 se não houver sala de jantar nem copa | — |
| `sala_jantar`, `copa` | mesa de 4 | mesa de 6 |
| `cozinha` | pia, fogão, geladeira | — |
| `banheiro` | lavatório, vaso, box | — |
| `lavabo` | lavatório, vaso | — |
| `lavanderia` | tanque, máquina | — |

**Regras do programa:**

1. **Assentos ≥ leitos** (NBR e MCMV). Leitos = soma de `sleeps` das camas de todos os cômodos (casal 2, solteiro 1). A sala começa com sofá de 3 e poltrona (4 lugares, a forma da Tabela 1). Se faltar assento, entra um sofá de 2 e depois poltronas, uma a uma [X: ordem de composição].
2. **Mesa na sala.** Sem `sala_jantar` nem `copa` no programa, a mesa de 4 entra no conjunto da sala (NBR "sala estar/jantar"; MCMV "sala de estar/refeições: mesa para 4 pessoas").
3. **1 criado-mudo no casal.** A Tabela 1 da NBR diz "mínimo 1" e o MCMV pede 1. A Tabela 2 pede 2, mas admite 1. O mínimo fica 1, e quem quiser 2 lista os itens (seção 9).
4. **Quarto é de casal por padrão** [X]. A NBR numera os dormitórios (casal, 2 pessoas, 1 pessoa), mas o pedido não diz quem dorme onde. O conjunto `quarto_duplo` é escolhido no pedido. Ver a pergunta 5.
5. **Tanque.** A Tabela 1 da NBR diz "tanque externo para unidades térreas". O M1.2 trata a `lavanderia` como cômodo verificado de qualquer forma, e a área externa de serviço fica para quando houver o tipo.

## 7. A verificação "cabe?"

### 7.1 Três formas, com o custo de cada uma

| Abordagem | Como | Custo | Problema |
|---|---|---|---|
| **A. Só checagem depois da geração** | cada alternativa pronta passa por um empacotamento por cômodo; quem falha é rejeitada (ou recebe aviso) | ≈ 10–50 ms por cômodo, ≈ 0,5 s por alternativa [estimativa] | o solver não sabe do mobiliário: propõe banheiros que não comportam o box e gasta uma resolução inteira (20 a 110 s na casa grande) para cada rejeição; pode terminar sem planta |
| **B. Restrição completa no CP-SAT** | posição e giro de cada móvel como variáveis do modelo da planta | modelo várias vezes maior (cômodos × itens × 4 giros × pares sem sobreposição) | o M1.1 já não atinge a meta de tempo; isso a afasta mais. Descartada |
| **C. As duas: escada pré-calculada no CP-SAT e checagem exata depois** (proposta) | para cada conjunto, calcula uma vez a menor profundidade útil para cada largura útil (a "escada"); o modelo da planta ganha **uma** restrição por cômodo; a alternativa pronta passa pela checagem exata, que também produz o arranjo | pré-cálculo ≈ 60 a 80 testes pequenos por conjunto distinto, ≈ 1–4 s [estimativa, a medir]; no modelo, uma restrição `element` por cômodo (desprezível); depois, como na A | a escada ignora em qual parede fica a porta; a checagem exata pode rejeitar, o que deve ser raro (seção 7.4) |

**Proposta: C.** Ela entrega o objetivo da 20.2 (o gerador não propõe o que não cabe) pelo custo da A, sem o desperdício de rejeições em série.

### 7.2 O oráculo `fits`

`fits(conjunto, perfil, W, H, paredes_de_porta=None) → arranjo | None`: um modelo CP-SAT pequeno, em unidades de 10 mm, com 1 worker e semente fixa, o que o torna determinístico.

- **Variáveis:** posição e giro (4 valores) de cada móvel; o lado escolhido da cama de solteiro; a parede e a posição da zona da porta; a posição dos módulos livres.
- **Restrições:** as regras 1 a 9 da seção 5 e a largura mínima do cômodo no perfil.
- **Sobreposição:** proibida entre corpos e entre corpo e zona de uso, zona da porta ou módulo. Zonas sobrepõem zonas à vontade.
- **Alcance (regra 6):** é a única regra que o CP-SAT não expressa bem. Fica num laço preguiçoso:
  1. o CP-SAT acha um arranjo;
  2. o Python confere o alcance numa grade de 50 mm, erodindo o espaço livre por meia `circulacao` e fazendo um flood fill a partir da zona da porta;
  3. se falhar, entra uma cláusula que proíbe aquela combinação de giros e lados relativos, e o modelo resolve de novo.

  O laço para em 30 voltas [construtor: calibrar]. Se não convergir, o resultado é "não confirmado", tratado como **não cabe**, o lado conservador.

### 7.3 A escada e a restrição no gerador

- O gerador trabalha com a área útil aproximada `GRID·k − parede_ext` em cada eixo (`cpsat.py`). A escada é calculada nessa mesma grade: `hmin[k]` = o menor `j` tal que `fits(100k − 150, 100j − 150)`.
- **Monotonia:** se cabe num retângulo, cabe num maior. **Simetria:** o arranjo gira junto com o cômodo. A escada sai por varredura em escada (de `(k mínimo, j máximo)`, desce `j` enquanto couber, senão sobe `k`), só na metade `k ≤ j`. São ≈ 60 a 80 chamadas por conjunto.
- **No modelo:** `hk ≥ hmin[wk]` via `add_element`. Uma largura inviável recebe `hmin` acima do domínio, o que a proíbe. O lado mínimo da escada substitui o `min_side` atual, e a menor área da escada entra como `smallest` na trava de área-alvo (a lógica de `cap` já existe).
- **Cache:** em memória (`functools.lru_cache`), com a chave formada pelos itens resolvidos (dimensões e zonas), os valores do perfil e a largura mínima. Os 5 pedidos da bancada têm de 4 a 8 conjuntos distintos. Cache em disco só se a medição pedir (7.6).
- A aproximação da área útil é **conservadora**: a área real é maior, porque as paredes internas têm 100 mm e não 150. Logo, o que satisfaz a escada também cabe com as medidas reais.
- **Fases e tentativas:** `wk` e `hk` são as mesmas variáveis nas duas fases e em todas as tentativas de forma e de encosto, então a restrição vale em todas, sem código à parte. [decisão do agente na leitura de construtor]
- **Conjunto que não cabe em lugar nenhum:** se a escada sair vazia até o maior cômodo permitido pelo lote, o gerador para antes de resolver, com erro que nomeia o cômodo e os itens ("o mobiliário de q1 — cama king, 2 criados-mudos, guarda-roupa de 2,10 — não cabe em nenhum cômodo deste lote"). [idem]
- **Lista explícita num tipo sem conjunto** (ex.: escritório com `["mesa_4"]`): a verificação vale para os itens listados, como em qualquer cômodo. [idem]

### 7.4 A checagem exata depois da geração

Para cada cômodo com conjunto, na alternativa pronta:

1. Retângulo útil real (`useful_bounds`).
2. **Paredes de porta:** os trechos de parede interna de pelo menos 900 mm compartilhados com um vizinho de onde se chega a este cômodo, pela mesma regra do `check_access` (atravessável, ou suíte para privativo). A fachada também conta para o cômodo de entrada.
3. `fits` com a zona da porta restrita a esses trechos.

**Resultado:**
- se cabe, o arranjo vai para `Plan.furniture`;
- se não cabe com `furniture_rule = "enforce"`, a alternativa é descartada e o padrão é proibido, como já acontece com `check_access` em `generate_alternatives`;
- se não cabe com `"warn"`, a alternativa recebe o aviso `furniture_no_fit`, com o mínimo e o atual.

A rejeição deve ser rara, porque a escada já garante o caso com a porta em qualquer parede. O que sobra é o cômodo cujas únicas paredes de acesso ficam onde só cabe móvel. O plano mede a taxa nos 5 pedidos.

### 7.5 O que deriva disso

- **Largura e área mínimas por tipo e perfil:** saem da escada do conjunto padrão. Novo subcomando `python -m pygridplan furniture-minimums [--profile P]` imprime a tabela, que é a "derivação" prometida na 20.2 e a forma de o responsável conferir os números.
- **Catálogo:** para os tipos com conjunto, `min_width_mm` e `min_area_m2` de `room_types.yaml` ficam redundantes ou mais rígidos que a lei (banheiro 1,50 e cozinha 1,80 vêm do MCMV e hoje valem para toda casa). **Proposta [X]:** remover esses campos desses tipos. As larguras viram dado do perfil (`room_min_width`) e os demais tipos não mudam. Pergunta 2.
- **Alvo menor que o mínimo:** aviso `target_below_furniture` ("alvo de 6 m² menor que o mínimo para o mobiliário, 7,8 m²"). O gerador já usa o maior dos dois.
- **Mensagem de "não coube":** `_no_fit_message` passa a somar as áreas mínimas derivadas.

### 7.6 Metas de custo (a medir na tarefa 1 do plano)

| Medida | Meta | Se passar |
|---|---|---|
| escada de um conjunto | ≤ 2 s | grade de 20 mm no oráculo, ou cache em disco em `out/cache/` |
| pré-cálculo de um pedido da bancada | ≤ 5 s | idem |
| tempo total de 4 alternativas | ≤ +20 % sobre o M1.1 | rever a restrição (só na fase 2) ou a escada |
| alternativas rejeitadas pela checagem exata | ≤ 1 em 4 | a escada passa a exigir a porta numa parede que não seja só de móveis |

## 8. Relatório HTML e DXF

### 8.1 Modelo

O arranjo é o resultado da verificação, como os retângulos dos cômodos são o resultado do solver. Ele fica no modelo central (a fonte da verdade):

```
Plan.furniture: tuple[PlacedItem, ...] = ()
PlacedItem: room_id, item, rect (corpo, mm, absoluto), rotation (0/90/180/270), zones: tuple[Rect, ...]
```

As zonas ficam guardadas porque dependem do perfil e dos valores personalizados do pedido. Assim, DXF e tela não recalculam nada. Um plano antigo sem `furniture` continua válido e sai sem móveis.

### 8.2 Relatório HTML

```
PyGridPlan — 4 alternativas
Perfil de mobiliário: ergonômico (Pedro/Boueri; NBR onde faltam) · regra: impor · 2 valores personalizados
[legenda de cores]
┌ Alternativa 1 — nota 0,91 ───────────────┐
│ planta com móveis (traço claro) e folgas │
│ (tracejado fraco); <title> com o nome    │
│ critérios ...                            │
│ Mobiliário                               │
│  quarto 1   ✓ cabe   mín. 2,60 × 3,00    │
│  banheiro   ✓ cabe   mín. 1,40 × 1,90    │
│  ⚠ quarto 2: alvo 6 m² < mínimo 7,8 m²   │
└──────────────────────────────────────────┘
```

- No SVG, corpos em contorno claro com preenchimento neutro e zonas tracejadas em baixa opacidade. O nome do móvel fica num `<title>` (dica ao passar o mouse), sem rótulos que poluam a planta.
- Cada cartão ganha a tabela "Mobiliário": cômodo, "cabe" ou "não cabe", o mínimo da escada e as medidas úteis.
- O topo do relatório diz o perfil, a regra e os valores personalizados.

### 8.3 DXF

- `A-MOBILIARIO` (já existe e está vazio): cada móvel é um `INSERT` de um bloco `MOB-<item>-<w>x<d>` (contorno e nome), com rotação. No CAD, o usuário move ou troca o móvel como uma peça só.
- **Layer novo** `A-MOBILIARIO-FOLGAS`: as zonas de uso, em polilinha tracejada, cor 8, marcada como não imprimível.
- `A-AVISOS` (já existe): no modo `warn`, o texto "mobiliário não cabe (perfil ergonômico)" no cômodo.

## 9. Personalização

Do mais simples ao mais fino, todos no pedido JSON (o M2 leva para a tela, em tempo real):

```json
{
  "furniture_profile": "ergonomico",
  "furniture_rule": "enforce",
  "furniture_overrides": {
    "clearances": {"lateral_cama": 700},
    "items": {"guarda_roupa_casal": {"w": 2100, "d": 600}},
    "room_min_width": {"banheiro": 1200}
  },
  "rooms": [
    {"id": "q1", "type": "quarto", "furniture": ["cama_king", "criado_mudo", "criado_mudo", "guarda_roupa_casal"]},
    {"id": "q2", "type": "quarto", "furniture": "quarto_duplo"},
    {"id": "esc", "type": "escritorio"},
    {"id": "lav", "type": "lavabo", "furniture": []}
  ]
}
```

| Campo | Efeito |
|---|---|
| `furniture_profile` | perfil base (`nbr`, `mcmv`, `ergonomico`, `folgado`); padrão `ergonomico` |
| `furniture_rule` | `enforce`: o gerador não propõe o que não cabe (padrão); `warn`: só avisa (DEC-0108: o usuário assume) |
| `furniture_overrides` | troca valores do perfil: folgas, dimensões de itens e larguras mínimas, em mm. Valor do usuário não precisa de fonte e aparece no relatório como "personalizado" |
| `RoomRequest.furniture` | id de um conjunto, lista explícita de itens (substitui o conjunto padrão; repetir um id = 2 unidades) ou `[]` (sem verificação neste cômodo) |

Ids desconhecidos dão erro em português na validação do pedido. As regras do programa (assentos e mesa) só se aplicam aos conjuntos padrão: quem lista os itens decide sozinho.

## 10. Mudanças no código (mapa) [construtor: detalhe]

| Arquivo | Mudança |
|---|---|
| `src/pygridplan/model/furniture.py` (novo) | carrega e valida `furniture.yaml` (pydantic, `check_sourced`), resolve perfil, fallback e personalização, e monta o conjunto de cada cômodo com as regras do programa |
| `src/pygridplan/validation/furniture.py` (novo) | `fits` (CP-SAT + alcance), `staircase`, `check_furniture(plan, …)` |
| `src/pygridplan/model/plan.py` | `PlacedItem` e `Plan.furniture` |
| `src/pygridplan/model/request.py` | `furniture_profile`, `furniture_rule`, `furniture_overrides`, `RoomRequest.furniture` |
| `src/pygridplan/generators/cpsat.py` | `hmin` via `add_element`; `min_side` e `smallest` vindos da escada; checagem exata em `generate_alternatives`; `_no_fit_message` |
| `src/pygridplan/export/svg.py`, `report.py`, `dxf.py` | móveis, folgas, perfil e tabela; blocos e layer `A-MOBILIARIO-FOLGAS` |
| `src/pygridplan/__main__.py` | subcomando `furniture-minimums` |
| `data/room_types.yaml` | sem `min_width_mm`/`min_area_m2` nos tipos com conjunto (se a pergunta 2 for aprovada); versão 0.4 |

## 11. Testes

| Teste | Tipo | O que garante |
|---|---|---|
| `test_furniture_data.py` (**já existe nesta rodada**) | rápido | toda medida tem fonte externa; perfis, folgas, itens e conjuntos se referenciam sem buracos; âncoras da D2 |
| `test_furniture_model.py` | rápido | fallback de perfil; personalização; regras do programa (assentos ≥ leitos, mesa na sala, `[]`, lista explícita); id desconhecido dá erro |
| `test_fits.py` | rápido | casal `nbr` cabe em 2,40 × 2,90 e não em 2,40 × 2,80 nem 2,30 × 3,50 (seção 5); duplo `mcmv` com largura ≥ 2,60; o arranjo devolvido respeita as regras 1 a 9 (conferência independente, sem CP-SAT); alcance: corpo que fecha o cômodo é rejeitado; criado-mudo na zona lateral; mesa com o lado menor na parede; `frente_box` ausente no `nbr` |
| `test_staircase.py` | rápido | monotonia, simetria, igualdade com a busca exaustiva num conjunto pequeno; personalização (lateral 900 alarga o casal) |
| `test_generate.py` (acréscimos) | lento | 5 pedidos da bancada: todo cômodo com conjunto passa na checagem exata e tem arranjo em `Plan.furniture`; `nbr` permite banheiro mais estreito que `mcmv`; `warn` nunca rejeita; tempo dentro da meta 7.6 |
| `test_report.py`, `test_dxf.py` (acréscimos) | rápido | perfil e tabela no HTML; blocos no `A-MOBILIARIO` e folgas no layer novo; plano sem móveis exporta igual a hoje |
| `test_cli` (acréscimo) | rápido | `furniture-minimums` imprime as larguras e áreas por tipo |

Conferência visual pelo responsável: `out/m1-2/<pedido>/report.html` nos 5 pedidos, nos perfis `ergonomico` e `nbr`.

## 12. Dados promovidos nesta rodada

Seguindo `data/README.md` (inventário → pesquisa → promoção só do que a fase lê → teste → registro):

- **Promovidos** em `data/furniture.yaml` (v0.1):
  - NBR: todos os itens, folgas e larguras de dormitórios, sala, mesas, cozinha, banheiro e área de serviço;
  - MCMV: cama de solteiro, entre camas, box, larguras, módulos e frente da porta;
  - ergonomia: Pedro e Panero via Mendonça, Boueri via Kapitzky, NAURB;
  - colchões queen e king (mercado, conferidos).
- **Conferência visual da S07** das pp. 1–2 da cópia UNMP: confirma os valores da sala que a D2 deixara pendentes e acrescenta dois achados, a mesa com o lado menor encostado e os 0,50 m na frente da estante.
- **Fontes novas** em `sources.yaml`: `mendonca-2015`, `kapitzky-2019`, `naurb-ufpel` e `madeiramadeira-colchoes`. Notas corrigidas: `nbr15575-1-anexo` (Anexo F/G, conferência), `mcmv-725-2023` (itens do Anexo III) e `mcmv-espec-2017` (substituída).
- **Não promovidos:**
  - presets de mercado de trechos de busca;
  - Palermo, LNEC e Portaria 168 (só trecho);
  - quadros ambíguos de Pedro (mesa de centro, tanque);
  - NBR 9050 secundária;
  - lavatório do MCMV (≥ 0,30 × 0,40: a orientação não é dita, e a diferença para a NBR é de 1 cm);
  - máquina de abertura frontal (1,10, Pedro);
  - sofás sem braço;
  - Reis e Lay (o valor coincide com Pedro, que já é a fonte).

## 13. O que fica a cargo do construtor

- A formulação exata do oráculo: variáveis de giro, `add_no_overlap_2d` ou pares com booleanos, e a cláusula do laço de alcance.
- A grade de alcance (50 mm proposto) e o limite de voltas.
- O estilo visual dos móveis no SVG (sem desviar do relatório atual) e o desenho dentro dos blocos DXF (contorno e nome bastam).
- Os nomes internos de funções e mensagens, em português, no padrão das atuais.
- A interação da escada com a proporção máxima (2,5) e com a faixa da circulação: as restrições convivem no modelo. Se um conjunto só couber fora da proporção, o erro de "não cabe" deve dizer isso.

## 14. Hipóteses do agente (resumo para conferir)

1. Perfil padrão `ergonomico`, e não o "conservador" da 20.2.
2. Regras de composição 1 a 9 (seção 5), em especial a sobreposição livre entre zonas e o criado-mudo dentro da zona lateral.
3. Abordagem C (escada + checagem exata), com as metas de custo da 7.6 ainda por medir.
4. "Cabe?" é restrição por padrão (`enforce`); `warn` é opção do usuário.
5. Remoção dos mínimos do catálogo nos tipos com conjunto.
6. Quarto de casal por padrão; mesa na sala sem sala de jantar; ordem de composição dos assentos.
7. Arranjo guardado no `Plan`.
8. Zona da porta de 0,80 × `circulacao` fora do MCMV.

## 15. Perguntas ao responsável (bloco único, da mais importante para a menos)

1. **Perfil padrão.** A seção 20.2 aprovou "conservador = o maior mínimo entre as fontes". A D2 mostrou que isso é Panero (0,91 m em volta da cama, 1,01 m na frente da pia). Proponho quatro perfis com fonte (`nbr`, `mcmv`, `ergonomico`, `folgado`) e o **`ergonomico` como padrão**. Aceita a troca, ou prefere outro padrão? Se for o `nbr`, as casas ficam menores; se for o `mcmv`, maiores e acessíveis.
2. **Mínimos do catálogo.** Hoje, banheiro com 1,50 e cozinha com 1,80 (valores do MCMV) valem para toda casa. Proponho que, nos tipos com conjunto de móveis, o mínimo passe a ser só o que o mobiliário pede no perfil escolhido (no `ergonomico`, o banheiro fica perto de 1,40). Remover esses mínimos do catálogo, ou mantê-los como piso extra?
3. **Restrição ou aviso por padrão.** Proponho que o gerador não proponha cômodo em que o mobiliário mínimo não cabe (`enforce`), com a opção `warn` para quem quer assumir. Concorda que o padrão seja `enforce`?
4. **Regras de composição.** As que mais mexem na área:
   - zonas de uso de móveis diferentes podem se sobrepor;
   - o criado-mudo pode ficar na faixa lateral da cama;
   - a cama de solteiro precisa de um lado livre só;
   - a mesa pode ter um lado menor na parede;
   - sofá e poltrona encostados na parede;
   - zona da porta de 0,80 × a circulação do perfil.

   Alguma delas contraria o que você faria num projeto?
5. **Quarto de casal ou duplo.** Proponho todo `quarto` como casal, e o duplo só quando o pedido disser. A alternativa é seguir a NBR pela ordem: 1.º quarto casal, 2.º duplo, 3.º solteiro. Qual prefere?
6. **Mobiliário no `Plan`.** Proponho guardar o arranjo (corpo, giro e zonas) no modelo, para o DXF e o futuro M2 lerem sem recalcular. Concorda?
7. **Presets de mercado.** Só os colchões queen e king entraram. A D2 diz que conferir cerca de 20 fichas (sofá, guarda-roupa, geladeira) muda mais o resultado que qualquer norma. Isso vira uma trilha de dados antes do M2, durante ou depois?
8. **Ordem M1.2 → M2** (pendente da S07). Este plano assume o M1.2 inteiro antes do design do M2. Mantém?
