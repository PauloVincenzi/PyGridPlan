# PyGridPlan — Documento de design do MVP

Versão: 1.3 · Criado em: 2026-11-11 · Atualizado em: 2026-11-12 · Status: **conteúdo aprovado; seção 20 (M1.1 e M1.2) aguarda aprovação do responsável**
Fonte: decisões DEC-0001 a DEC-0061 do [DECISOES.md](../../DECISOES.md). O histórico de versões deste arquivo está no git. Cada item abaixo cita a decisão de origem. O que não vem de decisão do responsável está marcado como **[decisão do Agente]** ou **[a cargo do construtor]**.

---

## 1. Intenção e o porquê

O PyGridPlan gera **plantas baixas residenciais 2D**, offline, a partir de um pedido que mistura campos fixos, campos opcionais e texto livre. A planta é construída **ao vivo, por etapas**, e em cada etapa o sistema oferece **algumas alternativas diferentes entre si** para o usuário escolher. O resultado sai em **DXF** (DEC-0006, DEC-0007, DEC-0008, DEC-0023).

É um projeto de **portfólio e estudo** (arquitetura de software, geometria computacional, otimização, estatística e IA aplicada), feito para dar orgulho ao responsável, que também é o primeiro usuário (DEC-0001).

**Diferencial:** "planta boa" é o que **cada usuário** define pelas próprias preferências. O sistema só impõe um piso mínimo de validade e recomendações que o usuário pode furar de forma consciente (DEC-0029, DEC-0031).

**Critério de sucesso:** versatilidade. O app interpreta pedidos variados e gera plantas boas o bastante para um arquiteto ou engenheiro usar como ponto de partida (DEC-0001).

## 2. Objetivos, não-objetivos e anti-objetivos

### Objetivos do MVP
1. Entrar com terreno e cômodos (campos) e ver a planta nascer na tela, etapa por etapa.
2. Gerar várias alternativas de disposição de cômodos com um solver de restrições (CP-SAT) e deixar o usuário escolher, voltar e escolher outra.
3. Garantir sempre a **validade geométrica** (seção 5.1).
4. Exportar a planta escolhida em DXF com layers organizados.
5. Mostrar o raciocínio: console com cada comando, grafo de relações ao vivo e o "por quê" de cada decisão.

### Não-objetivos (ficam para depois do MVP)
- 3D, multipavimento, terreno irregular, cômodos não retangulares, formas curvas (DEC-0003, DEC-0046 a DEC-0049).
- Plantas elétrica e hidráulica, paisagismo, cores de parede (DEC-0003).
- Os geradores 3 e 4, crescimento em grade e recozimento simulado (DEC-0050).
- Conformidade com normas e legislação municipal. O app **não afirma** conformidade (DEC-0015).
- Instalador desktop (Tauri) e versão aprofundada do servidor MCP (DEC-0011, DEC-0012).

### Anti-objetivos (seria fracasso mesmo funcionando)
- **Interface com cara de dashboard**, lenta ou cheia de botões (DEC-0013).
- **LLM desenhando ou definindo coordenadas**. A geometria é sempre determinística (DEC-0005).
- **Violar uma recomendação em silêncio.** Toda violação aceita aparece na tela, no histórico e no DXF (DEC-0031).
- **Caixa-preta.** Uma decisão do motor que não pode ser explicada (DEC-0021).
- **Depender de internet ou de API paga** para funcionar (DEC-0004).
- **Alternativas quase iguais** apresentadas como escolhas diferentes (DEC-0023).
- **Código inchado**: abstrações e configurações que ninguém pediu (pedido do responsável na S03).

## 3. Restrições

- **Offline e gratuito** (DEC-0004). Nenhuma chamada de rede em tempo de execução.
- **Hardware de referência:** i5-1335U, 8 GB de RAM (DEC-0005). O LLM local e o solver precisam caber nisso.
- **Ambiente presente:** Python 3.13, Node.js 26.13 LTS, Git (DEC-0014, S01).
- **Stack:** motor em Python, interface em HTML/CSS/TypeScript rodando no navegador local (DEC-0011).
- **Dependências** só entram com justificativa e teste (DEC-0009, CLAUDE.md).
- **Repositório público:** normas pagas e livros protegidos não entram; só valores extraídos com a citação (DEC-0024, DEC-0038).

