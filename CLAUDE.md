# CLAUDE.md — Regras do agente

> Arquivo administrado pelo responsável pelo projeto. O agente pode **sugerir** mudanças, mas não altera estas regras por conta própria.

## Projeto — PyGridPlan

Gerador de plantas baixas residenciais 2D, offline, a partir de entradas estruturadas e texto livre. É um projeto de portfólio e estudo (arquitetura de software, geometria computacional, otimização, estatística e IA aplicada). As fases 3D e complementares vêm depois. Contexto completo: [DECISOES.md](DECISOES.md).

## Comunicação

- Responder sempre em **português (Brasil)**.
- Ser um desenvolvedor crítico: apontar problemas, propor alternativas melhores e diferenciar fatos, hipóteses e decisões.
- Não inventar resultados de testes, funcionalidades ou capacidades de bibliotecas.

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

## Fluxo de trabalho

1. Ler este arquivo e o DECISOES.md.
2. Propor antes de implementar e implementar só o escopo acordado.
3. Testar. Uma funcionalidade só está concluída com testes passando.
4. Atualizar a documentação e o DECISOES.md.
5. Reportar de forma objetiva.
