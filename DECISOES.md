# DECISOES.md — Registro cronológico do projeto

> **Append-only.** Nunca apagar nem reescrever entradas. Para substituir uma decisão, criar uma nova que referencie a anterior.
> Cada decisão tem identificador, data, sessão, autor, categoria, contexto, decisão, justificativa, consequências e status.
> Autores: **Responsável** (dono do projeto) · **Agente** (Claude Code).

---

## Sessão S01 — 2026-11-10

### Log da sessão (prompts e ações, em resumo)

1. **Responsável:** pediu a instalação do plugin `superpowers`. **Agente:** instalou `superpowers@claude-plugins-official` (escopo de usuário) pela linha de comando, porque `/plugin` não está disponível na extensão do VS Code.
2. **Responsável:** perguntou como usar o superpowers no VS Code. **Agente:** explicou as skills disponíveis.
3. **Responsável:** pediu um brainstorm a partir do `IDEIA.md`: entrevista com uma pergunta por vez sobre objetivo, escopo do MVP, motor de regras e cálculo espacial, e pipeline de saída CAD. Esclareceu que o `IDEIA.md` era um prompt gerado pelo GPT depois de uma conversa breve, e que outros caminhos podiam ser explorados.
4. **Responsável:** definiu a natureza do projeto (portfólio e estudo; ver DEC-0001) e o critério de sucesso: versatilidade para interpretar pedidos com campos fixos, opcionais e texto livre, gerando alternativas de forma gradual e interativa.
5. **Responsável:** adicionou o hábito dos três arquivos de governança, a interface rápida com respostas por clique, a visualização ao vivo e o console estilo AutoCAD.
6. **Responsável:** restringiu o MVP ao essencial e ao 2D, pediu uma IA offline sem API paga, perguntou sobre Claude + AutoCAD, MCP e métodos de otimização. **Agente:** apresentou as opções e as recomendações.
7. **Responsável:** escolheu o caminho híbrido de IA, o DXF via ezdxf, as 4 camadas e os múltiplos métodos de geração. Perguntou sobre linguagens para um app desktop e sobre MCP.
8. **Responsável:** escolheu o app web local em Python + HTML/CSS/TypeScript, exigiu um front-end de qualidade (não um "dashboard") e pediu as skills de interface.
9. **Responsável:** pediu a instalação de `frontend-design` e `playwright`, o registro dos demais plugins para depois, o preenchimento mínimo de README e CLAUDE, o início deste registro e a exclusão do `IDEIA.md`. Definiu a direção visual (DEC-0013). **Agente:** executou tudo isso.

### Decisões

**DEC-0001 — Natureza e objetivo do projeto**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Escopo
Contexto: o `IDEIA.md` partia da construção da casa do próprio responsável.
Decisão: o projeto é de **portfólio e estudo** (desenvolvimento de software, geometria, estatística, IA, modelagem e otimização) e algo de que o responsável quer se orgulhar. Não é uma ferramenta para a casa própria. Virar produto com usuários reais é uma possibilidade futura, não o objetivo.
Critério de sucesso: **versatilidade**, ou seja, interpretar pedidos que misturam campos fixos, opcionais e texto livre e gerar plantas de qualidade, boas o bastante para um arquiteto ou engenheiro usar como ponto de partida.
Primeiro usuário: o próprio responsável.
Status: Aprovada.

**DEC-0002 — Arquivos de governança**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Processo
Decisão: o projeto mantém pelo menos três arquivos. **CLAUDE.md** traz as regras de conduta do agente. **README.md** é a vitrine no GitHub, com o resumo, a estrutura e os requisitos. **DECISOES.md** é append-only e cronológico, com todos os prompts e decisões do responsável e todas as decisões, sugestões, alterações e construções do agente.
Consequências: toda mudança no projeto gera um registro aqui.
Status: Aprovada.

**DEC-0003 — Escopo inicial: somente 2D**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Escopo
Decisão: o app inicial gera **apenas a planta baixa 2D**, com construção ao vivo e visão fixa de cima. O 3D (inclusive a visualização ao vivo com câmera), as cores de parede, a arborização e as plantas elétrica e hidráulica são fases posteriores. O motor 2D deve ser projetado para se encaixar nelas.
Justificativa: construir aos poucos, com algo funcional e "sem rodeios".
Status: Aprovada.

**DEC-0004 — App offline e independente**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Arquitetura
Decisão: o app funciona **offline**, sem depender do Claude Code nem da API da Anthropic, por causa do custo. Uma API paga pode ser plugada no futuro como opção, nunca como requisito.
Status: Aprovada.

**DEC-0005 — Interpretação de texto: abordagem híbrida**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável (proposta do Agente) · Categoria: IA
Decisão: um **parser de regras** cuida do que é estruturado (números, cômodos, palavras-chave) e um **LLM pequeno local** (via llama.cpp/Ollama ou similar) cuida do texto livre. Os dois preenchem um **JSON de schema fixo**, que é validado antes de chegar ao motor. O LLM **nunca desenha nem define coordenadas**.
Justificativa: funciona mesmo sem o LLM, é previsível e testável. Um modelo pequeno basta, porque ele só traduz o pedido.
Consequências: modelo e velocidade precisam ser validados com um teste no hardware de desenvolvimento (i5-1335U, 8 GB RAM). A arquitetura deixa o provedor de LLM substituível.
Status: Aprovada (modelo específico a definir).

**DEC-0006 — Entrada em três camadas**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto
Decisão: as entradas se dividem em **essenciais e fixas** (terreno, número de cômodos, pavimentos), **opcionais** (áreas, formato, garagem…) e **texto livre** (ex.: "oficina longe dos quartos por causa do barulho", "varal com sol", "janelas para o leste", "evitar corredores"). Preferências não viram restrições rígidas automaticamente.
Status: Aprovada.

**DEC-0007 — Construção gradual e interativa**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto
Decisão: a planta é construída **por etapas visíveis e aprováveis**. O app abre com uma malha infinita (como o fundo do AutoCAD). Cada resposta atualiza o desenho: por exemplo, ao definir o terreno de 25×10 m, o contorno aparece e a tela centraliza nele. Ao definir os cômodos, o app mostra possibilidades que o usuário navega e escolhe. As etapas simples se resolvem com um clique ("aceitar" ou "especificar diferente").
Sequência proposta pelo Agente: zonas → blocos → cômodos → paredes → aberturas.
Status: Aprovada (sequência exata a detalhar).

