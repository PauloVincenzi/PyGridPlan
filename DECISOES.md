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

### Log da sessão — continuação

2. **Responsável:** confirmou os três commits, pediu a renomeação do branch para `main` e autorizou o push **desta vez**. Pediu o documento de design. Pediu que o agente sugira skills de repositórios confiáveis sempre que for oportuno (interface, otimização etc.) e que o oriente continuamente sobre o presente e os próximos passos. Pediu a instalação de uma skill vista no Instagram que faz o Claude escrever só o código estritamente necessário. **Agente:** fez os commits `89b9cb8`, `055b001` e `f2173b3`, renomeou o branch para `main` e fez o push para `origin/main`. Identificou a skill como `karpathy-guidelines` (repositório comunitário `forrestchang/andrej-karpathy-skills`, licença MIT; não é oficial do Karpathy nem da Anthropic), leu o conteúdo antes de instalar (só markdown, sem scripts nem hooks) e instalou o plugin `andrej-karpathy-skills@karpathy-skills` no escopo de usuário. Levantou no marketplace oficial os plugins úteis por fase. Escreveu o documento de design `docs/superpowers/specs/2026-11-11-pygridplan-mvp-design.md`, passou-o por um revisor independente (subagente), resolveu 4 das 6 dúvidas levantadas e levou as outras 2 ao responsável.

### Decisões — continuação

**DEC-0055 — Skill de código mínimo: karpathy-guidelines**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (identificação e instalação pelo Agente) · Categoria: Ferramentas / Processo
Decisão: o plugin `andrej-karpathy-skills` foi instalado e a skill `karpathy-guidelines` passa a orientar a escrita de código (pensar antes de codar, simplicidade primeiro, mudanças cirúrgicas, execução guiada por metas verificáveis). A regra foi acrescentada à seção "Princípios de arquitetura" do CLAUDE.md, por pedido do responsável.
Nota do Agente: não há como confirmar que é exatamente a skill do post visto no Instagram. É a mais difundida com essa proposta e contém a regra "se escreveu 200 linhas e dava em 50, reescreva". Outra candidata com a mesma proposta é a `ponytail` (DietrichGebert), não instalada. Código mínimo não autoriza cortar validação nem testes.
Status: Aprovada.

**DEC-0056 — Sugestão proativa de skills e orientação contínua**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Processo
Decisão: o agente sugere skills e plugins adequados a cada fase, apenas os que existem de fato e com o conteúdo de terceiros lido antes de instalar, e fecha cada rodada dizendo o que foi feito e quais são os próximos passos. A autorização de push desta rodada foi pontual: a regra da DEC-0053 continua valendo.
Status: Aprovada.

**DEC-0057 — Documento de design do MVP (rascunho)**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente · Categoria: Arquitetura / Escopo
Decisão proposta: o documento `docs/superpowers/specs/2026-11-11-pygridplan-mvp-design.md` consolida DEC-0001 a DEC-0054. Escolhas próprias do Agente, marcadas no texto: K = 4 alternativas por etapa; unidade em mm e grade de 100 mm; modelo de cômodos nos eixos das paredes (externa 150 mm, interna 100 mm); agregação inicial por soma ponderada com retornos decrescentes; métrica de diversidade; layers do DXF; marcos M0–M8 com sugestão de fechar o MVP no M5; estrutura do repositório; mínimos e recuos rígidos até existir a negociação; valores mínimos provisórios marcados "sem fonte"; orientação solar com sol bom ao norte (hemisfério sul); meta de ~5 s por alternativa com soluções parciais transmitidas desde o M1.
Status: Proposta (aguardando duas respostas e a aprovação do responsável).

### Pendências abertas (S03) — atualização

- Responsável: responder se a casa é um bloco único e como se define a área construída.
- Responsável: responder se é permitido passar por um cômodo para chegar a outro e onde fica a entrada.
- Responsável: aprovar o documento de design. Depois disso, o Agente segue para a skill `writing-plans`.
- Commit do documento, do CLAUDE.md e do DECISOES.md, com o plano de commits a apresentar após a aprovação.

### Log da sessão — continuação 2

3. **Responsável:** pediu que o agente pensasse como engenheiro de software e de dados, porque a raiz confundia: `.superpowers/` sem propósito claro e `docs/superpowers/` aparentemente duplicando. Pediu pastas com nomes que digam o que guardam, questionou a data no nome do documento de design e perguntou sobre pastas `data` e `src`. Confirmou a skill `karpathy-guidelines`, com a ressalva de não poupar testes e validações, mas evitar complexidade, passos demais e redundância de definições ou armazenamento. Pediu que o CLAUDE.md liste todas as skills, com finalidade e regras. Achou o documento de design condizente com a conversa, aprovou as 5 skills por fase e respondeu às duas perguntas (implantação no terreno e passagem entre cômodos). **Agente:** explicou que `.superpowers/` é rascunho do servidor de mockups (nome fixo da skill, fora do git) e que `docs/superpowers/` era só o local padrão das skills, substituível. Moveu o design para `docs/design/mvp.md` (sem data no nome) e os mockups para `docs/design/mockups/`, removendo `docs/superpowers/`. Acrescentou ao CLAUDE.md as seções "Estrutura de pastas" e "Skills e plugins", atualizou o README e o `.gitignore` (`out/`), incorporou as respostas ao design (seções 5.5 e 6.2) e registrou DEC-0058 a DEC-0061.

### Decisões — continuação 2