## 4. Arquitetura

### 4.1 Visão geral

```
 Navegador (TypeScript)                       Python (motor)
 ┌──────────────────────────┐   HTTP/WS   ┌──────────────────────────────────────┐
 │ planta · grafo · console │ ◄─────────► │ servidor local (comandos + eventos)  │
 │ premissas · faixa A/B    │             ├──────────────────────────────────────┤
 └──────────────────────────┘             │ interpretação: regras + LLM → JSON  │
                                          │ pipeline de etapas (árvore estados) │
                                          │ geradores (CP-SAT, subdivisão)      │
                                          │ validador · pontuação               │
                                          │ modelo central  →  exportador DXF   │
                                          └──────────────────────────────────────┘
```

Princípios (CLAUDE.md, DEC-0005, DEC-0012):
- O **modelo central** é a fonte da verdade. Tela, DXF e o futuro 3D são derivados dele.
- A **IA é separada** da geometria. Ela só preenche o JSON do pedido.
- O motor expõe **comandos**. Interface, LLM, testes e o futuro MCP usam os mesmos comandos, e o console os mostra.

### 4.2 Motor em 4 camadas (DEC-0009)

1. **Topologia:** grafo de cômodos e relações com pesos, zonas social, íntima e serviço. Candidata: NetworkX.
2. **Geometria:** otimização por restrições numa grade modular. Candidata: OR-Tools CP-SAT.
3. **Alternativas:** várias soluções por etapa, escolhidas para serem diversas.
4. **Estatística:** medida de diversidade agora; calibração e aprendizado de pesos depois.

### 4.3 Comandos e eventos (DEC-0012, DEC-0027)

Toda operação do motor é um comando com nome e argumentos validados, por exemplo:

| Comando | Efeito |
|---|---|
| `site.set` | define o terreno (largura, profundidade, recuos, lado da frente, norte) |
| `rooms.set` | define a lista de cômodos e itens pedidos |
| `relation.set` | define a relação entre dois cômodos (aproximar/afastar, intensidade 1–5) |
| `pref.set` | define o peso de uma preferência |
| `stage.generate` | gera K alternativas para a etapa atual a partir do nó escolhido |
| `stage.choose` | escolhe uma alternativa e avança |
| `tree.goto` | volta a um nó anterior da árvore |
| `warning.accept` | aceita uma violação de recomendação (fica registrada) |
| `export.dxf` | exporta o nó escolhido |

O motor emite **eventos** enquanto trabalha (comando recebido, etapa iniciada, solução parcial, solução encontrada, retrocesso, aviso, fim). O console exibe os eventos como linha do tempo de chat, com horário. Os nomes exatos dos comandos são **[a cargo do construtor]**; o requisito é que sejam os mesmos para a interface, os testes e o futuro MCP.

### 4.4 Árvore de estados (DEC-0023)

O projeto é uma **árvore de estados**, como os ramos do git:
- cada nó guarda a etapa, o estado completo da planta naquele ponto, as premissas em vigor e o nó pai;
- cada etapa gera **K alternativas** (de 3 a 5; **[decisão do Agente]**: padrão K = 4, configurável);
- só o ramo escolhido é expandido; as irmãs ficam "não expandidas" até o usuário voltar a elas (DEC-0028, resposta registrada);
- desfazer, refazer e comparar alternativas saem dessa estrutura.

## 5. Avaliação de uma planta

### 5.1 Validade geométrica — inegociável (DEC-0031, DEC-0035)
Uma solução que viola qualquer item abaixo **não é uma planta** e é descartada, nunca pontuada:
- sobreposição de cômodos, paredes, móveis ou quaisquer elementos;
- elementos fora do terreno;
- cômodo inalcançável: todo cômodo tem ao menos uma porta e um caminho até a entrada (verificável a partir da etapa 2);
- incoerência vertical (relevante só no multipavimento futuro).

O **validador** é um módulo independente dos geradores, e todo gerador passa por ele.

