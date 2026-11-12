# CLAUDE.md — Regras do agente

> Arquivo administrado pelo responsável pelo projeto. O agente pode **sugerir** mudanças, mas não altera estas regras por conta própria.

## Projeto — PyGridPlan

Gerador de plantas baixas residenciais 2D, offline, a partir de entradas estruturadas e texto livre. É um projeto de portfólio e estudo (arquitetura de software, geometria computacional, otimização, estatística e IA aplicada). As fases 3D e complementares vêm depois. Contexto completo: [DECISOES.md](DECISOES.md).

## Comunicação

- Responder sempre em **português (Brasil)**.
- Ser um desenvolvedor crítico: apontar problemas, propor alternativas melhores e diferenciar fatos, hipóteses e decisões.
- Não inventar resultados de testes, funcionalidades ou capacidades de bibliotecas.
- **Encerramento de fase explícito.** Toda etapa, fase ou marco termina com uma declaração clara de estado: **concluída**, **pausada** (funcional, com acréscimos previstos) ou **em andamento**. A declaração justifica por que a fase é suficiente e funcional, com evidência (testes, revisão, conferência visual), e lista o que fica pendente e se bloqueia a fase seguinte. Só se passa para a próxima fase depois dessa declaração.
- **Definição de pronto de um marco:** todas as tarefas do plano feitas; suíte de testes e `pyright` sem falhas; revisão final independente com os achados críticos e importantes corrigidos; conferência visual aprovada pelo responsável quando houver saída visual; README e DECISOES.md atualizados; pendências menores listadas.
- **Toda resposta termina com "Próximos passos"**, separados em **Responsável** e **Agente**.

## Registro obrigatório — DECISOES.md

- **Sempre** registrar no [DECISOES.md](DECISOES.md), em ordem cronológica, tudo o que mudar no projeto: prompts do responsável, decisões, sugestões, alterações e construções do agente. Registrar ao fim de cada rodada, sem esperar o pedido.
- O arquivo é **append-only**. Nunca apagar nem reescrever entradas antigas. Para substituir uma decisão, criar uma nova que referencie a anterior (`Substitui: DEC-NNNN`).
- Nunca registrar chaves, tokens, senhas ou segredos.

### Estrutura obrigatória

Cada sessão de trabalho abre uma seção com três blocos:

```markdown
## Sessão SNN — AAAA-MM-DD

### Log da sessão (prompts e ações, em resumo)
1. **Responsável:** <o que pediu/disse>. **Agente:** <o que fez/respondeu>.

### Decisões
**DEC-NNNN — <título curto>**
Data: AAAA-MM-DD · Sessão: SNN · Autor: Responsável | Agente | Responsável (proposta do Agente) · Categoria: <Escopo | Arquitetura | IA | Produto | Interface | Processo | Ferramentas | ...>
Contexto: <por que a decisão surgiu> (opcional quando óbvio)
Decisão: <o que foi decidido>
Justificativa: <por quê> (opcional quando óbvio)
Consequências: <o que muda / o que fica pendente> (opcional)
Status: Proposta | Aprovada | Aprovada (detalhe a definir) | Substituída por DEC-NNNN | Revogada

### Pendências abertas (SNN)
- <item>
```

- A numeração `DEC-NNNN` é contínua no projeto inteiro e não recomeça por sessão. As sessões são numeradas `S01`, `S02`…
- Se a sessão continuar depois de um registro, acrescentar novos itens ao log e novas decisões, sem editar os anteriores.
- Diferenciar o que o responsável decidiu do que o agente propôs ou assumiu.

## Arquivos e git

- **Nunca excluir, sobrescrever ou descartar** arquivos ou alterações do responsável sem autorização explícita.
- **Commits só com autorização explícita.** Mensagens em inglês, no padrão Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `build:`, `chore:`.
- **Plano de commits antes de commitar.** Antes de qualquer commit, o agente mostra a lista dos commits sugeridos: a mensagem de cada um e os arquivos que entram em cada um. Só depois da confirmação do responsável o agente executa `git add` e `git commit`. O **`git push` é sempre feito pelo responsável**; o agente nunca faz push.

## Princípios de arquitetura

- A IA é **separada** do motor geométrico. Ela interpreta o pedido e preenche um JSON validado; a geometria é sempre determinística.
- O app funciona **offline** e não depende de API paga.
- O modelo central de dados é a fonte da verdade. DXF, tela e o futuro 3D são representações derivadas dele.
- 2D primeiro. Nada de 3D antes de um modelo 2D consistente.
- Simplicidade sem engenharia excessiva. Não adicionar dependências sem justificativa.
- Código enxuto: ver a skill `karpathy-guidelines` na seção "Skills e plugins".

## Estrutura de pastas