**DEC-0058 — Estrutura de pastas do repositório**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (proposta do Agente) · Categoria: Arquitetura / Processo
Contexto: confusão entre `.superpowers/` e `docs/superpowers/`; documento de design com data no nome.
Decisão:
- `src/pygridplan/` (motor, layout "src"), `web/` (interface), `data/` (dados de referência versionados), `tests/` (com `fixtures/`), `docs/design/` (design e mockups), `docs/plans/` (planos por marco), `docs/theory/` (teoria), `out/` (saídas geradas, fora do git);
- `.superpowers/` e `.playwright-mcp/` são rascunhos das ferramentas, fora do git, e não guardam nada importante;
- nomes de pastas e arquivos em inglês, minúsculas com hífen; conteúdo em português;
- **sem data no nome dos arquivos**: data e versão no cabeçalho, histórico no git;
- esses locais substituem os padrões das skills (`docs/superpowers/specs` → `docs/design`, `docs/superpowers/plans` → `docs/plans`);
- pastas só nascem com o primeiro arquivo.
Justificativa do Agente: o layout "src" evita importar o pacote sem instalá-lo (erro clássico de testes passando só na máquina do autor); separar `data/` (referência curada, versionada, com fonte) de `out/` (gerado, descartável) e de `tests/fixtures/` (casos de teste) evita misturar dado de verdade com dado produzido.
Consequências: o documento de design foi movido de `docs/superpowers/specs/2026-11-11-pygridplan-mvp-design.md` para `docs/design/mvp.md`, e o mockup citado na DEC-0045 está agora em `docs/design/mockups/layout-v5.html`. A antiga pasta `knowledge/` do design virou `data/`. O catálogo de tipos de cômodo em `data/` é a fonte única de zona, classe de passagem e mínimos.
Status: Aprovada (organização pedida pelo responsável; nomes propostos pelo Agente).

**DEC-0059 — Implantação no terreno: bloco único e pergunta condicional de divisas**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (parâmetros propostos pelo Agente) · Categoria: Produto / Arquitetura
Decisão:
- a casa **por padrão** é um bloco único, mas nem sempre precisa ser; blocos separados são representáveis no modelo. O gerador do MVP produz bloco único (proposta do Agente);
- o encostamento em divisas é definido pelo usuário numa pergunta **semi-obrigatória**: "A casa pode encostar em alguma divisa?", com marcação de esquerda, direita e fundo (nenhuma = casa solta; a frente nunca encosta);
- a pergunta só aparece quando é relevante: área pretendida ÷ área do terreno ≥ 0,30, **ou** a casa compacta não cabe com os afastamentos recomendados (limiares propostos pelo Agente, configuráveis);
- área construída pretendida é campo opcional; sem ela, o motor estima pela soma dos mínimos mais a circulação.
Exemplos do responsável: terreno 100×100 m com 200 m² → não pergunta; terreno 25×10 m com ≥ 100 m² → pergunta.
Status: Aprovada (limiares a validar com casos de teste).

**DEC-0060 — Passagem entre cômodos: privativos vs. atravessáveis**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (detalhes propostos pelo Agente) · Categoria: Arquitetura / Produto
Decisão:
- **privativos, sem travessia:** quarto, banheiro e closet. A sequência quarto → closet → banheiro dentro da suíte é natural e não conta como travessia social;
- **atravessáveis:** os demais, incluindo salas integradas ou separadas, cozinhas, áreas de lazer;
- o sistema precisa suportar programas atípicos de alto padrão (cinema, spa, academia, quadras, várias cozinhas, excesso de cômodos convencionais).
Detalhes propostos pelo Agente: a classe de passagem é atributo do tipo de cômodo no catálogo de `data/`; tipos novos entram como atravessáveis e o usuário pode mudar; atravessar tem custo suave, maior em cômodos de uso concentrado (cinema, escritório, spa); a entrada fica na frente do terreno, posição escolhida pelo motor e ajustável.
Status: Aprovada.

**DEC-0061 — Registro de skills no CLAUDE.md**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Ferramentas / Processo
Complementa: DEC-0055, DEC-0056.
Decisão: o CLAUDE.md lista todas as skills e plugins usados, a usar e possíveis, com origem, situação, finalidade e regra de uso. Ficam aprovados para instalação por fase: `pyright-lsp` e `code-simplifier` (M0), `playground` (M1), `typescript-lsp` e `modern-web-guidance` (M2), além do já previsto `mcp-server-dev`. A `karpathy-guidelines` é confirmada com a ressalva do responsável: evitar complexidade, passos demais e redundância de definições ou armazenamento, **sem** poupar testes nem validações. O documento de design teve o conteúdo aprovado; as seções 5.5 e 6.2, novas, aguardam a leitura do responsável.
Status: Aprovada.

### Pendências abertas (S03) — atualização 2

- Responsável: ler as seções 5.5 (passagem) e 6.2 (implantação) do `docs/design/mvp.md`.
- Responsável: confirmar o plano de commits desta rodada.
- Responsável: decidir se apaga as pastas locais `.superpowers/` e `.playwright-mcp/` (opcional; ambas estão fora do git).
- Agente: com o design aprovado, usar `writing-plans` para o plano do M0 em `docs/plans/`; instalar `pyright-lsp` e `code-simplifier` no início do M0, com confirmação.

### Log da sessão — continuação 3

4. **Responsável:** perguntou por que o layout `src/` obriga a instalar o pacote antes dos testes e como evitar isso; comentou a separação dos dados em três pastas (`data/`, `tests/fixtures/`, `out/`), perguntando se `out/` servirá a análises; concordou com a fonte única de tipos de cômodo e com pastas sob demanda. Pediu que a estrutura macro de software e dados, com paths, fique sempre no README. Autorizou os 5 commits e o push **desta vez**. Decidiu manter `.superpowers/` e `.playwright-mcp/` (geradas e fora do git). Pediu a instalação de `pyright-lsp` e `code-simplifier` e o plano do M0 via `writing-plans`. **Agente:** fez os commits `309f811`, `8aff969`, `eab1fc7`, `e037a83`, `2e1d24f` e o push. No meio do caminho, um commit local juntou por engano o `.gitignore` e o rename do mockup; antes do push, o Agente desfez esse commit local e refez os dois separados, como no plano aprovado. Instalou o `pyright` 1.1.414 (npm, global) e os plugins `pyright-lsp` e `code-simplifier`. Conferiu que existem wheels para Python 3.13 no Windows (ortools 9.15, ezdxf 1.4.5, pydantic 2.14, pyyaml 6.0, pytest 9.2). Atualizou o README (estrutura macro e tabela de dados) e o CLAUDE.md (regra do README e situação dos plugins). Escreveu `docs/plans/m0-foundation.md`. Registrou DEC-0062 a DEC-0065.

### Decisões — continuação 3