### 5.2 Recomendações — negociáveis com sinalização (DEC-0031)
Dimensões e áreas mínimas, folgas de circulação, garagem por veículo, recuos etc. Regras:
- o motor **nunca** viola uma recomendação por conta própria; ele só **propõe** a violação durante uma negociação (DEC-0020). Portanto, **até a negociação existir (M6), mínimos e recuos são restrições rígidas** no solver **[decisão do Agente]**;
- antes da biblioteca de medidas, os mínimos por tipo de cômodo usam **valores provisórios**, marcados como "provisório, sem fonte" nos dados e na tela, até serem substituídos por valores com citação **[decisão do Agente]**;
- uma violação aceita fica sinalizada na planta (⚠ com o valor recomendado vs. o adotado), registrada no histórico como "termo de ciência" e anotada no DXF.

### 5.3 Objetivos do usuário (DEC-0029, DEC-0032)
Cada preferência vira um critério com peso. No MVP, os pesos vêm de:
- campos e botões (sim/não);
- relações entre cômodos com intensidade 1–5 e direção (aproximar/afastar);
- escalas bipolares (−2 a +2) para "o que você valoriza" (DEC-0036);
- texto livre interpretado (seção 7).

**Critérios ativos antes do M5 [decisão do Agente]:** relações entre cômodos (adjacência ponderada), boas práticas padrão (5.4) e **orientação solar**. Como o uso é no Brasil (hemisfério sul), o sol "bom" vem do **norte**: por padrão, quartos e sala preferem fachadas norte/leste, e áreas de serviço aceitam sul/oeste. O hemisfério é um parâmetro do terreno (padrão: sul). Na faixa de baixo do M2, as perguntas são as **escalas bipolares** de uma lista inicial fixa de valores (iluminação, quintal, cozinha integrada, privacidade dos quartos, área de serviço separada), como manda a DEC-0036.

### 5.4 Boas práticas padrão (DEC-0033)
Valem quando o usuário não se manifestou, com peso baixo: minimizar sempre a área de corredor; área verde mínima quando o quintal não foi citado; agrupar áreas molhadas quando viável.

### 5.5 Passagem entre cômodos (DEC-0060)
Todo cômodo precisa ser alcançável a partir da entrada (5.1), mas **nem todo cômodo pode ser atravessado** no caminho até outro:
- **Privativos (não atravessáveis):** quarto, banheiro (incluindo lavabo) e closet. Exceção natural dentro de uma suíte: quarto → closet → banheiro. Isso é circulação interna da suíte, não travessia social.
- **Atravessáveis:** todos os demais cômodos (salas integradas ou separadas, cozinhas, áreas de lazer, varandas, lavanderia, garagem, home theater, academia, spa, quadras etc.).
- A classe de passagem é um **atributo do tipo de cômodo** no catálogo (seção 14). Um tipo novo ou personalizado entra como atravessável, e o usuário pode mudar.
- **[Decisão do Agente]:** atravessar um cômodo é permitido, mas tem um custo suave nas boas práticas (5.4), maior para cômodos de uso concentrado (home theater, escritório, spa). Assim o motor evita, por padrão, que a sala de cinema vire corredor.
- Programas atípicos e de alto padrão (várias cozinhas, cinema, spa, academia, quadras, excesso de cômodos convencionais) precisam ser representáveis: o catálogo é aberto, e nenhuma regra supõe uma lista fixa de cômodos.

A **entrada** fica na frente do terreno; o motor escolhe a posição, e o usuário pode ajustar **[decisão do Agente]**.

### 5.6 Agregação (DEC-0034)
**No MVP [decisão do Agente]:** soma ponderada de critérios normalizados em [0, 1], com **utilidade de retornos decrescentes** por critério (ex.: raiz ou logaritmo da área de quintal). A nota é sempre exibida **decomposta por critério**.
**Depois do MVP:** integral de Choquet (interação entre critérios) e fronteira de Pareto. A interface de pontuação deve aceitar trocar o agregador sem mexer nos geradores.

## 6. Pipeline de etapas

### 6.1 Etapas (DEC-0007, DEC-0017)
0. **Premissas:** terreno, cômodos, relações, preferências e, quando aplicável, a implantação (6.2). O grafo de bolhas nasce aqui.
1. **Cômodos:** posição e dimensões dos retângulos, contidos no terreno com os recuos, sem sobreposição, respeitando mínimos, adjacências e orientação. Inclui a circulação como cômodo próprio, minimizado.
2. **Portas e janelas:** portas garantem a alcançabilidade (5.1); janelas ficam em paredes externas e entram nos critérios de iluminação e ventilação.
3. **Mobiliário simplificado** (retângulos e círculos), começando pela mobília fixa e pelos itens pedidos.