**DEC-0008 — Saída CAD: Python + ezdxf gerando DXF**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável (proposta do Agente) · Categoria: Arquitetura
Decisão: a exportação é em **DXF via ezdxf**, offline, sem exigir o AutoCAD instalado, com layers organizados.
Alternativas descartadas por ora: automatizar o AutoCAD por dentro (AutoLISP, .scr, .NET, COM), que prende o app a um software pago, e o Autodesk Platform Services, que é pago e online.
Registro para o futuro (fase 3D/BIM): **Revit** (API em C#, pyRevit, Dynamo) e **IFC** (IfcOpenShell), este como caminho aberto.
Status: Aprovada.

**DEC-0009 — Arquitetura do motor em 4 camadas**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável (proposta do Agente) · Categoria: Arquitetura
Decisão:
1. **Topologia:** grafo de ambientes e relações com pesos, e zonas social, íntima e de serviço (candidata: NetworkX).
2. **Geometria:** otimização por restrições em grade modular (candidata: OR-Tools CP-SAT), com cômodos sem sobreposição, contidos no terreno, com dimensões mínimas e adjacência medida como parede compartilhada.
3. **Alternativas:** variação de pesos e topologia. No futuro, otimização multiobjetivo e Pareto (candidata: pymoo/NSGA-II).
4. **Estatística:** calibração de pesos, medida de diversidade e, no futuro, aprendizado das preferências pelas escolhas do usuário (ex.: Bradley-Terry).
Consequências: as bibliotecas são candidatas e entram somente após testes que justifiquem cada dependência.
Status: Aprovada.

**DEC-0010 — Múltiplos métodos de geração comparáveis**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto / Arquitetura
Decisão: haverá vários geradores com uma **interface comum**, produzindo o mesmo modelo de planta e avaliados pela mesma pontuação: (1) árvore de subdivisão, (2) crescimento em grade, (3) otimização por restrições (CP-SAT) e (4) recozimento simulado (o quarto método foi proposto pelo Agente). A comparação deve ser visual (a construção) e de resultado (as plantas), como um benchmark justo.
Consequências: o MVP nasce com um ou dois geradores e os demais entram depois, sem refatoração. Quais vêm primeiro ainda está pendente.
Status: Aprovada.

**DEC-0011 — Stack: app web local**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Arquitetura
Decisão: é um **app web local e offline**. O motor fica em **Python** e a interface em **HTML/CSS/TypeScript**, rodando no navegador do próprio computador.
Propostas do Agente, a confirmar: servidor local em FastAPI e, no futuro, um instalador via Tauri. Electron foi descartado pelo consumo de RAM. PySide6 e C#/.NET foram considerados e não escolhidos.
Status: Aprovada (bibliotecas a confirmar).

**DEC-0012 — Motor como conjunto de comandos e MCP**
Data: 2026-11-10 · Sessão: S01 · Autor: Agente (aceito pelo Responsável) · Categoria: Arquitetura
Decisão: o motor expõe suas operações como **comandos**, os mesmos que aparecem no console estilo AutoCAD. Esses comandos servem à interface, ao LLM local e, no futuro, a um **servidor MCP** (Model Context Protocol, um padrão para assistentes de IA usarem ferramentas de outros programas).
Plano: uma versão **básica e funcional durante o desenvolvimento**, para o Claude Code e o Cowork testarem o motor, e uma versão **aprofundada no fim do projeto**, como contribuição para a comunidade.
Status: Aprovada.

**DEC-0013 — Direção visual da interface**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Interface
Decisão:
- O tema é escuro, inspirado no modo escuro do AutoCAD, porém **muito mais simples e rápido** (sem excesso de botões nem navegação lenta).
- A **planta ocupa cerca de 90% da tela**. Perguntas, console e botões ficam numa lateral ou aparecem sobre a tela quando necessários.
- A paleta é preto, cinzas, branco, **laranja** (próxima do visual do Claude) e **roxo**.
- Uma faixa superior estreita traz as opções gerais: novo, abrir, salvar, excluir projeto e abas.
- O front-end é tratado como produto: animado, interativo e com movimento com propósito, nunca com cara de dashboard.
- Há um console que mostra em tempo real os comandos executados pelo motor, com histórico.
Status: Aprovada (detalhes a prototipar).

**DEC-0014 — Plugins de desenvolvimento**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Ferramentas
Decisão: foram instalados no escopo de usuário `superpowers`, `frontend-design` e `playwright`, todos do marketplace `claude-plugins-official`. Ficam registrados para as etapas futuras `modern-web-guidance` (na fase de interface) e `mcp-server-dev` (na fase MCP).
Observação do Agente: o **Node.js não está instalado** nesta máquina. Ele é necessário para o servidor MCP do playwright e para compilar o TypeScript. Python 3.13 e Git 2.55 estão presentes.
Status: Aprovada.

**DEC-0015 — Exclusão do IDEIA.md e itens herdados**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Processo
Decisão: o `IDEIA.md` foi excluído a pedido do responsável. Era um prompt gerado pelo GPT a partir de uma conversa breve, e as ideias foram absorvidas pelo brainstorm desta sessão.
Itens do IDEIA.md **ainda não discutidos**, preservados aqui como referência e **pendentes de validação**:
- unidade interna em milímetros, com exibição em m/cm e grade de snap independente da precisão;
- convenção de layers `A-PAREDES-EXT`, `A-PAREDES-INT`, `A-PORTAS`, `A-JANELAS`, `A-MOBILIARIO`, `A-COTAS`, `A-TEXTOS`, `A-HACHURAS`, `A-TERRENO`, `A-AREAS`, `A-CIRCULACAO`, `A-ESTRUTURA`, `A-VEGETACAO`;
- modelo central com entidades de ID único (Project, Site, Floor, Room, Wall, Door, Window, Furniture…) e histórico de versões;
- separação entre topologia e geometria, com retângulos `(x, y, w, h)` como simplificação inicial;
- distinção entre área mínima, desejada e máxima;
- normas brasileiras e legislação municipal como evolução futura, sem afirmar conformidade sem verificação;
- roadmap de referência V0–V10 (estrutura → motor 2D → aberturas → mobiliário → editor → agente → otimização → 3D → paisagismo → complementares → produto);
- concorrentes de referência: Maket, Planner 5D, Floorplanner, Homestyler;
- a pasta ainda não é um repositório git.
Status: Aprovada.

### Pendências abertas (S01)

- Nome do projeto.
- Escopo exato do MVP: tipo de casa, onde a planta "termina", quais geradores entram primeiro.
- Regras de qualidade da planta: o que torna uma planta "boa", fonte das dimensões mínimas, circulação.
- Retrato detalhado da interface.
- Documento de design, revisão e aprovação, seguidos do plano de implementação.
- Inicializar o git (com autorização).
- Instalar o Node.js.

### Log da sessão — continuação

10. **Responsável:** aprovou a estrutura do DECISOES.md e pediu que ela vire regra no CLAUDE.md. Pediu a instalação do Node.js pelo terminal. Disse que vai inicializar o git depois de definir o nome do projeto. Descreveu o pipeline de construção com retrocesso entre etapas (DEC-0017). **Agente:** adicionou ao CLAUDE.md a regra e o modelo da estrutura (DEC-0016) e instalou o Node.js 26.13.0 LTS (npm 11.20.0) via `winget install OpenJS.NodeJS.LTS`.

### Decisões — continuação

**DEC-0016 — Estrutura obrigatória do DECISOES.md**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Processo
Decisão: a estrutura usada na S01 (log da sessão, decisões `DEC-NNNN` com campos padronizados e pendências) passa a ser regra permanente, documentada no CLAUDE.md. O registro é feito sempre, ao fim de cada rodada.
Status: Aprovada.

**DEC-0017 — Pipeline de construção em etapas com retrocesso**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Escopo / Arquitetura
Decisão: a planta é construída em etapas sucessivas, e **cada etapa pode devolver o problema a etapas anteriores** quando encontra uma solução melhor ou quando a solução atual é inviável:
1. **Cômodos, paredes e linhas de demarcação.** É a etapa principal de otimização: dimensões e disposição, considerando relações entre ambientes e orientação cardinal.
2. **Portas e janelas.** Agora é possível avaliar iluminação, ventilação, circulação e relações entre ambientes, além das restrições interpretadas pelo LLM ("x longe de y", "z integrado com w"). Pode alterar a etapa 1.
3. **Mobiliário simplificado** (retângulos e formas circulares aproximadas, como louças sanitárias), com prioridade para a **mobília fixa** (pia, fogão, ilha, armário planejado) e os itens pedidos pelo usuário (ex.: "pia de x metros lineares", "mesa para N pessoas"). Verifica se cada cômodo comporta o que foi pedido e pode alterar as etapas 1 e 2.
O "fim" da planta no MVP **não é fixado agora**. O responsável vai decidir ao longo do desenvolvimento até onde basta. A arquitetura deve permitir acrescentar etapas.
Status: Aprovada (ponto final do MVP a definir).

### Pendências abertas (S01) — atualização

- Git a inicializar pelo responsável depois de definir o nome do projeto. O Node.js já foi instalado.
- Validar o retrato do pipeline com retrocesso (playback do Agente).

### Log da sessão — continuação 2

11. **Responsável:** aprovou as três etapas e transformou em decisão as quatro propostas do Agente: antecipar, voltar com motivo, limite de voltas e retrocesso visível. Pediu que fossem aprofundadas. Reforçou que o projeto deve ser muito visual e interativo. Pediu um **grafo de relações em miniatura** num canto da tela e esclareceu que cada etapa tem **várias soluções** que o usuário pode escolher. **Agente:** registrou DEC-0018 a DEC-0023 e aprofundou as propostas.

### Decisões — continuação 2

**DEC-0018 — Antecipação de requisitos (pré-dimensionamento)**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável (proposta do Agente) · Categoria: Arquitetura
Decisão: antes da etapa 1, cada item pedido (mobília fixa, "mesa para N pessoas", "pia de x m lineares", ilha) é convertido, por meio de uma **biblioteca de itens com dimensões e folgas de uso e circulação**, em **dimensões mínimas** (largura, comprimento, área) do cômodo. Esses mínimos entram como restrições desde o início, e voltar etapas passa a ser exceção.
Detalhes propostos pelo Agente: cada mínimo guarda sua **origem** (ex.: "largura mínima da cozinha = 3,20 m por causa da ilha 1,2 × 0,9 m + 2 × 0,9 m de circulação + bancada 0,6 m"), para o usuário ver o porquê. As fontes de referência das dimensões, como Neufert e a lista de mobiliário mínimo da NBR 15575, ainda precisam ser confirmadas, com origem e versão registradas.
Status: Aprovada.

**DEC-0019 — Retrocesso com motivo concreto (restrições aprendidas)**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável (proposta do Agente) · Categoria: Arquitetura
Decisão: quando uma etapa devolve o problema a uma anterior, ela envia um **motivo estruturado** (etapa de origem, elemento afetado, tipo, valor e explicação; ex.: `cozinha.largura >= 3.20 m — ilha não cabe`). O motivo vira uma **nova restrição** na etapa anterior, que assim não repete o erro (inspiração: decomposição de Benders e cortes do tipo "no-good").
Detalhes propostos pelo Agente: as restrições aprendidas se acumulam num **caderno de restrições** visível ao usuário, que pode inspecioná-las e removê-las. Cada uma é marcada como **rígida** (inviável sem ela) ou **suave** (melhora a nota).
Status: Aprovada.

**DEC-0020 — Limite de voltas e negociação com o usuário**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável (proposta do Agente) · Categoria: Arquitetura / Produto
Decisão: cada etapa tem um **orçamento de tentativas** e um **limite de tempo**. Ao estourar, ou ao detectar um ciclo (o mesmo estado repetido), o sistema para e **pergunta ao usuário o que ceder**, mostrando as opções com o custo de cada uma (ex.: "ilha 20% menor" vs. "sala de estar −2 m²" vs. "aumentar a área construída").
Detalhes propostos pelo Agente: o solver sempre devolve a **melhor solução encontrada até o momento**, para a interface nunca travar. Os limites são configuráveis.
Status: Aprovada.

**DEC-0021 — Retrocesso e decisões visíveis (explicabilidade)**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável (proposta do Agente) · Categoria: Interface
Decisão: todo retrocesso aparece **no console** (ex.: `↩ etapa 1: cozinha não comporta a ilha`) e **na planta**, com transição animada da versão anterior (em "fantasma") para a nova.
Detalhes propostos pelo Agente: cada decisão do motor tem um **"por quê?"** consultável (as restrições e os pesos que a determinaram). Há também uma linha do tempo das etapas com as voltas marcadas.
Status: Aprovada.

**DEC-0022 — Grafo de relações em miniatura (diagrama de bolhas ao vivo)**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Interface / Produto
Decisão: um **grafo de relações entre cômodos** fica exibido em tamanho reduzido num canto da tela. Ele aparece assim que os cômodos são definidos, com **nós retangulares** próximos entre si, como um primeiro esboço da planta. As restrições e preferências do usuário (cozinha integrada à sala, suíte perto da entrada, banheiro perto dos quartos, oficina longe dos dormitórios) **ajustam ao vivo os pesos** das ligações e dos nós, exibidos em números.
Justificativa: mostra a lógica interna do sistema, no estilo das visualizações de backend, redes neurais e estruturas de dados, nas etapas iniciais, quando o usuário define as premissas e o motor gera as soluções.
Detalhes propostos pelo Agente:
- é o equivalente computacional do **diagrama de bolhas / organograma funcional** usado por arquitetos;
- nós com tamanho proporcional à área e cor por zona (social, íntima, serviço);
- ligações de atração e de repulsão com estilos diferentes;
- posicionamento por simulação de forças, para que os pesos "puxem" e "empurrem" os nós de forma animada.
Status: Aprovada (visual a prototipar).

**DEC-0023 — Árvore de alternativas por etapa**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto / Arquitetura
Decisão: **cada etapa gera várias soluções**, não uma só. O usuário escolhe uma, e a etapa seguinte gera novas soluções a partir dela e das novas respostas e preferências. Ele pode voltar e escolher outra opção de uma etapa anterior.
Detalhes propostos pelo Agente:
- o projeto é modelado como uma **árvore de estados** (como os ramos do git), o que dá de graça o histórico, o desfazer/refazer e a comparação de alternativas;
- só o ramo escolhido é expandido (geração sob demanda);
- cada etapa oferece poucas opções (ordem de 3 a 5), escolhidas para serem **diferentes entre si**, com uma métrica estatística de diversidade, e não variações quase iguais;
- a árvore pode ter sua própria visualização compacta.
Status: Aprovada (número de opções a definir).

### Log da sessão — continuação 3

12. **Responsável:** confirmou as quatro propostas. Pediu uma biblioteca de conhecimento sobre medidas e tamanhos de objetos escolhíveis pelo usuário. Comparou o excesso de restrições a overfitting. Detalhou o console em formato de chat e o ciclo de vida do grafo de bolhas. Perguntou se é preciso processar todos os ramos da árvore. **Agente:** registrou DEC-0024 a DEC-0028 e respondeu que não: a expansão é sob demanda.

### Decisões — continuação 3

**DEC-0024 — Biblioteca de conhecimento de medidas**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Dados / Arquitetura
Decisão: haverá uma biblioteca (pasta de dados e referências) com medidas de móveis, eletrodomésticos, louças, cômodos e folgas de uso, reunida a partir de literatura, artigos, padrões, normas, convenções de mercado e senso comum de projeto. É a base do pré-dimensionamento (DEC-0018).
Detalhes propostos pelo Agente:
- dados estruturados (ex.: JSON/YAML) com **fonte, versão e data de cada valor**;
- normas pagas (ABNT/NBR) e livros protegidos **não** são copiados para o repositório público; guardamos apenas os valores extraídos, com a citação.
Status: Aprovada.

**DEC-0025 — Tamanhos de objetos escolhíveis pelo usuário**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto
Decisão: cada objeto da biblioteca oferece **presets de tamanho** (ex.: geladeira pequena, média, grande, enorme ≈ 1 × 1 m) e a opção de **medida personalizada**. A escolha alimenta o pré-dimensionamento.
Status: Aprovada (presets por objeto a definir).

**DEC-0026 — Excesso de restrições como sinal de solução ruim**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Arquitetura
Decisão: o limite de voltas (DEC-0020) existe também para impedir que o motor acumule restrições aprendidas até chegar a uma solução tecnicamente viável, porém ruim na prática. Ao atingir o limite, entra o **script de negociação** com o usuário.
Nota do Agente: o responsável comparou isso a overfitting. Tecnicamente, o fenômeno é **superrestrição** (acúmulo de restrições que empurra a busca para cantos estranhos do espaço de soluções), e não overfitting, que é um conceito de modelos aprendidos a partir de dados. O efeito prático descrito (uma solução "válida" porém ruim) e o remédio (limitar e negociar) estão corretos. A métrica proposta é o número de restrições aprendidas, além da nota da solução: se a nota cair abaixo de um piso, o sistema também negocia.
Status: Aprovada.

**DEC-0027 — Console como linha do tempo em formato de chat**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Interface
Decisão: o console mostra **tudo** o que é executado: comandos, avanço de etapa, retrocesso e o porquê. O formato é de chat, em linha do tempo, com as entradas antigas subindo e saindo por cima (com scroll para rever).
Status: Aprovada.

**DEC-0028 — Ciclo de vida do grafo de bolhas**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Interface
Decisão: o grafo de relações **surge grande no centro da tela** (ou levemente deslocado), onde a planta vai nascer, e é construído com **animação de forças com inércia** conforme o usuário responde. Depois das perguntas mínimas, quando os primeiros esboços de planta aparecem, o grafo **encolhe e vai para um canto**, perto do painel de perguntas, dos campos fixos e do console. Complementa a DEC-0022.
Status: Aprovada.

Resposta registrada (expansão da árvore, ver DEC-0023): não é preciso processar todos os ramos. Somente o ramo escolhido é expandido. As opções irmãs ficam guardadas como "não expandidas" e só são calculadas se o usuário voltar a elas. O custo é cerca de K soluções por etapa visitada, e não K^(número de etapas). Uma otimização opcional proposta pelo Agente é pré-calcular em segundo plano a etapa seguinte da opção mais provável, para dar sensação de instantâneo.

### Log da sessão — continuação 4

13. **Responsável:** definiu que "planta boa" é o que **o usuário** define por botões e chat, havendo apenas um conjunto de premissas mínimas universais (circulação adequada, garagem dimensionada para N veículos…). Esse é o diferencial do produto. **Agente:** registrou DEC-0029 e propôs a avaliação em três camadas (DEC-0030), aguardando confirmação.

### Decisões — continuação 4

**DEC-0029 — "Planta boa" é definida pelo usuário (diferencial do produto)**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto
Decisão: a qualidade de uma planta é definida pelas preferências e restrições de **cada usuário**, inseridas por botões, campos fixos e chat (ex.: sem quintal, quintal grande, varanda perto do jardim, piscina com área de lazer ao lado da cozinha com porta de vidro, oficina grande, muita luz natural). Existe apenas um **piso de premissas mínimas universais** que nenhuma preferência anula (ex.: circulação adequada na cozinha, garagem com dimensões corretas para N veículos).
Justificativa: é o diferencial, ou seja, permitir que qualquer pessoa projete uma planta **adequada** seguindo os próprios gostos.
Status: Aprovada.

**DEC-0030 — Avaliação em três camadas (proposta)**
Data: 2026-11-10 · Sessão: S01 · Autor: Agente · Categoria: Arquitetura
Decisão proposta:
1. **Piso técnico (restrições rígidas e universais):** sem sobreposição; tudo dentro do terreno e dos recuos; dimensões e áreas mínimas; folgas de circulação; todo cômodo acessível pela circulação; garagem dimensionada. Uma planta que viola o piso é descartada, nunca pontuada.
2. **Objetivos do usuário (nota principal):** cada preferência vira um critério com peso definido pelo usuário (botões e chat).
3. **Boas práticas padrão (peso baixo, desligáveis):** aplicadas apenas quando o usuário não se manifestou (ex.: pouca área desperdiçada em corredores, forma compacta, áreas molhadas agrupadas). Qualquer preferência explícita do usuário prevalece.
A nota é exibida **decomposta por critério**, para o usuário ver por que uma alternativa ganha de outra.
Status: Substituída por DEC-0031 a DEC-0034.

### Log da sessão — continuação 5

14. **Responsável:** ajustou a DEC-0030. O piso técnico deve ser **negociável** com ciência do usuário (ex.: garagem menor que a norma, mas utilizável). Os pesos vêm do LLM, de botões sim/não, de aspectos correlatos inferidos e de **notas dadas pelo próprio usuário** (positivas, neutras ou negativas), num formato de quiz ou entrevista, que exige estudo a fundo. As boas práticas são o padrão: área verde mínima, corredores sempre minimizados, banheiros próximos quando possível. A comparação entre alternativas precisa captar **interações entre critérios** (+1 e +1 podem valer mais ou menos que 2). **Agente:** registrou DEC-0031 a DEC-0034, substituindo a DEC-0030.

### Decisões — continuação 5

**DEC-0031 — Piso técnico em dois níveis: validade geométrica vs. recomendações negociáveis**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável (refinamento proposto pelo Agente) · Categoria: Arquitetura / Produto
Substitui: DEC-0030 (item 1).
Decisão:
- **Validade geométrica (inegociável):** sem sobreposição, dentro do terreno, paredes consistentes, todo cômodo alcançável. Sem isso o resultado não é uma planta.
- **Recomendações normativas e de boa prática (negociáveis):** dimensões mínimas, folgas de circulação, garagem por veículo, recuos etc. O usuário **pode passar por cima de forma consciente** (ex.: garagem apertada, mas utilizável).
Detalhes propostos pelo Agente:
- toda violação aceita fica **sinalizada** na planta, com um alerta visível e o valor recomendado vs. o adotado;
- ela é registrada no histórico do projeto, como um "termo de ciência";
- pode constar no DXF (layer ou nota de observações);
- o motor nunca viola uma recomendação por conta própria, apenas propõe a violação durante a negociação (DEC-0020).
Status: Aprovada.

**DEC-0032 — Obtenção dos pesos das preferências (estudo a fundo)**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto / IA / Estatística
Substitui: DEC-0030 (item 2).
Decisão: os pesos dos objetivos do usuário vêm de quatro fontes combinadas:
1. interpretação do texto livre pelo LLM local;
2. botões fixos (sim/não);
3. **aspectos correlatos inferidos** (ex.: "piscina" → lazer, área externa, sol);
4. **notas dadas pelo próprio usuário** numa escala com valores positivos, neutros e negativos ("quanto você valoriza iluminação, circulação, ventilação, lazer, quarto grande, cozinha com muitos armários…"), num formato de quiz ou entrevista.
Quais perguntas fazer, em que ordem e com qual escala ainda precisa de **estudo a fundo**.
Métodos a estudar, propostos pelo Agente:
- escala tipo Likert bipolar (ex.: −2 a +2);
- AHP (comparações par a par);
- análise conjunta, ou *conjoint* (escolher entre duas opções e inferir pesos);
- **aprendizado por escolhas** (Bradley-Terry): cada alternativa que o usuário escolhe refina os pesos.
Hipótese inicial do Agente: notas rápidas no começo, refinadas pelas escolhas ao longo da árvore.
Status: Aprovada (método a estudar).

**DEC-0033 — Boas práticas como padrão**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto
Substitui: DEC-0030 (item 3).
Decisão: as boas práticas valem como **padrão** quando o usuário não se manifestou. Exemplos:
- área verde mínima (nem ausente, nem grande) quando o quintal não foi mencionado;
- **minimizar sempre a área de corredores**, considerada perdida, mesmo quando o usuário pede corredores específicos (cumpre-se o pedido com a menor área possível);
- agrupar áreas molhadas (banheiros, cozinha, lavanderia) quando for viável, para simplificar a hidráulica.
A lista completa será construída junto com a biblioteca de conhecimento (DEC-0024).
Status: Aprovada.

**DEC-0034 — Agregação com interação entre critérios (estudo a fundo)**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Arquitetura / Estatística
Substitui: DEC-0030 (nota única por soma).
Decisão: a comparação entre alternativas **não** é uma soma simples de pontos por critério. Os critérios podem ser atendidos em graus intermediários, e critérios relacionados **interagem**: ganhos simultâneos podem valer mais (sinergia) ou menos (redundância) que a soma.
Métodos a estudar, propostos pelo Agente:
- **utilidade com retornos decrescentes** por critério (o 10º m² de quintal vale menos que o 1º);
- **integral de Choquet**, um agregador multicritério que modela sinergia e redundância entre pares de critérios;
- **fronteira de Pareto**, para mostrar os compromissos reais em vez de forçar uma nota única.
A exibição decomposta por critério continua.
Status: Aprovada (método a estudar).

### Log da sessão — continuação 6

15. **Responsável:** detalhou a validade geométrica inegociável (sem sobreposição de paredes ou móveis, nada fora do terreno, todo cômodo alcançável com porta, nenhum cômodo "em cima do telhado"). Confirmou que as recomendações podem ser furadas com plena sinalização. Pediu estilos de pergunta combinados conforme a etapa, para evitar monotonia: escalas bipolares para a matriz inicial de pesos, AHP e A-vs-B para refinar. Perguntou se, no A-vs-B, convém mostrar os ganhos e as perdas. Pediu uma pasta de fundamentação teórica. **Agente:** registrou DEC-0035 a DEC-0038 e respondeu sobre o A-vs-B (DEC-0037, proposta).

### Decisões — continuação 6

**DEC-0035 — Validade geométrica: a verdade inegociável**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Arquitetura
Complementa: DEC-0031.
Decisão: nenhuma solução, nem por escolha do usuário, pode violar:
- sobreposição de paredes, móveis ou quaisquer elementos;
- elementos fora dos limites do terreno definido;
- cômodo inalcançável: todo cômodo tem pelo menos uma porta e um caminho até a entrada;
- incoerência vertical (pensando no 3D futuro): nenhum cômodo "em cima do telhado" ou sem apoio; todo elemento de pavimento superior deve estar sobre estrutura ou pavimento válido.
As **recomendações dimensionais e normativas** continuam negociáveis com **plena sinalização** (DEC-0031).
Status: Aprovada.

**DEC-0036 — Estilos de pergunta combinados por etapa**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto
Decisão: os formatos de pergunta variam conforme a etapa da planta e para evitar monotonia:
- **escalas bipolares** (positivo, neutro, negativo) para montar a **matriz inicial de pesos** das características;
- **AHP** e **escolha A vs. B**, mais precisos, quando o algoritmo precisa calibrar duas ou mais características em conflito, o que conecta com a fronteira de Pareto (DEC-0034). Escolher entre alternativas é a forma natural de o usuário indicar seu ponto de equilíbrio;
- botões sim/não e chat livre continuam disponíveis.
Status: Aprovada.

**DEC-0037 — Informação exibida na escolha A vs. B (proposta)**
Data: 2026-11-10 · Sessão: S01 · Autor: Agente · Categoria: Produto / Estatística
Contexto: o responsável perguntou se é melhor mostrar os ganhos e as perdas de cada opção ou deixar o usuário escolher sem informação extra.
Proposta:
- mostrar **as duas plantas** mais um **resumo curto e simétrico** das diferenças (ex.: "A: + luz nos quartos, − quintal · B: + quintal, − luz nos quartos"), em linguagem natural e com barras pequenas em vez de números crus;
- detalhes completos sob demanda ("ver detalhes").
Justificativa:
- escolher às cegas gera escolhas ruidosas, pela imagem e não pelo que importa, e pesos mal estimados;
- números crus e enquadramentos assimétricos ("A perde 5 pontos") induzem viés, por efeito de enquadramento e ancoragem;
- a apresentação simétrica por atributos é o padrão da análise conjunta (*choice-based conjoint*) e mantém a escolha informativa para o aprendizado de pesos.
Status: Proposta (aguardando o responsável).

**DEC-0038 — Pasta de conhecimento e fundamentação teórica**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Processo / Dados
Amplia: DEC-0024.
Decisão: o projeto terá uma pasta de **conhecimento e referência** que vai além das medidas: artigos, material de pesquisa, teoria e dados sobre arquitetura, engenharia, otimização, estatística, decisão multicritério e tecnologias usadas. A agregação com interação entre critérios (DEC-0034) e a obtenção de pesos (DEC-0032) serão fundamentadas ali antes de serem implementadas.
Detalhes propostos pelo Agente:
- cada tema tem uma nota de síntese própria (o que é, por que importa para o projeto, fórmulas, exemplo, referências);
- PDFs protegidos não entram no repositório público, apenas a citação.
Estrutura a definir no documento de design.
Status: Aprovada.

### Log da sessão — continuação 7

16. **Responsável:** aprovou a DEC-0037. **Agente:** registrou a DEC-0039 e passou ao retrato da interface.

### Decisões — continuação 7

**DEC-0039 — Aprovação do formato A vs. B**
Data: 2026-11-10 · Sessão: S01 · Autor: Responsável · Categoria: Produto
Decisão: fica aprovada a proposta DEC-0037: duas plantas lado a lado, um resumo curto e simétrico das diferenças em linguagem natural com barras, e detalhes sob demanda.
Status: Aprovada.

---

## Sessão S02 — 2026-11-11

### Log da sessão (prompts e ações, em resumo)

1. **Responsável:** viu os três mockups de layout da S01 (A: painel lateral; B: ilhas flutuantes; C: linha de comando estilo AutoCAD) e aprovou o padrão visual dos três. Escolheu uma combinação (DEC-0040). Informou que a aba do navegador fechou e o link não abria mais. **Agente:** religou o servidor de mockups, montou o mockup `layout-v2.html` com a combinação em três momentos (início com o grafo grande, etapa 1 e escolha A vs. B) e registrou a DEC-0040.

### Decisões

**DEC-0040 — Layout da tela principal: combinação A + C**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Interface
Contexto: comparação dos mockups A, B e C. O responsável achou a planta pequena demais na A e grande demais na B (embora a B fosse melhor que a A). Achou também que as ilhas flutuantes da B atrapalham a visão da planta.
Decisão:
- **tamanho da planta na tela** na proporção da opção C (meio-termo);
- **painel lateral fixo** à direita, como na A, com o grafo de relações e o console;
- **perguntas, botões de preferência e escolhas A vs. B numa faixa embaixo**, como na C. Algumas perguntas ainda podem ficar no painel lateral;
- o padrão visual dos três mockups (escuro, laranja e roxo, malha estilo AutoCAD) é aprovado como referência de qualidade.
Proposta do Agente para separar as perguntas: a **faixa de baixo é "a decisão da vez"** (uma pergunta por vez, que some quando não há o que decidir) e o **painel lateral é "o estado do projeto"** (grafo, premissas e preferências editáveis, console e campo de texto livre).
Status: Aprovada (regra da faixa vs. painel em validação no mockup v2).

### Pendências abertas (S02)

- Validar o `layout-v2.html`.
- Assuntos restantes do brainstorm: escopo exato do MVP (tipo de casa, quais geradores primeiro), nome do projeto, documento de design.
- O responsável vai inicializar o git depois de definir o nome; incluir `.superpowers/` no `.gitignore`.

### Log da sessão — continuação

2. **Responsável:** aprovou o layout v2 com ajustes: premissas sempre visíveis no painel direito sem sobrecarga; faixa superior +30% (altura e fonte); console pequeno com ~1/3 da altura do painel e scroll; faixa de perguntas maior, principalmente no A vs. B. **Agente:** montou `layout-v3.html` e `layout-v3-1.html`, conferiu com screenshots via playwright e registrou a DEC-0041. O teste de estresse mostrou que, na escala do mockup, cerca de 30 premissas não cabem inteiras junto com o grafo e o console.

### Decisões — continuação

**DEC-0041 — Ajustes do layout (v3)**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Interface
Complementa: DEC-0040.
Decisão:
- **Faixa superior** 30% maior em altura e fonte (novo, abrir, salvar, excluir, abas de projeto, indicador de etapa).
- **Console** com texto pequeno em monoespaçada, ocupando cerca de 1/3 da altura do painel lateral, com barra de scroll e horário em cada linha.
- **Faixa de perguntas** bem maior: texto ~17 px, botões e escala grandes. No A vs. B, as miniaturas são grandes o bastante para comparar as plantas, com o resumo simétrico (DEC-0037/0039) e um botão "Escolher" em cada uma.
- **Premissas e preferências sempre visíveis** no painel direito, em chips compactos agrupados por tipo (terreno, cômodos, relações, preferências, itens pedidos, restrições aprendidas, avisos aceitos), com contador, edição por clique e destaque animado no item mais recente.
- Tamanho da planta e do grafo no primeiro passo: aprovados como estão.
Status: Aprovada (regra para quando as premissas não couberem em validação).

### Log da sessão — continuação 2

3. **Responsável:** aprovou o v3.1 e pediu as proporções 20/50/30 no painel direito (grafo, premissas e console), dando prioridade às premissas. Achou o bloco de premissas sobrecarregado de cores e subcampos e pediu algo mais visual e imediato, sem perder nada. Pediu o campo de texto livre 30% maior, deixando claro que ele serve para ajustar preferências não perguntadas. **Agente:** montou `layout-v4.html`, conferiu por screenshot que as 30 premissas cabem inteiras sem scroll e registrou a DEC-0042.

### Decisões — continuação 2

**DEC-0042 — Painel direito 20/50/30 e premissas visuais**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Interface
Complementa: DEC-0041. Resolve a pendência sobre premissas que não cabem.
Decisão:
- O painel direito tem proporções verticais fixas: **grafo 20%**, **premissas e preferências 50%**, **console 30%**. A prioridade é que o usuário veja claramente quais preferências estão sendo obtidas.
- O **campo de texto livre** fica 30% maior, com um rótulo explicativo ("✎ Texto livre: ajuste qualquer coisa que não foi perguntada") e um exemplo no placeholder.
Proposta do Agente para o bloco de premissas, sem os chips coloridos:
- **fatos** (terreno, cômodos, itens pedidos) aparecem como texto corrido com separadores;
- **intensidades** (relações entre cômodos e preferências) aparecem como **barras bipolares** que crescem do centro: verde para a direita ("quero/aproximar"), vermelho para a esquerda ("evitar/afastar"); o número exato aparece ao passar o mouse;
- o item mais recente fica em laranja;
- os avisos aceitos ficam numa linha com ⚠.
Resultado do teste: 30 premissas cabem inteiras na escala do mockup, ainda com folga.
Status: Aprovada (formato das barras em validação).

### Log da sessão — continuação 3

4. **Responsável:** pediu o grafo dentro do bloco de premissas, um pouco menor, com o bloco ocupando 70% e o console mantido. Disse que a barra horizontal bipolar confunde em duas colunas e sugeriu barra vertical ou pizza. Pediu linhas suaves entre os subtópicos. Adiantou que a planta deve ter cotas: só as do terreno nesta fase e, no futuro, uma cota interativa com o mouse. **Agente:** montou `layout-v5.html` com o grafo integrado, a proporção 70/30, linhas separadoras, o indicador em anel (rosca) e as cotas do terreno. Mostrou também três indicadores para comparar (anel, barra vertical, pontos). Ajustou o tamanho do grafo depois de o screenshot mostrar o último item cortado. Registrou DEC-0043 e DEC-0044.

### Decisões — continuação 3

**DEC-0043 — Painel direito 70/30 com o grafo integrado**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Interface
Substitui: DEC-0042 (proporções 20/50/30 e barra horizontal bipolar).
Decisão:
- O bloco separado do grafo deixa de existir. O grafo de relações, menor, passa a ser o primeiro item do bloco de premissas e preferências.
- Proporções verticais: **premissas (com o grafo) 70%** e **console 30%**. O campo de texto livre continua igual.
- Os subtópicos (grafo, terreno, cômodos, itens, relações, o que você valoriza, avisos) ficam separados por **linhas suaves e pouco opacas**.
- O indicador de intensidade **não pode depender de esquerda/direita**, por causa das duas colunas.
Proposta do Agente: um anel (rosca) colorido pela direção (verde = quero/aproximar, vermelho = evitar/afastar), com o preenchimento indicando a intensidade. Alternativas mostradas: barra vertical e pontos de 1 a 5.
Status: Aprovada (escolha do indicador pendente).

**DEC-0044 — Cotas na planta**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Interface / Produto
Decisão:
- **Nesta fase**, a planta exibe apenas as **cotas do terreno**, em um lado de cada par de lados paralelos (uma cota horizontal e uma vertical), no estilo de cota do AutoCAD.
- **No futuro**, a cota será interativa: com o mouse dentro de um cômodo, retas ortogonais (horizontal e vertical) "infinitas" encontram as paredes, e as medidas do cômodo aparecem junto ao cursor ou fixas ao lado das paredes.
Status: Aprovada (a cota interativa é futura).

### Log da sessão — continuação 4

5. **Responsável:** escolheu o indicador C (pontos), aprovou o restante do layout v5 e pediu para prosseguir. **Agente:** registrou a DEC-0045 e passou ao escopo do MVP.

### Decisões — continuação 4

**DEC-0045 — Indicador de intensidade: pontos**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Interface
Complementa: DEC-0043.
Decisão: a intensidade de relações e preferências é exibida com **1 a 5 pontos acesos**, na cor da direção (verde = quero/aproximar, vermelho = evitar/afastar). O layout v5 (`.superpowers/brainstorm/.../layout-v5.html`) fica **aprovado como referência da interface**.
Justificativa: os pontos se leem como uma nota exata, sem precisar estimar tamanho, e funcionam em duas colunas.
Status: Aprovada.

### Log da sessão — continuação 5

6. **Responsável:** fechou o recorte geométrico do MVP: casa térrea, cômodos retangulares, terreno retangular. Perguntou se o algoritmo conseguiria gerar plantas de mais de um pavimento sem antes ter o 3D (escadas, alinhamento de paredes entre pavimentos). Registrou as evoluções futuras: cômodos ortogonais não retangulares, terrenos irregulares sem deformar todos os cômodos e, por último, formas circulares. **Agente:** respondeu que o multipavimento não depende do 3D (é um problema "2,5D") e registrou DEC-0046 e DEC-0047.

### Decisões — continuação 5

**DEC-0046 — Recorte geométrico do MVP**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Escopo
Decisão: o MVP trata apenas de **casa térrea**, **cômodos retangulares** e **terreno retangular**. O modelo de dados nasce preparado para pavimentos, polígonos e terrenos irregulares (campo de pavimento, geometria genérica), mas os algoritmos do MVP só lidam com o caso retangular.
Status: Aprovada.

**DEC-0047 — Evoluções geométricas futuras e o multipavimento**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Escopo / Arquitetura
Decisão (ordem de dificuldade, do mais viável ao mais complexo):
1. **cômodos ortogonais não retangulares** (formas em L, T ou U, só com ângulos de 90°), viáveis como união de retângulos na mesma grade;
2. **terreno irregular**: o algoritmo deve lidar com ele **sem deformar todos os cômodos**, podendo ou não acompanhar o lado torto;
3. **ambientes circulares ou curvos**, o passo mais complexo, por último.
Nota técnica do Agente sobre o multipavimento: gerar plantas de vários pavimentos **não depende do 3D**. É um problema "2,5D", com uma planta 2D por pavimento ligada por **restrições verticais**:
- a escada é um elemento com a mesma projeção (x, y) nos dois pavimentos e com área reservada nos dois;
- as áreas molhadas empilhadas ficam como preferência, para economizar hidráulica;
- o alinhamento de paredes ou estrutura entre pavimentos é uma preferência de economia construtiva (sobreposição de linhas de parede);
- o pavimento superior deve estar apoiado (DEC-0035).
O 3D é visualização e modelagem e não é pré-requisito lógico. A ordem entre "3D" e "multipavimento" no roadmap fica em aberto. Preferência inicial do responsável: multipavimento depois de algum 3D.
Hipótese do Agente para o terreno irregular: os cômodos ficam numa grade ortogonal alinhada ao eixo principal do terreno, e só os cômodos encostados no lado torto podem ser recortados por ele; as sobras viram área externa ou jardim.
Status: Aprovada (registro de roadmap; nada disso entra no MVP).

### Log da sessão — continuação 6

7. **Responsável:** definiu multipavimento e 3D como próximos passos, sem ordem entre eles. Aprovou o tratamento do terreno irregular, com a planta paralela à frente do terreno, ou seja, à rua. Aprovou a ordem dos geradores: CP-SAT, árvore de subdivisão, depois crescimento em grade e recozimento simulado. **Agente:** registrou DEC-0048 a DEC-0050.

### Decisões — continuação 6

**DEC-0048 — Multipavimento e 3D sem ordem definida**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Escopo
Substitui: DEC-0047 (trecho "preferência inicial: multipavimento depois de algum 3D").
Decisão: multipavimento (2,5D) e 3D são **próximos passos após o MVP 2D, sem ordem definida** entre si.
Status: Aprovada.

**DEC-0049 — Orientação da planta em terreno irregular**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Arquitetura
Complementa: DEC-0047.
Decisão: a grade ortogonal dos cômodos fica, por padrão, **paralela à frente do terreno** (direção da rua), para a construção ser ortogonal à rua, mesmo que a frente esteja inclinada em relação aos outros lados. Só os cômodos encostados em lados tortos podem ser recortados por eles; as sobras viram área externa. (Aplicação futura; o MVP usa terreno retangular.)
Status: Aprovada.

**DEC-0050 — Ordem de implementação dos geradores**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável (proposta do Agente) · Categoria: Arquitetura
Complementa: DEC-0010.
Decisão:
1. **CP-SAT** (otimização por restrições), o primeiro, por garantir a validade geométrica e gerar soluções diversas;
2. **árvore de subdivisão**, simples, rápida e muito visual;
3. e 4. **crescimento em grade** e **recozimento simulado**, por último, para o comparativo.
Status: Aprovada.

### Log da sessão — continuação 7

8. **Responsável:** discutiu o nome do projeto. Rejeitou "agent_floor_plan" (o projeto não é só planta baixa nem exatamente um agente) e pediu um nome técnico e profissional, em inglês, bom para portfólio, git e um app futuro. Considerou Prumo, TruePlan e variações com "your". Decidiu por **TruePlumb** e pediu para renomear a pasta. **Agente:** registrou a DEC-0051, atualizou o README e o CLAUDE.md e renomeou a pasta para `TruePlumb`.

### Decisões — continuação 7

**DEC-0051 — Nome do projeto: TruePlumb**
Data: 2026-11-11 · Sessão: S02 · Autor: Responsável · Categoria: Processo / Produto
Decisão: o projeto se chama **TruePlumb**. A pasta passa de `agent_ia_foor_plan` para `TruePlumb`.
Origem: "plumb and true", expressão da carpintaria em inglês para "no prumo e no esquadro", ou seja, perfeitamente reto e correto. Remete ao "prumo" em português e ao diferencial de plantas tecnicamente corretas.
Consequências:
- o nome do repositório git e o título do README seguem o novo nome;
- disponibilidade como marca, domínio ou repositório ainda não foi verificada;
- sugestão do Agente para um slogan futuro, a confirmar: "plan your home, plumb and true".
Status: Aprovada.

### Pendências abertas (S02) — atualização

- Responsável: inicializar o git na pasta `TruePlumb`, com `.superpowers/` e `.playwright-mcp/` no `.gitignore`.
- Agente: escrever o documento de design, passá-lo por revisão independente e levá-lo à aprovação; depois, o plano de implementação.

---

## Sessão S03 — 2026-11-11

### Log da sessão (prompts e ações, em resumo)

1. **Responsável:** informou o nome definitivo **PyGridPlan**, que criou o repositório e inicializou o git. Pediu a lista exata dos arquivos que pode excluir da raiz, os próximos passos e os primeiros commits. Pediu como regra que o agente sempre mostre antes quais commits e quais arquivos sugere, e que, após a confirmação, o agente faça `git add` e `git commit`, ficando o `git push` com o responsável. **Agente:** atualizou o nome no README e no CLAUDE.md, acrescentou a regra de commits ao CLAUDE.md, criou o `.gitignore`, copiou o mockup aprovado para `docs/mockups/layout-v5.html`, registrou DEC-0052 a DEC-0054 e apresentou o plano de commits para confirmação.

### Decisões

**DEC-0052 — Nome definitivo do projeto: PyGridPlan**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Processo / Produto
Substitui: DEC-0051.
Decisão: o projeto se chama **PyGridPlan**. A pasta e o repositório git usam esse nome. O slogan provisório "plan your home, plumb and true", ligado ao nome anterior, foi retirado do README.
Consequências: disponibilidade do nome como repositório, domínio ou marca ainda não foi verificada pelo Agente.
Status: Aprovada.

**DEC-0053 — Regra de commits: plano antes, push pelo responsável**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Processo
Decisão: antes de qualquer commit, o agente mostra os commits sugeridos (mensagem e arquivos de cada um). Após a confirmação, o agente executa `git add` e `git commit`. O `git push` é sempre do responsável. A regra foi acrescentada ao CLAUDE.md, seção "Arquivos e git", por pedido explícito do responsável.
Status: Aprovada.

**DEC-0054 — `.gitignore` inicial e preservação do mockup aprovado**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente · Categoria: Ferramentas / Processo
Decisão:
- o `.gitignore` exclui `.superpowers/` e `.playwright-mcp/` (artefatos das ferramentas do agente, incluindo um token de sessão do servidor de mockups), `.claude/settings.local.json`, caches e ambientes Python, `node_modules/`, arquivos `.env` e arquivos de sistema e editor;
- como o `layout-v5.html`, aprovado como referência da interface (DEC-0045), estava dentro de `.superpowers/` (que fica fora do git), uma cópia foi colocada em `docs/mockups/layout-v5.html` para entrar no repositório.
Status: Proposta (aguardando o responsável junto com o plano de commits).

### Pendências abertas (S03)

- Responsável: confirmar o plano de commits; depois, criar o repositório remoto e fazer o `git push`.
- Responsável: decidir se renomeia o branch `master` para `main` (padrão atual do GitHub).
- Agente: escrever o documento de design (`docs/superpowers/specs/`), passá-lo por revisão independente e levá-lo à aprovação; depois, o plano de implementação.