**DEC-0062 — Instalação do pacote: layout `src/` com instalação editável**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente (pergunta do Responsável) · Categoria: Arquitetura / Ferramentas
Contexto: o responsável perguntou se a exigência de instalar o pacote antes dos testes é uma restrição a evitar.
Decisão: manter o layout `src/` e instalar uma vez com `pip install -e ".[dev]"` num `.venv`. O comando instala as dependências e o pacote em modo editável (as mudanças no código valem sem reinstalar). Como as dependências precisam ser instaladas de qualquer forma, o pacote não custa um passo extra. A alternativa (`pythonpath = ["src"]` no pytest, sem instalar) foi descartada para manter um único caminho. O README documenta o requisito na tarefa 1 do M0.
Status: Aprovada (implementação no M0).

**DEC-0063 — Categorias de dados do projeto**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (proposta do Agente) · Categoria: Dados
Decisão: o README mantém a tabela das categorias de dados: **referência** (`data/`, versionada, com fonte), **casos de teste** (`tests/fixtures/`, versionados, também entradas de benchmark), **gerados** (`out/`, fora do git, recriáveis a partir de entrada e semente), **resultados de análise** (só o resumo versionado; local a decidir quando houver benchmark) e **dados do usuário** (projetos salvos e histórico de escolhas para o aprendizado de pesos; local a decidir no M2, fora do repositório). A estrutura macro de software e dados com paths fica sempre no README (regra no CLAUDE.md).
Status: Aprovada.

**DEC-0064 — Instalação de pyright-lsp e code-simplifier**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Ferramentas
Decisão: instalados `pyright-lsp` e `code-simplifier` (`claude-plugins-official`, escopo de usuário) e o executável `pyright` 1.1.414 via `npm install -g pyright`, exigido pelo plugin.
Status: Aprovada.

**DEC-0065 — Plano do M0 (fundação)**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente · Categoria: Arquitetura
Decisão proposta: `docs/plans/m0-foundation.md`, com 6 tarefas em TDD (esqueleto e testes de instalação; modelo da planta; catálogo; paredes derivadas e área útil; validador; DXF e CLI) e 35 testes previstos. Escolhas do Agente:
- Pydantic para as entidades (uma definição para validar e serializar);
- catálogo em YAML (`data/room_types.yaml`, com PyYAML), legível para curadoria;
- origem no canto frente-esquerda do terreno;
- paredes derivadas e não armazenadas;
- área útil conservadora em lados parcialmente externos;
- desvio consciente: no M0 o cômodo guarda um `Rect`, e não um polígono genérico (design seção 10), até os terrenos irregulares entrarem;
- cada passo "Commit" do plano é uma proposta ao responsável (DEC-0053).
Status: Proposta (aguardando revisão e escolha do modo de execução).

### Pendências abertas (S03) — atualização 3

- Responsável: revisar o plano do M0 e escolher o modo de execução (subagentes ou nativo).
- Responsável: confirmar o plano de commits desta rodada.

### Log da sessão — continuação 4

5. **Responsável:** aprovou o plano do M0 e a execução nativa, sem subagentes por tarefa. Confirmou os cômodos só retangulares por ora; polígonos genéricos e ambientes curvos (aproximados por malha em milímetros) serão estudados depois. Autorizou o agente a fazer `git add` e `git commit` durante a execução; o push fica com o responsável. **Agente:** criou o branch `feat/m0-foundation`, porque não se implementa direto no `main`. Fez os 3 commits de documentação pendentes e executou as 6 tarefas em TDD (teste vermelho antes de cada implementação). Fez uma verificação visual do DXF (render SVG e screenshot) e passou o branch por uma revisão final independente (subagente). O revisor apontou 0 problemas críticos, 2 importantes e 8 menores. O Agente corrigiu os 2 importantes e 2 menores que reclassificou como importantes, cada um com teste RED → GREEN. Ao fim: 40 testes passando e `pyright` com 0 erros. Atualizou o README e registrou DEC-0066 e DEC-0067.

### Decisões — continuação 4

**DEC-0066 — M0 (fundação) concluído**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente (execução aprovada pelo Responsável) · Categoria: Arquitetura
Substitui: DEC-0065 (status do plano).
Decisão: o M0 está implementado no branch `feat/m0-foundation`:
- pacote `src/pygridplan` (modelo `Rect`/`Site`/`Room`/`Plan` em mm inteiros, JSON);
- catálogo `data/room_types.yaml` (12 tipos, valores provisórios "sem fonte");
- paredes derivadas e área útil;
- validador (erros `overlap`, `wall_overlap`, `too_small`, `outside_lot`; avisos `setback`, `min_width`, `min_area`);
- DXF com os 10 layers e cotas do terreno;
- CLI `python -m pygridplan export-dxf`;
- 40 testes e `pyright` sem erros.
Rulings do Agente durante a execução:
- os briefs foram lidos direto do plano, porque o script da skill procura títulos "Task N";
- reinstalação editável depois de criar o pacote;
- `tests/conftest.py` com a fixture compartilhada;
- sala do teste de recuo aumentada, porque disparava um `min_area` legítimo;
- imports do ezdxf ajustados para o pyright.
Correções da revisão final:
- `extra="forbid"`: chaves desconhecidas no JSON ou no YAML agora são erro, e não são mais ignoradas;
- detecção de paredes sobrepostas entre cômodos afastados menos que uma parede externa (design 5.1);
- erro para cômodo menor que as próprias paredes;
- fonte TrueType (`arial.ttf`) no estilo de texto do DXF, porque a SHX padrão não exibe "²" nem acentos.
Pendências menores adiadas:
- rótulos largos demais em cômodos estreitos (avaliar no M2);
- IDs duplicados no catálogo se sobrescrevem;
- a CLI não roda o validador;
- o teste de IDs duplicados não passa pelo `load_plan`;
- `pyright` não é dependência declarada (documentado no README).
Status: Aprovada (aguarda o push e a decisão de merge do responsável).

**DEC-0067 — Geometria dos cômodos: retângulos agora, polígonos depois**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Arquitetura
Complementa: DEC-0046, DEC-0047.
Decisão: no início, os cômodos são só retângulos (`Room.rect`). Depois será estudada a generalização para **polígonos com número de lados qualquer**. Ambientes curvos poderão ser **aproximados por malha em milímetros**, no último caso.
Status: Aprovada (estudo futuro).