As paredes são **derivadas** da etapa 1: arestas compartilhadas entre cômodos viram paredes internas, e o contorno vira parede externa.

**Modelo de eixos [decisão do Agente]:** os retângulos dos cômodos são desenhados **nos eixos das paredes** e ficam na grade de 100 mm. Dois cômodos vizinhos compartilham a aresta (o eixo da parede entre eles). Consequências:
- "sobreposição" no validador significa interseção de **interiores** de retângulos; tocar pela aresta é permitido e é o que gera parede;
- a adjacência é o comprimento da aresta compartilhada;
- a **área útil** de um cômodo desconta meia espessura de cada parede que o cerca (externa 150 mm, interna 100 mm), e é ela que é comparada com os mínimos;
- o DXF desenha cada parede como faixa centrada no eixo; o contorno externo da casa fica a meia espessura externa para fora dos eixos, e isso entra na checagem de recuos.

### 6.2 Implantação no terreno (DEC-0059)
- **Padrão: bloco único.** A casa nem sempre precisa ser um bloco só; blocos separados (ex.: edícula, área de lazer isolada) são representáveis no modelo, mas **o gerador do MVP produz bloco único** **[decisão do Agente]**.
- **Área construída pretendida** é um campo opcional. Sem ele, o motor estima pela soma dos mínimos dos cômodos mais a circulação.
- **Pergunta de implantação** (faz parte da etapa 0): *"A casa pode encostar em alguma divisa?"*, com marcação múltipla de **esquerda**, **direita** e **fundo**. Nenhuma marcada significa casa solta, afastada de todos os lados. A frente nunca encosta (recuo frontal).
- **Quando perguntar:** só quando a ocupação torna a pergunta relevante. A pergunta aparece se **qualquer** das condições for verdadeira **[limiares: decisão do Agente, configuráveis]**:
  1. área pretendida ÷ área do terreno ≥ **0,30**;
  2. a casa, na forma mais compacta possível, não cabe com os afastamentos laterais e de fundo recomendados.
  Exemplo: terreno 10×25 m (250 m²) com 100 m² pretendidos → 0,40 → pergunta. Terreno 100×100 m com 200 m² → 0,02 e cabe folgado → não pergunta; casa solta.
- Sem pergunta, a casa é **solta** e o motor escolhe a posição. A escolha fica nas premissas e pode ser mudada depois.
- Encostar numa divisa zera o afastamento daquele lado; os afastamentos dos lados não marcados continuam como recomendação (5.2).

### 6.3 Pré-dimensionamento (DEC-0018, DEC-0024, DEC-0025)
Antes da etapa 1, cada item pedido ("mesa para 6", "ilha", "pia de 2 m") é convertido em dimensões mínimas do cômodo, usando a **biblioteca de medidas**. Cada mínimo guarda sua **origem** legível ("largura mínima da cozinha = 3,20 m por causa da ilha…"). Os itens têm presets de tamanho e aceitam medida personalizada.

### 6.4 Retrocesso (DEC-0019, DEC-0020, DEC-0021, DEC-0026)
- Uma etapa que não consegue cumprir sua tarefa devolve um **motivo estruturado** (etapa, elemento, tipo, valor, explicação), que vira restrição aprendida na etapa anterior.
- As restrições aprendidas aparecem num **caderno visível**, marcadas como rígidas ou suaves, e o usuário pode removê-las.
- Cada etapa tem um orçamento de tentativas e de tempo. Ao estourar, ao detectar ciclo ou quando a nota cai abaixo de um piso, o sistema **negocia com o usuário** o que ceder, mostrando o custo de cada opção.
- O solver sempre devolve a melhor solução até o momento; a interface nunca trava.
- Todo retrocesso aparece no console e na planta, com a versão anterior em "fantasma".

## 7. Interpretação do pedido (DEC-0005, DEC-0006)

- O pedido vira um **JSON de schema fixo**, validado antes de chegar ao motor.
- Um **parser de regras** cobre o que é estruturado (números, cômodos, palavras-chave). Ele funciona **sem o LLM**.
- Um **LLM pequeno local** cobre o texto livre e só preenche campos do JSON (ex.: "oficina longe dos quartos" → relação afastar, oficina × dormitórios, intensidade 4). Nunca gera coordenadas.
- O provedor de LLM é substituível. O modelo específico e o runtime (llama.cpp, Ollama ou similar) **dependem de um teste no hardware de referência** (seção 12).
- Preferências do texto livre aparecem como premissas editáveis no painel, para o usuário corrigir uma interpretação errada.