| Pasta | Conteúdo |
|---|---|
| `src/pygridplan/` | motor Python |
| `web/` | interface TypeScript |
| `data/` | dados de referência versionados (catálogo de cômodos, medidas), cada valor com fonte, versão e data |
| `tests/` | testes; `tests/fixtures/` guarda os casos de referência |
| `docs/design/` | documentos de design e `mockups/` aprovados |
| `docs/plans/` | planos de implementação, um por marco |
| `docs/research/` | pesquisas: relatório `<título>.md` + `notes/<título>/` (skill `deep-research`) |
| `docs/theory/` | fundamentação teórica |
| `out/` | saídas geradas (DXF, projetos salvos), fora do git |
| `.superpowers/`, `.playwright-mcp/` | rascunhos das ferramentas do agente, fora do git; não guardar nada importante ali |

- Nomes de pastas e arquivos em inglês, em minúsculas com hífen; o conteúdo dos documentos é em português.
- **Sem data no nome dos arquivos.** Data de criação, de atualização e versão ficam no cabeçalho do documento; o histórico fica no git.
- Os locais acima **substituem os padrões das skills** (ex.: `docs/superpowers/specs/` → `docs/design/`, `docs/superpowers/plans/` → `docs/plans/`).
- Um mockup aprovado é copiado de `.superpowers/` para `docs/design/mockups/`.
- Não criar pastas vazias nem arquivos "para o futuro": cada pasta nasce com seu primeiro arquivo.
- **Coleta de dados em trilhas `Dn`** (DEC-0074): inventário → pesquisa em `docs/research/` → promoção para `data/` só do que uma fase lê, com fonte por valor (`data/sources.yaml`) → teste de registro → DECISOES.md. Processo detalhado em `data/README.md`. Nunca inventar valores; sem fonte, o campo fica vazio.
- O **README.md** mantém sempre atualizada a estrutura macro (software e dados, com paths e o marco de cada pasta). Toda pasta nova ou mudança de estrutura atualiza o README na mesma rodada.

## Skills e plugins

Regras gerais: sugerir a skill adequada quando a fase pedir; recomendar só plugins que existem de fato; ler o conteúdo de plugins de terceiros antes de instalar; registrar no DECISOES.md toda instalação ou remoção.

| Skill / plugin | Origem | Situação | Finalidade e regra de uso |
|---|---|---|---|
| `superpowers:brainstorming` | `superpowers` (oficial) | em uso | antes de criar ou mudar funcionalidade; o design vai para `docs/design/` |
| `superpowers:writing-plans` | `superpowers` | próxima | depois do design aprovado; um plano por marco em `docs/plans/` |
| `superpowers:test-driven-development` | `superpowers` | a usar | toda implementação: teste primeiro |
| `superpowers:systematic-debugging` | `superpowers` | a usar | qualquer bug ou teste falhando, antes de propor correção |
| `superpowers:verification-before-completion` | `superpowers` | a usar | antes de dizer "pronto" ou propor commit: rodar os testes e mostrar o resultado |
| `superpowers:requesting-code-review` / `receiving-code-review` | `superpowers` | a usar | ao fim de cada marco |
| `superpowers:executing-plans` / `subagent-driven-development` | `superpowers` | a usar | execução dos planos; o responsável escolhe o modo |
| `karpathy-guidelines` | `andrej-karpathy-skills` (comunidade, MIT) | em uso | ao escrever, revisar ou refatorar código: o mínimo que resolve, nada especulativo, sem redundância de definições ou armazenamento, mudanças cirúrgicas, meta verificável. **Nunca** corta testes nem validações |
| `frontend-design` | oficial | instalado | M2–M3: interface com qualidade de produto, seguindo o mockup aprovado |
| `playwright` | oficial | instalado | testes de ponta a ponta e screenshots da interface |
| `pyright-lsp` | oficial | instalado (pyright 1.1.414 via npm) | checagem de tipos do Python enquanto o código é escrito |
| `code-simplifier` | oficial | instalado | revisão de simplificação depois de implementar, junto com a karpathy |
| `playground` | oficial | instalado | páginas HTML interativas que montam um texto/JSON a partir de controles visuais (não executam o motor). Uso previsto: montar pedidos de teste e explorar pesos de critérios |
| `anthropic-skills:deep-research` | Anthropic | a usar na trilha D1 | pesquisa em várias fontes com relatório citado (curadoria de cômodos, medidas e normas) |
| `typescript-lsp` | oficial | instalar no M2 | checagem do TypeScript da interface |
| `modern-web-guidance` | oficial | instalar no M2 | boas práticas web atuais na interface |
| `mcp-server-dev` | oficial | instalar na fase MCP | servidor MCP básico (durante o desenvolvimento) e aprofundado (fim do projeto) |

Não há, até agora, skill confiável específica de otimização (CP-SAT/OR-Tools); se surgir, avaliar e registrar.

## Fluxo de trabalho

1. Ler este arquivo e o DECISOES.md.
2. Propor antes de implementar e implementar só o escopo acordado.
3. Testar. Uma funcionalidade só está concluída com testes passando.
4. Atualizar a documentação e o DECISOES.md.
5. Reportar de forma objetiva.