### Pendências abertas (S03) — atualização 4

- Responsável: `git push -u origin feat/m0-foundation` e decidir o merge no `main` (direto ou via pull request).
- Agente: no M1, começar pelo plano `docs/plans/m1-cpsat-generator.md` (gerador CP-SAT, pontuação, árvore de estados), resolvendo antes as pendências menores do M0 que afetam o M1 (CLI com validador, IDs duplicados no catálogo).
- Instalar o plugin `playground` no início do M1 (DEC-0061).

### Log da sessão — continuação 5

6. **Responsável:** escolheu a opção 2 (push e pull request, ambos feitos por ele). Abriu o DXF num visualizador da Autodesk e o SVG no navegador e achou a planta condizente. Pediu eixos e paredes em cores diferentes, e paredes que fechem nas quinas, preenchidas até a interseção (como o *fill* do AutoCAD). Perguntou se o M0 está encerrado e se dá para começar o M1. Pediu como regra declarar sempre quando uma fase termina, pausa ou avança, com justificativa, e terminar toda resposta com os próximos passos do responsável e do agente. **Agente:** em TDD (4 testes novos, RED → GREEN): paredes como hachura sólida estendidas até a face da parede perpendicular; layer `A-EIXOS` vermelho, traço-ponto; `A-AREAS` com o contorno da área útil. Fez a conferência visual por SVG. Fez o commit `2504cab`. Atualizou a seção 13 do design e acrescentou as regras ao CLAUDE.md. Registrou DEC-0068 a DEC-0071.

### Decisões — continuação 5

**DEC-0068 — Representação do DXF: paredes preenchidas, eixos e área útil**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (solução do Agente) · Categoria: Interface / Arquitetura
Complementa: DEC-0008; altera a lista de layers da DEC-0065/DEC-0066.
Decisão:
- paredes em **hachura sólida**: cada faixa é estendida nas pontas até a face da parede perpendicular mais grossa, o que fecha quinas e encontros em T;
- **eixos** no novo layer `A-EIXOS` (cor 1, vermelho; linha CENTER; `$LTSCALE` 50);
- paredes externas na cor 7 e internas na cor 8;
- `A-AREAS` passa a ter o contorno da **área útil** (faces internas, cor 9), e o comando ÁREA do AutoCAD bate com o rótulo.
Justificativa do Agente: contornos separados por parede nunca fecham as quinas (as linhas se cruzam). O contorno único exato exige união de polígonos, que fica para depois se o responsável quiser paredes editáveis como linhas.
Status: Aprovada.

**DEC-0069 — Regra: encerramento explícito de fase e definição de pronto**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Processo
Decisão: toda fase, etapa ou marco termina com uma declaração de estado (concluída, pausada com acréscimos previstos, ou em andamento), justificada com evidências, listando as pendências e dizendo se elas bloqueiam a fase seguinte. "Pronto" para um marco: tarefas do plano feitas; testes e `pyright` sem falhas; revisão final com críticos e importantes corrigidos; conferência visual aprovada quando houver saída visual; README e DECISOES.md atualizados; pendências menores listadas. Regra registrada no CLAUDE.md.
Status: Aprovada.

**DEC-0070 — Regra: próximos passos em toda resposta**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Processo
Decisão: toda resposta do agente neste projeto termina com "Próximos passos", separados em **Responsável** e **Agente**. Regra registrada no CLAUDE.md.
Status: Aprovada.

**DEC-0071 — Declaração: M0 concluído**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente (conferência visual aprovada pelo Responsável) · Categoria: Processo
Decisão: o M0 está **concluído**, segundo a DEC-0069:
- as 6 tarefas do plano foram feitas;
- 43 testes passam e o `pyright` não acusa erros;
- a revisão final independente teve 0 achados críticos, e os importantes foram corrigidos;
- o responsável conferiu o DXF num visualizador Autodesk; o ajuste visual que pediu (DEC-0068) foi feito;
- README e DECISOES.md estão atualizados.
É suficiente para o M1 porque o M1 consome exatamente o que o M0 entrega: o modelo `Plan` (forma da solução do gerador), o catálogo (mínimos por tipo), o validador (porta de entrada de toda solução gerada) e a exportação DXF (para inspecionar as alternativas).
Pendências que **não bloqueiam** o M1: rótulos largos em cômodos estreitos (M2); `pyright` fora das dependências declaradas.
Pendências a resolver **no início do M1**: a CLI deve rodar o validador; IDs duplicados no catálogo devem dar erro; o teste de IDs duplicados deve passar pelo `load_plan`.
Status: Aprovada (o merge no `main` acontece via pull request do responsável).

### Pendências abertas (S03) — atualização 5

- Responsável: `git push -u origin feat/m0-foundation`, abrir o pull request e fazer o merge.
- Agente: depois do merge, instalar o `playground` e escrever o plano do M1.

### Log da sessão — continuação 6

7. **Responsável:** fez o push, abriu e mergeou o PR #1 (M0). Perguntou se as medidas mínimas e os tipos de cômodo do catálogo foram embasados em pesquisa, já que a maioria dos cômodos foi citada de memória por ele, e pediu pesquisa extensa em material de arquitetura e engenharia: nomes de cômodos, destinos, dimensões mínimas, normas e padrões. Pediu para voltar ao `main` atualizado, criar o branch do M1, instalar o `playground` e escrever o plano do M1 para revisão antes de codar. **Agente:** respondeu que **não** houve pesquisa: os valores do catálogo são provisórios, marcados "provisório, sem fonte", e propôs a trilha de dados D1 (DEC-0072). Atualizou o `main` (`1ececa7`), criou `feat/m1-cpsat-generator` e apagou o branch local do M0, já mergeado. Instalou o `playground` e corrigiu a finalidade dele no CLAUDE.md: ele monta textos a partir de controles visuais e não executa o motor. Escreveu `docs/plans/m1-cpsat-generator.md` (DEC-0073).

### Decisões — continuação 6