## 8. Geradores (DEC-0010, DEC-0050)

Todos os geradores seguem uma **interface comum**: recebem o problema da etapa (premissas, restrições, nó pai), um K, uma semente e um orçamento; emitem eventos de progresso e devolvem soluções no mesmo modelo de planta, avaliadas pela mesma pontuação.

1. **CP-SAT** (primeiro): variáveis inteiras para posição e tamanho de cada cômodo na grade; sem sobreposição (`NoOverlap2D`); contido no terreno com recuos; mínimos de largura e área; adjacência medida como **comprimento de parede compartilhada**. A diversidade das K soluções vem de resolver em sequência, exigindo distância mínima das soluções anteriores, ou de variar pesos e topologia **[a cargo do construtor]**, desde que a métrica de diversidade (seção 9) aprove o resultado.
2. **Árvore de subdivisão** (segundo): corta o terreno recursivamente seguindo o grafo de zonas. É rápida e muito visual.

Os geradores 3 e 4 entram depois do MVP sem refatoração, graças à interface comum.

**Meta de desempenho [decisão do Agente]:** para 8 a 12 cômodos, cada alternativa sai em até ~5 s no hardware de referência, e o conjunto de K em até ~20 s. O gerador **transmite soluções parciais desde o M1** (eventos), e a interface mostra a melhor até o momento. Se a meta não for atingida no teste da seção 12, a grade ou o K padrão são revistos, e isso é registrado como decisão.

## 9. Diversidade das alternativas (DEC-0023)

As K alternativas de uma etapa precisam ser **diferentes de verdade**. **[Decisão do Agente]:** uma distância entre plantas que combine posição relativa dos cômodos (quem está ao norte, sul, leste ou oeste de quem) e sobreposição de áreas por cômodo; as K alternativas são escolhidas para maximizar a menor distância entre pares, entre as candidatas que passam no validador e têm nota acima de um piso.

## 10. Modelo de dados

**[Decisão do Agente]**, partindo do IDEIA.md (DEC-0015) e de DEC-0046:
- **Unidade interna:** milímetros inteiros. Exibição em m e cm. A grade de snap é independente: padrão 100 mm, configurável.
- **Entidades com ID único:** `Project`, `Site` (polígono, recuos, aresta da frente, direção do norte), `Floor`, `Room` (tipo, zona, geometria, mínimos com origem), `Wall` (eixo, espessura, interna/externa), `Opening` (porta/janela, parede, posição, largura), `Furniture`, `Relation`, `Preference`, `Constraint` (rígida/suave, origem, aprendida ou não), `AcceptedWarning`, `StateNode`.
- A geometria é genérica (polígono), mas os algoritmos do MVP só aceitam retângulos e terreno retangular, com um único `Floor` (DEC-0046).
- Espessuras de parede padrão: externa 150 mm, interna 100 mm **[decisão do Agente; valores a revisar com a biblioteca de medidas]**.
- O projeto salva e abre como um arquivo JSON (o botão "salvar/abrir" da faixa superior).

## 11. Interface (DEC-0013, DEC-0022, DEC-0027, DEC-0028, DEC-0040 a DEC-0045)

Referência visual aprovada: [mockups/layout-v5.html](mockups/layout-v5.html).

- **Tema escuro**, inspirado no AutoCAD, muito mais simples. Paleta: preto, cinzas, branco, laranja e roxo.
- **Faixa superior** (30% maior que a do v2): novo, abrir, salvar, excluir, abas de projeto e indicador de etapa.
- **Planta** com malha infinita, pan e zoom; ao definir o terreno, o contorno aparece e a tela centraliza. Mostra só as **cotas do terreno** no MVP, no estilo do AutoCAD (DEC-0044).
- **Painel direito:** 70% premissas, 30% console (DEC-0043).
  - Premissas: grafo de relações em miniatura no topo; depois terreno, cômodos, itens, relações, "o que você valoriza" e avisos, separados por linhas suaves. Fatos em texto corrido; intensidades com **1 a 5 pontos** na cor da direção (verde = quero/aproximar, vermelho = evitar/afastar) (DEC-0045). Item mais recente em laranja.
  - Campo de texto livre 30% maior, com o rótulo "✎ Texto livre: ajuste qualquer coisa que não foi perguntada".
  - Console em monoespaçada pequena, com horário e scroll.
