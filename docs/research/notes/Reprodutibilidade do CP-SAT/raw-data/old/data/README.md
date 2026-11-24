# Dados de referência

Versão: 0.2 · Atualizado em: 2026-11-11

Dados curados que o motor lê como **conhecimento a priori**: valores padrão quando o usuário não informa algo. Todo valor tem **fonte, versão e data** (DEC-0024). A pesquisa completa que originou estes arquivos está em [docs/research/](../docs/research/).

## Arquivos

| Arquivo | Conteúdo | Lido por |
|---|---|---|
| `sources.yaml` | Registro de fontes. É a **fonte única** das citações | `model/sources.py` e testes |
| `room_types.yaml` | Catálogo de tipos de cômodo: zona, passagem, atributos, mínimos, faixa de conforto | `model/catalog.py` (gerador, validador, DXF) |
| `costs/consumption.yaml` | Consumo de material por unidade de serviço (composições SINAPI) | estimador de custo (fase futura) |
| `costs/prices.yaml` | Preços de insumos e referências de verificação (CUB, IBGE) | estimador de custo (fase futura) |
| `costs/finish_classes.yaml` | Classes de acabamento: econômica, média, alto | estimador de custo (fase futura) |

## Tipos de fonte (`kind`)

`N` norma ABNT · `L-fed` lei federal · `L-mun` lei municipal (vale só na cidade) · `F` programa federal ou referência oficial de custo · `A` acadêmico · `P` prática, mercado, popular · `X` proposta do agente, sem fonte externa.

## Regras

1. **Citação obrigatória.** Todo número do catálogo (`min_width_mm`, `min_area_m2`, `comfort_area_m2`) tem uma entrada em `sources` que aponta para um `id` de `sources.yaml`. `load_catalog` recusa o arquivo sem isso, e `tests/test_data_registry.py` confere todas as citações de `data/`.
2. **Sem número inventado.** Sem fonte, o campo fica vazio. Um valor derivado pelo agente usa a fonte `agente` (`X`) e precisa de fonte real antes de virar referência.
3. **Normas pagas.** Guardamos só o valor e a citação; o texto da norma não entra no repositório.
4. **Legislação municipal** entra como referência ou, no futuro, como perfil opcional, **nunca** como padrão nacional.
5. **Preços** têm mês de referência (`reference_month`), abrangência (`scope`: UF, cidade ou média nacional) e tipo (`sinapi` ou `varejo`). Preço zerado é inválido. Varejo é amostra indicativa.
6. **Versão:** cada arquivo tem `version` e `updated`; mudanças de valor são registradas no DECISOES.md.

## Perfil padrão do catálogo

"Piso nacional": o mais exigente entre o anexo de mobiliário da NBR 15575-1 e o MCMV, quando ambos existem. A NBR não fixa área mínima de cômodo; por isso `min_area_m2` só existe quando há fonte, e a área-alvo do gerador vem de `comfort_area_m2`. A conclusão central da pesquisa é que **a área mínima real de um cômodo é consequência do mobiliário mais as folgas**; o validador de "cabe o mobiliário?" entra com o mobiliário (M8).

## Esquema de custos

Separa **o que se consome** (`consumption.yaml`: serviço → materiais com quantidade por unidade, perdas incluídas), **quanto custa** (`prices.yaml`: item → preço por mês e abrangência) e **qual variante cada classe usa** (`finish_classes.yaml`). O `driver` de cada serviço é a grandeza que a planta fornece: `wall_area_net`, `wall_face_area_net`, `floor_area` etc. Mão de obra fica de fora; as composições SINAPI trazem as horas, então ela pode ser estimada depois sem mudar o esquema. Plano futuro: um ETL que importa o XLSX mensal do SINAPI de uma UF e grava um subconjunto curado (licença de reuso ainda a confirmar).

## Como fazer uma nova coleta de dados (trilha `Dn`)

1. **Inventário:** listar quais dados a fase seguinte precisa (ver a tabela de 28 categorias no relatório D1).
2. **Pesquisa:** skill `deep-research`; notas em `docs/research/notes/<título>/` e relatório em `docs/research/<título>.md`.
3. **Estruturação:** promover para `data/` só o que uma fase vai ler, com `sources` em cada valor.
4. **Teste:** `pytest` (o teste de registro barra citação desconhecida).
5. **Registro:** DECISOES.md (decisão da trilha e mudanças de valor) e este README.

Lacunas e próximas coletas: seção final de [docs/research/Dados de referência para plantas.md](../docs/research/Dados%20de%20refer%C3%AAncia%20para%20plantas.md).