**DEC-0072 — Trilha de dados D1: curadoria de cômodos e medidas com fontes (proposta)**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (pedido) / Agente (proposta de método) · Categoria: Dados
Contexto: os 12 tipos do catálogo e seus mínimos foram definidos sem pesquisa, a partir de cômodos lembrados pelo responsável e de valores provisórios do Agente.
Decisão proposta: uma trilha de dados **paralela ao M1**, sem código, que entrega:
1. `docs/theory/room-program.md`: síntese com referências sobre os tipos de cômodo residenciais (inclusive atípicos e de alto padrão), destino, zona, dimensões e áreas mínimas usuais, circulações e vãos de porta;
2. `data/room_types.yaml` revisado, com **fonte, versão e data em cada valor** (DEC-0024).
Fontes a buscar:
- ABNT NBR 15575-1 (anexo de dimensões e mobiliário mínimos);
- ABNT NBR 9050 (circulação e acessibilidade);
- códigos de obras municipais de várias cidades (variam entre si);
- Neufert, *A arte de projetar em arquitetura*;
- Panero & Zelnik, *Dimensionamento humano para espaços interiores*;
- especificações da Caixa para habitação de interesse social;
- literatura acadêmica.
Método: skill `deep-research` (subagentes de busca na web), com verificação cruzada entre fontes.
Ressalvas:
- normas pagas não são copiadas, só os valores com a citação;
- a legislação é municipal e varia, então o catálogo guarda **referências usuais**, não conformidade (DEC-0015).
Status: Proposta (aguardando o responsável autorizar a execução).

**DEC-0073 — Plano do M1 (gerador CP-SAT)**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente · Categoria: Arquitetura
Decisão proposta: `docs/plans/m1-cpsat-generator.md`, com 7 tarefas:
1. pendências do M0;
2. modelo do pedido;
3. checagem de acesso;
4. nota decomposta e diversidade;
5. modelo CP-SAT;
6. laço de alternativas;
7. CLI `generate` com página HTML de comparação.
Escolhas do Agente:
- diversidade **por construção** (proibir padrões de posição relativa já vistos);
- alternativas rejeitadas pelo validador são proibidas e o solver roda de novo;
- pesos numa fonte única (`WEIGHTS`), usada pela nota e pelo solver;
- tempo determinístico do CP-SAT para garantir reprodutibilidade;
- área-alvo padrão = mínimo × 1,25;
- passagem mínima de 900 mm;
- novos atributos no catálogo: `suite_access`, `wet`, `sun`;
- `Site.north` para o critério solar.
Proposta de mudança de escopo: a **árvore de estados** passa do M1 para o M2, porque com uma única etapa não há o que navegar.
Status: Proposta (aguardando revisão e o modo de execução).

### Pendências abertas (S03) — atualização 6

- Responsável: revisar o plano do M1, aprovar ou não a mudança da árvore de estados para o M2 e escolher o modo de execução.
- Responsável: autorizar a trilha D1 (pesquisa de cômodos e medidas).

### Log da sessão — continuação 7

8. **Responsável:** pediu a D1 antes do M1, para o M1 já usar os dados coletados, e avisou que haverá outras coletas ao longo do projeto. Pediu pesquisa além de destino, zona, larguras, áreas, circulação e portas: inventariar tudo o que o projeto precisará de material externo, incluindo o que ele esqueceu de listar. Definiu um novo tipo de dado: **custo de materiais em R$** por classe (econômica "dá pro gasto", média "já é boa", alto padrão), para estimar no futuro o custo de material da planta por quantidades. São exemplos: área de parede, reboco de parede e teto com cimento, cal ou gesso, classes de tinta, cerâmica e porcelanato, louças, metais, elétrica e hidráulica. A mão de obra fica de fora, mas estimável. Aprovou diversidade por construção, rejeição com nova tentativa, reprodutibilidade por semente e a árvore de alternativas no M2. Autorizou os 2 commits e o push. Escolheu execução nativa com revisão depois da tarefa 5 e no fim, começando o M1 logo após a D1. **Agente:** fez os commits `74c9f02` e `169d1f9` e o push do branch `feat/m1-cpsat-generator`. Executou a D1 com a skill `deep-research`: 5 frentes em paralelo (programa de cômodos; circulação, aberturas e garagem; implantação e conforto; custos de materiais; mobiliário, ergonomia e inventário), mais um relatório com citações. Estruturou o registro de dados:
   - `data/sources.yaml` (24 fontes com tipo);
   - `data/room_types.yaml` v0.2 (22 tipos, com fonte por valor);
   - `data/costs/` (consumo SINAPI, preços datados, classes);
   - `data/README.md` (dicionário e processo);
   - `model/sources.py`, e o `load_catalog` passou a recusar valor sem fonte.

   Em TDD, foram 7 testes novos no catálogo e 2 no registro. Ajustou a planta de teste porque o banheiro de 1,30 m útil ficou abaixo do novo mínimo, que tem fonte. Ao fim, 50 testes passando e `pyright` sem erros. Registrou DEC-0074 a DEC-0076.

### Decisões — continuação 7

**DEC-0074 — D1 concluída: registro de dados de referência com fonte por valor**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (pedido) / Agente (estrutura e valores) · Categoria: Dados
Substitui: DEC-0072 (status).
Decisão:
- **Pesquisa:** `docs/research/Dados de referência para plantas.md`, com notas em `docs/research/notes/…`. Traz um inventário de 28 categorias de dados por fase, valores com fonte e 19 lacunas priorizadas.
- **Achado central:** não existe área mínima nacional por cômodo. A NBR 15575-1 não fixa áreas, só mobiliário, folgas e três larguras. A área mínima real é **consequência do mobiliário mais as folgas**, e o validador de "cabe?" entra com o mobiliário (M8).
- **Registro:** `data/sources.yaml` é a fonte única das citações, com os tipos N, L-fed, L-mun, F, A, P e X. O catálogo cita uma fonte por valor, e código e teste recusam valor sem fonte ou com fonte desconhecida.
- **Catálogo v0.2:**
  - 22 tipos;
  - novos atributos `description`, `wet`, `sun`, `exterior`, `concentrated_use`, `stay` (permanência), `suite_access`, `comfort_area_m2` e `sources`;
  - perfil padrão "piso nacional", o mais exigente entre o anexo da NBR 15575-1 e o MCMV;
  - por isso o banheiro passa a ter largura mínima de 1,50 m (MCMV) e a sala de 2,40 m (era 2,70 m sem fonte);
  - `min_area_m2` só onde há fonte;
  - a área-alvo do gerador vem de `comfort_area_m2`.