- **Faixa de baixo:** "a decisão da vez", uma pergunta por vez, com texto ~17 px e botões grandes. No A vs. B, duas plantas grandes lado a lado, resumo curto e simétrico das diferenças com barras e "ver detalhes" (DEC-0037, DEC-0039).
- **Grafo de bolhas:** nasce grande no centro com animação de forças com inércia; nós retangulares com tamanho pela área e cor pela zona; ligações de atração e repulsão com estilos diferentes e pesos em números. Quando os primeiros esboços aparecem, encolhe para o painel (DEC-0022, DEC-0028).
- Movimento com propósito, nunca enfeite. Nada de cara de dashboard.

## 12. Validações técnicas antes de fixar dependências

Cada candidata entra só depois de um teste curto que a justifique (DEC-0009):

| Candidata | O que validar |
|---|---|
| OR-Tools CP-SAT | instala no Python 3.13; resolve 8–12 cômodos em grade de 100 mm num terreno 25×10 m em poucos segundos no hardware de referência |
| ezdxf | gera DXF com os layers da seção 13 e abre num visualizador DXF |
| NetworkX | só se o grafo precisar de algoritmos além do trivial; senão, estrutura própria |
| FastAPI + WebSocket | stream de eventos para o console sem travar a interface |
| Pydantic | validação do JSON do pedido e dos comandos |
| LLM local (ex.: modelos de 1–4 B parâmetros quantizados) | cabe em 8 GB junto com o resto, responde em segundos, preenche o JSON corretamente num conjunto de frases de teste |
| Build do TypeScript (ex.: Vite) e desenho da planta (SVG ou Canvas) | **[a cargo do construtor]**, com o requisito de animação fluida e pan/zoom |

## 13. Exportação DXF (DEC-0008)

- Via ezdxf, sem precisar do AutoCAD.
- Layers do MVP **[decisão do Agente, a partir da lista pendente da DEC-0015]**: `A-TERRENO`, `A-EIXOS` (DEC-0068), `A-PAREDES-EXT`, `A-PAREDES-INT`, `A-PORTAS`, `A-JANELAS`, `A-MOBILIARIO`, `A-COTAS`, `A-TEXTOS`, `A-AREAS`, `A-AVISOS` (violações aceitas).
- Representação (DEC-0068): paredes como **hachura sólida**, estendidas até a face da parede perpendicular (quinas e encontros em T fechados); **eixos** em layer próprio, vermelho, traço-ponto; `A-AREAS` com o contorno da **área útil** (faces internas).
- Unidade do desenho em milímetros.

## 14. Biblioteca de medidas e base teórica (DEC-0024, DEC-0038)

- `data/`: dados de referência estruturados (YAML ou JSON) com **fonte, versão e data** em cada valor. Dois conjuntos iniciais:
  - **catálogo de tipos de cômodo:** zona, classe de passagem (5.5), mínimos provisórios ou citados. É a **fonte única** dessas informações; o código não repete listas de cômodos;
  - **medidas de itens:** móveis, eletrodomésticos, louças e folgas, com presets de tamanho.
- `docs/theory/`: uma nota de síntese por tema (o que é, por que importa aqui, fórmulas, exemplo, referências). Temas obrigatórios antes de implementar: agregação multicritério (Choquet, Pareto) e obtenção de pesos (Likert, AHP, conjoint, Bradley-Terry).
- No MVP, a biblioteca começa pequena: os itens que os testes e o exemplo de referência usam.

## 15. Testes

- Uma funcionalidade só está pronta com testes passando (CLAUDE.md).
- O **validador** é a peça mais testada: casos válidos e inválidos para cada regra da seção 5.1.
- Todo gerador roda contra um conjunto de **casos de referência** (terrenos e programas de cômodos), e toda solução gerada passa pelo validador no próprio teste.
- O parser de regras e o LLM têm um conjunto de frases com o JSON esperado.
- O DXF exportado é relido e conferido (layers, entidades, unidades).
- A interface tem testes de ponta a ponta com playwright nos fluxos principais.