- **Propostas do Agente para revisão do responsável:**
  - escritório e home theater continuam **atravessáveis**, como na DEC-0060, com `concentrated_use` (o relatório sugeria torná-los privativos);
  - rouparia, despensa e depósito ficam privativos, porque são anexos de guarda e não caminho;
  - suíte é uma relação (`suite_access`) e não um tipo, com base na definição de Porto Alegre;
  - varanda e área gourmet usam `exterior: true` em vez de uma quarta zona;
  - largura do closet de 1,30 m = armário de 0,50 m (NBR) + circulação de 0,80 m.
- Cômodos sem nenhuma fonte (home theater, área gourmet, rouparia, despensa, brinquedoteca e outros) ficam **sem números**.
- **Processo:** as próximas coletas são trilhas `Dn`, conforme o `data/README.md` e a regra no CLAUDE.md.

Estado (DEC-0069): **concluída** como primeira coleta. Ela é suficiente para o M1, porque o gerador usa largura mínima, área mínima, faixa de conforto, passagem, `suite_access`, `wet` e `sun`, e todos já têm fonte ou estão explicitamente vazios. As lacunas (texto oficial das normas, licença do SINAPI, códigos municipais, Neufert e Panero, mobiliário de mercado) **não bloqueiam** o M1 e viram as próximas trilhas `Dn`.
Status: Aprovada (as propostas do Agente acima aguardam revisão).

**DEC-0075 — Custo de materiais: esquema, classes e primeira coleta**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável (ideia e classes) / Agente (esquema) · Categoria: Dados / Produto
Decisão:
- **Objetivo de produto:** estimar o custo de **material** da planta a partir de quantidades (paredes, faces de reboco, teto, piso, contagens), com classes escolhidas pelo usuário (econômica, média, alto); a mão de obra entra depois.
- **Base:** composições SINAPI (Caixa/IBGE), que trazem consumo por m² com perdas e horas de mão de obra. O CUB e o custo médio do IBGE servem só para checar a ordem de grandeza.
- **Esquema em `data/costs/`:**
  - `consumption.yaml`: serviço → materiais por unidade, com o `driver` de quantidade;
  - `prices.yaml`: preços com mês de referência, abrangência e tipo `sinapi` ou `varejo`, mais as referências de verificação;
  - `finish_classes.yaml`: NBR 15079 para tintas (econômica 70, standard 90, premium 110, super premium 150 m²/18 L) mapeada para as 3 classes do projeto, e uma proposta do Agente para pisos.
- **Primeira coleta:** 8 serviços (alvenaria, chapisco, reboco cimento+cal, gesso projetado, contrapiso, porcelanato, massa corrida, pintura premium) e 14 registros de preço.
- **Pendências:**
  - confirmar a licença de reuso do SINAPI;
  - montar o ETL por UF;
  - coletar as composições de teto, azulejo, selador, hidráulica, elétrica, louças e metais por classe;
  - decidir se fundação, estrutura e cobertura entram no escopo, já que não saem de uma planta 2D.
Status: Aprovada (implementação do estimador em fase futura).

**DEC-0076 — Plano do M1 aprovado, com ajustes**
Data: 2026-11-11 · Sessão: S03 · Autor: Responsável · Categoria: Arquitetura / Processo
Substitui: DEC-0073 (status).
Decisão: aprovados:
- diversidade por construção;
- rejeitar e tentar de novo as plantas que falham no acesso ou na validação;
- reprodutibilidade por semente;
- **árvore de alternativas movida para o M2**;
- execução **nativa** com revisão independente **depois da tarefa 5 e no fim**;
- commits durante a execução e push autorizados.

Ajustes que vêm da D1 (rulings registrados no ledger da execução):
- os atributos `suite_access`, `wet` e `sun` já entraram no catálogo pela D1, então as tarefas 3 e 4 só os consomem;
- a área-alvo padrão passa a ser o limite inferior de `comfort_area_m2` e, sem ele, `min_area_m2 × 1,25`;
- os IDs duplicados no catálogo, pendência da tarefa 1, já foram resolvidos na D1.
Status: Aprovada.

### Pendências abertas (S03) — atualização 7

- Responsável: revisar as propostas do Agente na DEC-0074 (passagem de escritório e home theater, anexos privativos, suíte como relação, `exterior`, closet de 1,30 m) e o perfil "piso nacional" (banheiro de 1,50 m).
- Agente: executar as tarefas do M1.

### Log da sessão — continuação 8

9. **Responsável:** pediu para continuar a tarefa. **Agente:** executou o M1 em modo nativo, com TDD.
   - **Tarefas 1 a 4:** pendências do M0, pedido, acesso, nota e diversidade.
   - **Tarefa 5 (CP-SAT):** medições levaram o tempo-limite padrão a 0,5 unidade determinística e ao uso de `interleave_search`, sem o qual 8 threads davam resultados diferentes a cada execução.
   - **Revisão intermediária** (subagente): 4 problemas importantes, corrigidos com teste vermelho → verde. Eram passagem real ≥ 0,90 m, diversidade sem "falsos diferentes" por relação diagonal, lado mínimo universal de 1,10 m e vão entre cômodos de 0 ou ≥ 0,90 m.
   - **Tarefa 6:** o perfil mostrou 6 de 10 soluções rejeitadas por ilhas de acesso. A restrição de **fluxo de conectividade** levou a 0 rejeições e K=4 em ~20 s.
   - **Tarefa 7:** comando `generate`, SVG e página de comparação. A execução real revelou uma quebra no console cp1252 do Windows, corrigida com teste.
   - **Revisão final** (subagente): 2 problemas importantes e 1 menor reclassificado, todos corrigidos com teste. Eram mínimos do lavabo vindos de lei municipal, traceback para pedido inválido e falha silenciosa com nenhuma alternativa.
   - Registrou DEC-0077 e DEC-0078.

### Decisões — continuação 8

**DEC-0077 — Declaração: M1 concluído**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente (conferência visual a cargo do Responsável) · Categoria: Processo / Arquitetura
Decisão: o M1 está **concluído** segundo a DEC-0069, com a conferência visual do responsável pendente:
- 7 de 7 tarefas feitas;
- 103 testes passando e `pyright` sem erros;
- revisão intermediária e revisão final independentes, sem críticos e com os importantes corrigidos;
- conferência visual do agente em `report.html`;
- README e DECISOES atualizados.

Entrega: a partir de um pedido em JSON, gera K plantas **válidas** (geometria + acesso), **realmente diferentes** (≥ 15% dos pares com posição relativa trocada) e **reprodutíveis** por semente, com nota decomposta em 6 critérios, em JSON, DXF e HTML.

Por que é suficiente para o M2: a interface vai consumir exatamente o modelo de pedido, `generate_alternatives`, a nota decomposta e o SVG.

Decisões de execução que mudaram o plano (rulings):
- tempo-limite de 0,5 unidade determinística, com `interleave_search`;
- fluxo de conectividade dos cômodos atravessáveis;
- lado mínimo universal de 1,10 m;
- vão de 0 ou ≥ 0,90 m entre cômodos;
- diversidade só por "troca de lado";
- a CLI imprime o tempo total.

Desempenho real com 8 cômodos: K=4 levou 19,9 s, 59,6 s e 33,3 s em três execuções (mesmas plantas). A variação vem da carga da máquina, e a meta de ~20 s só é atingida com a máquina livre.

Limites de qualidade observados (vão para o M2 ou um M1.1):
- silhueta recortada (compacidade 0,83–0,92);
- a casa "flutua" no lote, sem preferência pelo recuo frontal;
- a circulação vira uma célula de 1,10 × 1,10 m, e não um corredor;
- rótulos se sobrepõem em cômodos pequenos.

Pendências menores: estão listadas no ledger da execução e no relatório final da sessão.
Status: Aprovada (aguarda a conferência visual do responsável e o merge).

**DEC-0078 — Lavabo sem mínimos como padrão nacional**
Data: 2026-11-11 · Sessão: S03 · Autor: Agente (achado da revisão final) · Categoria: Dados
Corrige: DEC-0074 (valores do lavabo).
Decisão: o lavabo perde `min_width_mm` (1,00 m) e `min_area_m2` (1,5 m²). Ambos vinham da lei de BH, válida só em BH e só para multifamiliar, o que viola a regra 4 do `data/README.md`. Fica só a faixa de conforto de 1,2–1,7 m² (P). Dois testes passam a barrar essa situação: fonte `L-mun` como mínimo padrão, e faixa de conforto abaixo do mínimo.
Status: Aprovada.

### Pendências abertas (S03) — atualização 8

- Responsável: abrir `out/m1/report.html` e um `alt-N.dxf` (conferência visual do M1), fazer push, abrir o PR e o merge.
- Responsável: revisar as propostas da DEC-0074 e os limites de qualidade da DEC-0077, e decidir se viram um M1.1 antes do M2.

---

## Sessão S04 — 2026-11-12

### Log da sessão (prompts e ações, em resumo)

1. **Responsável:** leu o relatório da D1 e concordou que a área mínima é consequência do mobiliário mais as circulações. Pediu uma verificação de "cabe?" durante a definição dos cômodos. Disse que as divergências entre fontes não limitam nada: servem para um piso conservador, uma média ou mediana, ou um mínimo escolhido pelo usuário. O objetivo é evitar plantas sem sentido e dezenas de perguntas. Aprovou as seis propostas da DEC-0074.
   Sobre o `report.html` do M1:
   - o terreno era grande para o programa, então centralizar fazia sentido; em lote menor, o motor deveria encostar numa lateral ou na frente, respeitando o vizinho e as aberturas;
   - pediu **muro em todo o perímetro do lote**;
   - perguntou por que as silhuetas são irregulares e por que quase não há paredes na mesma reta. Lembrou que 3 quartos alinhados com as mesmas medidas são mais fáceis de construir, sem forçar o usuário;
   - não entendeu os vazios internos sem acesso: só fariam sentido como jardim de inverno, e indicados;
   - pediu um esquema de **3 a 4 cores**: 2 para os cômodos, 1 para a área externa construída e 1 para a área verde.

   Pediu ao Agente para tomar as 3 decisões pendentes e julgar a necessidade de M1.1 e M1.2.

   **Agente:** explicou que as formas irregulares não são um bug, e sim uma lacuna do modelo: nada pedia bloco cheio, alinhamento ou posição no lote. Tomou as 3 decisões (DEC-0079 a DEC-0081). Acrescentou ao design a seção 20 (M1.1 e M1.2) e os marcos M1.1 e M1.2. Registrou DEC-0079 a DEC-0083.

### Decisões

**DEC-0079 — Aprovação das propostas da DEC-0074**
Data: 2026-11-12 · Sessão: S04 · Autor: Responsável · Categoria: Dados / Produto
Decisão: ficam aprovadas:
- escritório e home theater atravessáveis, com `concentrated_use`;
- rouparia, despensa e depósito privativos;
- suíte como relação (`suite_access`);
- atributo `exterior` em vez de uma quarta zona;
- closet com largura mínima de 1,30 m;
- perfil "piso nacional", com banheiro de 1,50 m.
Status: Aprovada.

**DEC-0080 — M1 encerrado; integração via pull request**
Data: 2026-11-12 · Sessão: S04 · Autor: Agente (por delegação do Responsável) · Categoria: Processo
Complementa: DEC-0077.
Decisão: o responsável conferiu as 4 plantas no `report.html`. O M1 fica **concluído como gerador funcional**: as plantas são válidas, diferentes, reprodutíveis e têm nota. Os problemas de qualidade apontados (forma, alinhamento, vazios, implantação) são o escopo do **M1.1** e não bloqueiam o encerramento. O branch `feat/m1-cpsat-generator` vai para o `main` pela **opção 2**: o responsável faz o push e abre o PR, como no M0. O M1.1 começa num branch novo, a partir do `main` atualizado.
Status: Aprovada.