## 16. Marcos de construção [decisão do Agente]

Cada marco entrega algo que roda e é testado:

| Marco | Entrega |
|---|---|
| M0 | Esqueleto do repositório, modelo de dados, validador geométrico e exportador DXF (com uma planta escrita à mão) |
| M1 | Gerador CP-SAT da etapa 1 com K alternativas diversas e pontuação decomposta; tudo via linha de comando (a árvore de estados foi para o M2, DEC-0076) |
| M1.1 | Forma e implantação: bloco retangular sem vazios internos, paredes alinhadas, implantação previsível, encostar na divisa em lote pequeno, muro, áreas externas e esquema de 4 cores (seção 20) |
| M1.2 | Dimensionamento pelo mobiliário: dados D2 de mobiliário mínimo e folgas, verificação "cabe?" e perfis de mínimo (seção 20) |
| M2 | Servidor local e interface: malha, terreno com cotas, premissas, console ao vivo, faixa de decisões, escolha entre alternativas, salvar/abrir, exportar DXF |
| M3 | Grafo de bolhas animado e A vs. B com resumo simétrico |
| M4 | Etapa 2: portas (alcançabilidade) e janelas |
| M5 | Interpretação: parser de regras, depois LLM local |
| M6 | Pré-dimensionamento com a biblioteca de medidas e retrocesso com restrições aprendidas e negociação |
| M7 | Gerador por árvore de subdivisão e comparação lado a lado |
| M8 | Etapa 3: mobiliário simplificado |

**Onde termina o MVP:** o responsável decide ao longo do caminho (DEC-0017). **Sugestão do Agente:** considerar o MVP fechado em M5, quando o fluxo completo (pedido em texto → alternativas → escolha → DXF) já funciona.

## 17. Estrutura do repositório (DEC-0058)

```
src/pygridplan/        pacote Python (motor), layout "src"
  model/               entidades e serialização
  validation/          validade geométrica e recomendações
  pipeline/            etapas, árvore de estados, retrocesso
  generators/          cpsat/, subdivision/
  scoring/             critérios, agregação, diversidade
  interpret/           parser de regras, LLM, schema do pedido
  export/              dxf
  server/              comandos e eventos (HTTP/WebSocket)
web/                   interface TypeScript
data/                  dados de referência versionados (catálogo de cômodos, medidas)
tests/                 testes; fixtures/ guarda os casos de referência
docs/design/           documentos de design e mockups aprovados
docs/plans/            planos de implementação, um por marco
docs/theory/           fundamentação teórica
out/                   saídas geradas (DXF, projetos salvos) — fora do git
```

Cada pasta nasce quando o primeiro arquivo dela é criado; não se criam pastas vazias. Os subpacotes de `src/pygridplan/` são o alvo; o construtor pode juntar ou separar módulos conforme o código pedir.

## 18. O que fica a cargo do construtor

- Nomes exatos de comandos, eventos, módulos e funções.
- Estratégia concreta de diversidade no CP-SAT, desde que passe na métrica da seção 9.
- Ferramenta de build do TypeScript e técnica de desenho (SVG ou Canvas).
- Formato dos arquivos da biblioteca de medidas (YAML ou JSON).
- Tempo e tentativas padrão de cada etapa, desde que configuráveis.

## 19. Questões em aberto

- Ponto final do MVP (seção 16).
- Modelo e runtime do LLM local (seção 12).
- Fontes de referência das medidas (Neufert, NBR 15575, outras) e como citá-las (DEC-0018).
- Perguntas, ordem e escala do quiz de preferências (DEC-0032).

## 20. Qualidade das plantas: M1.1 e M1.2 (S04, DEC-0080 a DEC-0083)

Contexto: as 4 plantas do M1 são válidas, mas têm silhueta recortada, vãos internos sem uso, pouca parede "na mesma reta" e implantação aleatória no lote. **Não é um erro de código; é uma lacuna do modelo:** no M1, o solver só penalizava o perímetro da caixa envolvente e buscava o tamanho-alvo de cada cômodo isoladamente. Nada pedia um bloco cheio, alinhamento de paredes, cômodos iguais enfileirados ou uma posição definida no lote. O solver escolheu, entre milhões de arranjos válidos, um qualquer.