**DEC-0081 — Filosofia dos dados: piso conservador, mediana ou escolha do usuário**
Data: 2026-11-12 · Sessão: S04 · Autor: Responsável · Categoria: Dados / Produto
Complementa: DEC-0074.
Decisão: as divergências entre fontes não precisam ser resolvidas. Os dados oferecem **perfis de mínimo**:
- **conservador** (padrão): o maior mínimo entre as fontes;
- **mediana** das fontes;
- **personalizado**: o valor que o usuário informar.

O objetivo é o motor decidir a partir do pouco que o usuário informa, sem gerar plantas sem sentido para aquele pedido e sem uma longa sequência de perguntas.
Status: Aprovada.

**DEC-0082 — M1.1: forma e implantação**
Data: 2026-11-12 · Sessão: S04 · Autor: Responsável (requisitos) / Agente (solução) · Categoria: Arquitetura / Produto / Interface
Decisão: o escopo está na seção 20.1 do design:
- critério de bloco cheio (`void_area`);
- rejeição de vazio interno não pedido (um pátio só existe se for pedido, e aí é rotulado);
- critério suave de alinhamento (faces na mesma reta, cômodos iguais enfileirados);
- implantação padrão encostada no recuo frontal e centralizada na largura;
- em lote pequeno, encostar automaticamente numa divisa, com aviso e lado marcado "sem janela" a menos de 1,5 m da divisa (Código Civil, art. 1.301);
- muro em todo o perímetro (`A-MURO`, 150 mm, valor a confirmar);
- 4 categorias de cor: interna seca, interna molhada, externa construída e externa verde;
- aviso de permeabilidade abaixo de 25%.

Propostas do Agente:
- implantação padrão;
- espessura do muro;
- as 2 cores dos cômodos serem seca × molhada (útil para a hidráulica), com a zona social/íntima/serviço ficando para o grafo de bolhas.
Status: Proposta (aguardando aprovação do design; depois, plano).

**DEC-0083 — M1.2: dimensionamento pelo mobiliário**
Data: 2026-11-12 · Sessão: S04 · Autor: Responsável (requisito) / Agente (solução) · Categoria: Arquitetura / Dados
Decisão: o escopo está na seção 20.2 do design:
- trilha de dados D2 (mobiliário mínimo e folgas por tipo de cômodo, com fonte, em `data/furniture.yaml`);
- verificação "cabe?" por empacotamento CP-SAT dentro de cada cômodo, que também deriva os mínimos;
- perfis de mínimo (DEC-0081);
- itens pedidos aumentam os mínimos do cômodo.

Isso antecipa parte do M6 (pré-dimensionamento) e do M8 (mobiliário). Ordem dos marcos: M1.1 → M1.2 → M2.
Status: Proposta (aguardando aprovação do design).

### Pendências abertas (S04)

- Responsável: push do branch `feat/m1-cpsat-generator`, abrir o PR e fazer o merge.
- Responsável: aprovar a seção 20 do design, incluindo as propostas da DEC-0082.
- Agente: depois da aprovação, escrever o plano do M1.1 (`docs/plans/m1-1-shape-and-site.md`) num branch novo a partir do `main`.

### Log da sessão — continuação

2. **Responsável:** fez o commit `f627f62` (só `docs/design/mvp.md`) e o push. Pediu como regra receber o título e o texto do PR sempre que um branch fechar; ele faz o merge depois de recebê-los. Aprovou a seção 20 do design (DEC-0082 e DEC-0083 passam a Aprovada) e pediu para iniciar o M1.1 e escrever o plano. **Agente:**
   - entregou o título e o texto do PR do M1 e registrou a regra no CLAUDE.md;
   - notou que a sessão S04 do DECISOES.md ficou fora do `f627f62` e a levou para o branch do M1.1;
   - criou o branch `feat/m1-1-shape-and-site` a partir da ponta do M1;
   - escreveu `docs/plans/m1-1-shape-and-site.md`.

### Decisões — continuação

**DEC-0084 — Regra: título e texto do PR ao fechar cada branch**
Data: 2026-11-12 · Sessão: S04 · Autor: Responsável · Categoria: Processo
Decisão: ao fechar um branch, o agente entrega o título e o texto do pull request, em inglês. O responsável abre o PR e faz o merge. Regra registrada no CLAUDE.md ("Arquivos e git").
Status: Aprovada.

**DEC-0085 — Seção 20 aprovada e plano do M1.1**
Data: 2026-11-12 · Sessão: S04 · Autor: Responsável (aprovação) / Agente (plano) · Categoria: Arquitetura
Substitui: DEC-0082 e DEC-0083 (status: Proposta → Aprovada).
Decisão:
- O responsável aprovou a seção 20 do design, incluindo as propostas do Agente: implantação no recuo frontal centralizada na largura, muro de 150 mm e cores seca × molhada.
- Plano proposto `docs/plans/m1-1-shape-and-site.md`, com 6 tarefas:
  1. dados de implantação com fonte e tipo `patio`;
  2. vazio fechado como erro de validade;
  3. forma no solver e na nota (implantação rígida, área vazia com peso 3,0, critério `alignment`);
  4. encosto automático em lote pequeno e marcação "sem janela";
  5. muro, área verde e 4 cores;
  6. verificação e fechamento.
- Escolhas do Agente no plano:
  - um pátio é um **cômodo** do tipo `patio`, nunca um vazio;
  - ordem do encosto automático: esquerda, depois as duas laterais, depois o fundo;
  - permeabilidade de 25% só como aviso, com a cidade citada (lei municipal, regra 4);
  - cores únicas em `CATEGORY_STYLE`: seca laranja, molhada azul, construída cinza, verde verde.

Status: Plano Proposto (aguardando revisão, modo de execução e autorização de commits).

### Pendências abertas (S04) — atualização

- Responsável: fazer o merge do PR do M1, com o texto entregue nesta rodada.
- Responsável: revisar o plano do M1.1, escolher o modo de execução e autorizar os commits.