### 20.1 M1.1 — Forma e implantação

1. **Bloco cheio.** Novo critério `void_area` = área da caixa envolvente − soma das áreas dos cômodos, com peso alto. A planta tende ao retângulo cheio; formas em L e T continuam possíveis quando o programa ou o lote pedirem.
2. **Sem vazio interno sem uso.** Um vazio cercado por cômodos dos quatro lados é **rejeitado**, a menos que o pedido peça um pátio ou jardim de inverno (aí o vazio vira área externa rotulada). Recortes na borda do bloco viram área externa.
3. **Paredes na mesma reta.** Novo critério `alignment`, que premia cômodos vizinhos com faces na mesma linha (mesmo x, x2, y ou y2) e cômodos do mesmo tipo com a mesma profundidade e alinhados (ex.: 3 quartos enfileirados). É um critério **suave**: nunca passa por cima de uma relação ou área pedida pelo usuário.
4. **Implantação previsível.** Por padrão, a casa encosta no **recuo frontal** (o quintal fica no fundo) e fica **centralizada na largura** do lote. **[decisão do Agente]**
5. **Lote pequeno: encostar na divisa.** Sem `attached_sides` no pedido, se o programa não couber com os afastamentos laterais e de fundo, o gerador tenta de novo permitindo encostar: uma lateral, depois as duas, depois o fundo. A escolha aparece como **aviso**. Lado a menos de 1,5 m da divisa fica marcado **"sem janela"** (Código Civil, art. 1.301), regra que o M4 vai aplicar às aberturas. Com interface (M2), isso vira a pergunta de implantação da seção 6.2.
6. **Muro.** Todo o perímetro do lote recebe muro (frente, fundos e laterais), por dentro da divisa, com espessura padrão de 150 mm **[decisão do Agente; valor a confirmar numa trilha de dados]**. Layer DXF novo: `A-MURO`. O portão entra com as aberturas (M4).
7. **Áreas externas e cores.** Toda área do lote vira uma de **4 categorias**, com uma cor cada (DXF por layer, SVG e interface):
   - **interna seca** (salas, quartos, closet, circulação, escritório…);
   - **interna molhada** (banheiro, lavabo, cozinha, lavanderia), útil para a hidráulica;
   - **externa construída** (varanda, garagem, área gourmet, calçadas, pátio);
   - **externa verde** (quintal, jardim, o que sobra dentro do muro).

   A zona (social, íntima, serviço) continua aparecendo no grafo de bolhas, não na cor da planta.
8. **Permeabilidade.** Aviso quando a área verde ficar abaixo de 25% do lote. É a referência mais comum da D1 (Curitiba, ZR); a lei local manda.

### 20.2 M1.2 — Dimensionamento pelo mobiliário

Conclusão da D1, aceita pelo responsável: **a área mínima de um cômodo é consequência do mobiliário mínimo mais as circulações.**

1. **Trilha D2 (dados):** mobiliário mínimo por tipo de cômodo (cama, guarda-roupa, sofá, mesa, pia, fogão, geladeira, louças, tanque, lavadora) e as folgas de uso. Fontes: anexo da NBR 15575-1, MCMV e fabricantes, registradas em `data/furniture.yaml`, com fonte por valor.
2. **Verificação "cabe?":** para cada cômodo, um pequeno empacotamento (CP-SAT) testa se o mobiliário mínimo com as folgas cabe no retângulo útil e se sobra uma faixa de passagem até a porta. Ela roda como validação de cada alternativa e **deriva a largura e a área mínimas** de cada tipo.
3. **Perfis de mínimo.** As fontes divergem, e isso não é problema: o usuário escolhe o perfil.
   - **conservador** (padrão): o maior mínimo entre as fontes;
   - **mediana**: a mediana das fontes;
   - **personalizado**: o valor que o usuário informar.

   O objetivo é o gerador nunca propor um cômodo em que o que foi pedido não cabe, **sem** precisar de dezenas de perguntas.
4. **Itens pedidos** ("mesa para 6", "cama king", "pia de 2 m"): entram no conjunto de mobiliário daquele cômodo e aumentam os mínimos dele. É o pré-dimensionamento da seção 6.3, antecipado do M6.

Ordem: **M1.1 → M1.2 → M2.** A interface só deve mostrar plantas que já pareçam plantas.
