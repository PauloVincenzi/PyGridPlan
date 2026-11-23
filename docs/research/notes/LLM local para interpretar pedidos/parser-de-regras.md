# Parser de regras em português (pt-BR) antes e junto de um LLM pequeno — arquitetura híbrida "regras primeiro, LLM para o resto"

> Nota de pesquisa · criada em 2026-11-23 · estado de nov/2026 · versões conferidas no PyPI e na API do GitHub em 2026-11-22/23.
> Rótulos: [FATO] = verificado em fonte ou em teste local reproduzível; [HIPÓTESE] = plausível, não verificado; [OPINIÃO] = recomendação do pesquisador.
> **Testes locais:** text2num 3.1.0 e rapidfuzz 3.14.6 foram instalados num diretório isolado do scratchpad e executados com `python -I` (Python 3.13.14, Windows). Nada foi instalado no projeto. As saídas citadas como "teste local" foram copiadas literalmente do console.

## 1. Ferramentas Python para normalizar e casar texto em português: qual dependência compensa?

### Takeaway
Para um vocabulário fechado (cerca de 23 tipos de cômodo, relações e medidas), basta **`unicodedata` (biblioteca padrão) + `re` + uma tabela de sinônimos versionada em `data/` + `rapidfuzz` só para erros de digitação**. spaCy, Stanza e o RSLP são pesados ou não resolvem o que importa aqui (lematizar "quartos"→"quarto" se faz com uma regra de plural, e o NER deles reconhece pessoas e lugares, não cômodos). [OPINIÃO]

### Cited Findings
- [FATO] `unicodedata.normalize("NFD", s)` seguido da remoção dos caracteres de categoria `Mn` tira os acentos usando só a biblioteca padrão — [Python docs: unicodedata](https://docs.python.org/3/library/unicodedata.html)
- [FATO] **Unidecode 1.4.0** (24/04/2025) é **GPLv2+**; os classifiers vão só até o Python 3.11; o próprio FAQ sugere `text-unidecode` para quem não pode usar GPL — [PyPI Unidecode](https://pypi.org/project/Unidecode/)
- [FATO] `text-unidecode` 1.3 é de 30/08/2019 (sem release desde então), licença Artistic — [PyPI JSON text-unidecode](https://pypi.org/pypi/text-unidecode/json)
- [FATO] **RapidFuzz 3.14.6** (30/08/2026), MIT, Python ≥ 3.11, wheels até o CPython 3.15; tem `process.extractOne`/`extract`/`cdist` e os scorers `ratio`, `partial_ratio`, `token_sort_ratio`, `token_set_ratio`, `WRatio`, `QRatio`; no Windows precisa do VC++ 2019 redistributable — [PyPI rapidfuzz](https://pypi.org/project/rapidfuzz/). Repositório ativo (push em 09/11/2026, não arquivado) — [GitHub API rapidfuzz/RapidFuzz](https://api.github.com/repos/rapidfuzz/RapidFuzz)
- [FATO, teste local] `process.extractOne(q, escolhas, scorer=fuzz.WRatio, processor=utils.default_process)` com escolhas sem acento:
  - `"dormitório"` → `dormitorio` 90,0 · `"banhero"` → `banheiro` 93,3 · `"cosinha"` → `cozinha` 85,7 · `"area de servço"` → `area de servico` 89,7 · `"quartos"` → `quarto` 92,3 (resultado do teste local acima)
  - **Armadilhas:** `"sala"` → `sala de estar` com **90,0** (o WRatio usa casamento parcial, então qualquer prefixo curto pontua alto) e `"vaga"` → `garagem` 60,0 (o fuzzy **não** resolve sinônimos, só grafia) (resultado do teste local acima)
- [FATO] **spaCy 3.8.18** (26/10/2026), MIT, Python ≥ 3.10 e < 3.16 — [PyPI JSON spacy](https://pypi.org/pypi/spacy/json)
- [FATO] Os modelos portugueses mais recentes são **`pt_core_news_sm/md/lg` 3.8.0**, publicados em 30/09/2024. Wheel de **13,0 MB (sm), 42,4 MB (md) e 568,2 MB (lg)**. Licença **CC BY-SA 4.0**. Componentes: tok2vec, morphologizer, parser, lemmatizer (treinável), senter, attribute_ruler, ner. Treinados com UD Portuguese Bosque v2.8 + WikiNER; md e lg trazem vetores fastText (OSCAR + Wikipedia). Não há pipeline `trf` para português — [GitHub API spacy-models release pt_core_news_sm-3.8.0](https://api.github.com/repos/explosion/spacy-models/releases/tags/pt_core_news_sm-3.8.0); [spaCy models/pt](https://spacy.io/models/pt)
- [FATO] Métricas publicadas para o `pt_core_news_sm` **3.7.0** (não conferi as da 3.8.0): NER F 0,880, lemma acc 0,968, UPOS 0,962 — [Hugging Face spacy/pt_core_news_sm](https://huggingface.co/spacy/pt_core_news_sm). O NER segue o esquema WikiNER (PER/LOC/ORG/MISC), que não tem rótulo de cômodo [FATO pela fonte de treino; consequência para o projeto: OPINIÃO].
- [FATO] **Stanza 1.15.1** (14/11/2026), Apache-2.0, Python ≥ 3.9, repositório muito ativo (push em 20/11/2026) — [PyPI JSON stanza](https://pypi.org/pypi/stanza/json); [GitHub API stanfordnlp/stanza](https://api.github.com/repos/stanfordnlp/stanza). Não conferi a lista de modelos pt nem o tamanho deles.
- [FATO] **NLTK 3.10.4** (21/10/2026), Apache-2.0 — [PyPI JSON nltk](https://pypi.org/pypi/nltk/json). O `RSLPStemmer` implementa o algoritmo de Orengo & Huyck (regras de plural, feminino, aumentativo, advérbio, nome e verbo); precisa dos arquivos de regras `stemmers/rslp` do NLTK data; o autor do porte diz que é "intended for demonstration and educational purposes only"; os radicais nem sempre são palavras ("risca"→"risc") — [NLTK rslp source](https://www.nltk.org/_modules/nltk/stem/rslp.html)
- [FATO] O **text2num 3.1.0** também serve como normalizador numérico (ver seção 2), mas troca "quarto(s)" por ordinal — [teste local; PyPI text2num](https://pypi.org/project/text2num/)

### Inferences
- [OPINIÃO] **Recomendação de dependências para a camada de regras:** nenhuma obrigatória além da biblioteca padrão. `rapidfuzz` (MIT, só wheels, sem modelo) vale como opcional para tolerar erro de digitação, com `score_cutoff` alto (≈ 85) e só **depois** do casamento exato na tabela de sinônimos.
- [OPINIÃO] spaCy `sm` (13 MB, CC BY-SA) só se justificaria se o projeto precisasse de dependência sintática, por exemplo para ligar "longe" ao par certo de cômodos em frases longas. Como o LLM já cobre o texto livre, essa necessidade some. A licença CC BY-SA do modelo (share-alike) também merece atenção num projeto de portfólio [HIPÓTESE sobre a implicação legal; a licença é FATO].
- [OPINIÃO] O plural em pt-BR se resolve com 3 ou 4 regras de sufixo sobre a forma sem acento ("-s", "-oes→-ao", "-is→-l", "-res→-r"). Também dá para listar o plural de cada sinônimo direto na tabela, o que é mais explícito e testável. Não é preciso stemmer.
- [OPINIÃO] Ordem do pipeline de normalização: `casefold()` → NFKC → guardar o mapa de offsets para o texto original (para a cobertura de spans e para destacar trechos na interface) → remover acentos numa cópia usada só para casamento.

```python
# ILUSTRATIVO — não testado
import re, unicodedata
def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
def norm(s: str) -> str:
    return re.sub(r"\s+", " ", sem_acento(unicodedata.normalize("NFKC", s).casefold())).strip()
# Sobre texto já em NFC, NFD + remoção de Mn preserva o comprimento em pt-BR (cada letra acentuada vira
# base + 1 marca removida). Mas norm() colapsa espaços e o NFKC pode mudar o comprimento (ex.: ligaduras),
# então, para a cobertura de spans, use uma versão sem o re.sub ou guarde um mapa de offsets explícito.
```

### Gaps
- Não medi a qualidade do lematizador do spaCy pt nos termos do domínio ("suítes", "banheiros", "dormitórios"); o modelo não foi baixado.
- Não encontrei as métricas oficiais do `pt_core_news_*` 3.8.0 (a API do GitHub limitou as requisições sem autenticação).

## 2. Extração de números e medidas em português: bibliotecas mantidas em 2026

### Takeaway
O **text2num 3.1.0** (MIT, ativo, suporta pt-BR e pt-PT) converte bem os números por extenso, mas **destrói a palavra "quarto"**, que vira o ordinal "4º" em qualquer contexto. Por isso não pode rodar sobre o texto inteiro. O mais seguro é **regex própria para medidas** ("12x30", "12 por 30", "12,5 m", "m²") e um **léxico pequeno de números por extenso** (0–100 + "meio/meia"), escrito à mão ou usando o `text2num()` só em spans já isolados. Duckling e Recognizers-Text não compensam. [OPINIÃO baseada nos FATOS abaixo]

### Cited Findings
- [FATO] **text2num 3.1.0** (21/08/2026), MIT, Python ≥ 3.8, wheels CPython 3.8–3.15; idiomas: dinamarquês, holandês, inglês, francês, alemão, italiano, **português (BR e PT)**, espanhol. API: `alpha2digit(texto, "pt")` e `text2num(palavra, "pt")` — [PyPI text2num](https://pypi.org/project/text2num/). Repositório ativo (último commit em 21/08/2026, não arquivado) — [GitHub API allo-media/text2num](https://api.github.com/repos/allo-media/text2num)
- [FATO, teste local] Assinatura real na 3.1.0: `alpha2digit(text, lang, threshold=3.0)`. **Não existe** o parâmetro `ordinal_threshold`: passá-lo gera `TypeError`.
- [FATO, teste local] Saídas de `alpha2digit(..., "pt")`:
  | Entrada | Saída |
  |---|---|
  | `casa com três quartos sendo uma suíte, dois banheiros, garagem pra dois carros, terreno doze por trinta` | `casa com 3 4ᵒˢ sendo uma suíte, dois banheiros, garagem pra dois carros, terreno 12 por 30` |
  | `quarto` / `o quarto` / `quartos grandes` | `4º` / `o 4º` / `4ᵒˢ grandes` |
  | `dois quartos de solteiro` | `dois 4ᵒˢ de solteiro` (com `threshold=0`: `2 4ᵒˢ de solteiro`) |
  | `quero um quarto` (threshold=0) | `quero 1 4º` |
  | `uns quinze metros quadrados pra sala` | `uns 15 metros quadrados pra sala` |
  | `doze vírgula cinco metros` | `12,5 metros` |
  | `terreno de doze por trinta e cinco` / `doze x trinta` | `terreno de 12 por 35` / `12 x 30` |
  | `duzentos e cinquenta metros quadrados` | `250 metros quadrados` |
  | `dois e meio metros` / `doze metros e meio` / `meia dúzia` | inalterados (**não** trata "e meio" nem "meia dúzia") |
  | `três banheiros` | `3 banheiros` |
  - Com o `threshold=3.0` padrão, "um/uma/dois" ficam por extenso ("dois banheiros") e "três" é convertido. Com `threshold=0`, tudo é convertido, mas "um" passa a virar "1" também em usos não numéricos ("1 terço"). `text2num("doze","pt")`=12, `"vinte e cinco"`=25, `"dois mil"`=2000.
- [FATO] **Duckling** mudou para `meta/duckling` no GitHub; não está arquivado; último commit em 15/03/2026 — [GitHub API facebook/duckling → meta/duckling](https://api.github.com/repos/facebook/duckling). É uma biblioteca Haskell rodada como servidor HTTP (`stack build`, `stack exec duckling-example-exe`, POST em `:8000/parse`), sem wrapper Python oficial — [GitHub meta/duckling](https://github.com/facebook/duckling)
- [FATO] As dimensões do Duckling para **PT** são `Distance, Duration, Numeral, Ordinal, Quantity, Temperature, Time, Volume`. **Não há dimensão de área (m²)** — [Duckling/Dimensions/PT.hs](https://github.com/facebook/duckling/blob/main/Duckling/Dimensions/PT.hs)
- [FATO] **Microsoft Recognizers-Text**: o repositório (MIT) não está arquivado (último commit em 23/01/2026), mas o README chama os pacotes Python de "(alpha)", e .NET é a plataforma primária ("contributions propagate to the other platforms with time") — [GitHub microsoft/Recognizers-Text](https://github.com/microsoft/Recognizers-Text); [GitHub API](https://api.github.com/repos/microsoft/Recognizers-Text). No PyPI, `recognizers-text`, `recognizers-text-number` e `recognizers-text-suite` estão em **1.0.2a2, de 12/11/2019**, sem release há 7 anos — [PyPI JSON recognizers-text-suite](https://pypi.org/pypi/recognizers-text-suite/json). O código-fonte Python tem uma pasta `portuguese` em `recognizers_number/number` — [GitHub API contents](https://api.github.com/repos/microsoft/Recognizers-Text/contents/Python/libraries/recognizers-number/recognizers_number/number)
- [FATO] **num2words 0.5.14** (17/12/2024), LGPL, faz a direção contrária (número→extenso) — [PyPI JSON num2words](https://pypi.org/pypi/num2words/json). Pode ser útil só para **gerar casos de teste** por extenso [OPINIÃO].

### Inferences
- [OPINIÃO] **Não usar `alpha2digit` sobre o texto inteiro.** Num domínio em que "quarto" é o substantivo mais importante, a troca por "4º" é um bug sério e silencioso. Se for usar o text2num, aplicar o `text2num()` só a um span que a regex já marcou como número por extenso (por exemplo, a palavra antes de um tipo de cômodo ou de "metros").
- [OPINIÃO] Um léxico próprio de 0–100 + centenas cabe em cerca de 40 linhas, cobre "e meio/meia" e "um/uma" contextuais, e evita a dependência. O text2num vale como **oráculo de teste** (comparar os dois em `tests/`), sem entrar no código de produção. É uma alternativa razoável se o responsável preferir menos código próprio.
- [OPINIÃO] Ambiguidade de "três quartos": em pt-BR, "três quartos" quase sempre quer dizer 3 dormitórios num pedido de casa; o sentido de fração (¾) é raro aqui. Regra: **número + substantivo de cômodo = contagem**. Só tratar como fração com unidade explícita ("três quartos do terreno"), e mesmo assim mandar para o LLM ou para confirmação.
- [OPINIÃO] Padrões de regex que valem testar (ilustrativos):

```python
# ILUSTRATIVO — não testado
NUM = r"(\d+(?:[.,]\d+)?)"
TERRENO = re.compile(rf"\b(?:terreno|lote)\b[^\d]{{0,15}}{NUM}\s*(?:m\b|metros?)?\s*(?:x|por|×)\s*{NUM}\s*(?:m\b|metros?)?")
AREA = re.compile(rf"{NUM}\s*(?:m²|m2|metros?\s+quadrados?)")
CONTAGEM = re.compile(r"\b(\d+|um|uma|dois|duas|tres|quatro|cinco)\s+(quartos?|dormitorios?|suites?|banheiros?|vagas?)\b")
# "garagem pra 2 carros" / "2 vagas" → garagem.count; "12,5" → float com vírgula decimal (pt-BR)
```
- [OPINIÃO] Atenção ao **separador decimal** pt-BR: "12,5" é decimal; "1.200" pode ser milhar. Para medidas de lote e cômodo, valores ≥ 1000 são improváveis, então dá para tratar "." como decimal quando houver 1 ou 2 casas e mandar o resto para confirmação.

### Gaps
- Não testei Duckling nem Recognizers-Text localmente (exigem Haskell/stack e um pacote alfa de 2019, respectivamente).
- Não verifiquei se o Recognizers-Text Python reconhece pt-BR na prática.

## 3. Léxico de sinônimos de tipos de cômodo como dado versionado em `data/`

### Takeaway
O léxico deve ser um YAML em `data/` com `id` do catálogo → lista de sinônimos (e plurais), cada entrada com fonte, seguindo a regra do projeto. O catálogo atual (`data/room_types.yaml` v0.3) **não tem um tipo `suite`**, então "suíte" precisa mapear para uma **composição** (quarto + banheiro privativo), não para um id. [FATO sobre o catálogo; OPINIÃO sobre o desenho]

### Cited Findings
- [FATO] O catálogo `data/room_types.yaml` (versão 0.3, 2026-11-21) tem estes ids: sala, sala_jantar, hall, circulacao, lavabo, home_theater, escritorio ("Escritório / home office"), varanda, patio, area_gourmet, quarto, quarto_solteiro, closet, banheiro, rouparia, sala_intima ("Sala íntima / TV"), brinquedoteca, cozinha, copa, lavanderia ("Área de serviço / lavanderia"), despensa, deposito, garagem ("Garagem (por vaga)"). Não há `suite` nem `oficina` — [arquivo local data/room_types.yaml no worktree m5-local-llm-research]
- [FATO] O Rasa trata sinônimos como mapeamento pós-extração para um valor canônico, sem diferenciar maiúsculas e minúsculas: "Synonym mapping only happens **after** entities have been extracted". Lookup tables são listas de palavras transformadas em regex case-insensitive, recomendadas "as specific as possible" — [Rasa docs: NLU training data](https://legacy-docs-oss.rasa.com/docs/rasa/nlu-training-data/)
- [FATO, teste local] O fuzzy não substitui o léxico: "vaga"→"garagem" pontuou 60, e "sala" casou "sala de estar" com 90 por casamento parcial (seção 1).

### Inferences
- [OPINIÃO] Formato sugerido (ilustrativo), seguindo `data/README.md` e `sources.yaml`:

```yaml
# ILUSTRATIVO — data/room_lexicon.yaml (nome hipotético)
version: "0.1"
entries:
  - type: quarto
    terms: [quarto, quartos, dormitorio, dormitorios, dorm]
    sources: {terms: <fonte-glossario>}
  - type: quarto_solteiro
    terms: ["quarto de solteiro", "quartos de solteiro"]
  - type: banheiro
    terms: [banheiro, banheiros, wc, "banheiro social"]
  - type: lavabo
    terms: [lavabo, lavabos]          # NÃO é sinônimo de banheiro: lavabo não tem chuveiro
  - type: lavanderia
    terms: ["area de servico", lavanderia, "area de lavar"]
  - type: garagem
    terms: [garagem, vaga, vagas, "abrigo de carro", "abrigo"]
    count_terms: ["pra {n} carros", "{n} vagas"]
  - type: sala
    terms: [sala, "sala de estar", living, estar]
compositions:
  - term: [suite, suites]
    expands_to: [{type: quarto}, {type: banheiro, attach: private}]
```
- [OPINIÃO] **Termos ambíguos que pedem regra especial ou confirmação:** "sala" sozinha (estar? jantar? íntima?): mapear para `sala`, deixando a premissa visível; "quarto" (cômodo × ordinal × fração); "WC" (banheiro ou lavabo?); "abrigo" (pode ser abrigo de gás ou de lixo); "escritório" × "oficina" (oficina não está no catálogo, então vai para o LLM ou o usuário escolhe o tipo mais próximo); "área" sozinha (área de serviço? área gourmet? área em m²?).
- [OPINIÃO] Fonte dos sinônimos: a regra "valor sem fonte fica vazio" se aplica ao vocabulário. Candidatas a fonte: glossários de normas e programas habitacionais (NBR 15575, MCMV, códigos de obras municipais já em `sources.yaml`), dicionários (Houaiss/Aulete/Priberam para "dormitório", "lavabo", "living") e anúncios imobiliários como evidência de uso real. Termos inventados pelo agente devem ser marcados com `agente` (como o projeto já faz com `access_hub: agente`).
- [OPINIÃO] Casar **sempre a expressão mais longa primeiro** ("quarto de solteiro" antes de "quarto"; "sala de jantar" antes de "sala"), sobre o texto sem acento, com `\b`. Ordenar os termos por comprimento decrescente numa regex única alternada.

### Gaps
- Não pesquisei um glossário oficial de nomenclatura de ambientes residenciais com sinônimos regionais (por exemplo, "living", "edícula", "quarto de empregada"/"dependência"). Isso pede uma trilha `Dn` própria.

## 4. Mapear intensificadores e atenuadores para a intensidade (1..5)

### Takeaway
Não encontrei recurso linguístico pronto (léxico com escala numérica) para intensificadores e atenuadores do pt-BR aplicado a preenchimento de slots. A literatura de semântica de grau trata "muito" e "bem" de forma qualitativa. O caminho prático é uma **tabela de modificadores versionada, com valores marcados como decisão de projeto (`agente`/`responsável`)**, e não como dado de norma. A intensidade inferida aparece como premissa editável. [FATO sobre a ausência; OPINIÃO sobre a solução]

### Cited Findings
- [FATO] Quadros Gomes (2011), "Uma proposta de distinção semântica para os intensificadores *muito* e *bem*", *Estudos Linguísticos* 40(1):379–394: em semântica de grau, *muito* exige disjunção dos graus comparados e *bem*, conjunção (no quadro de Kennedy & McNally 2005) — [Estudos Linguísticos (GEL)](https://revistas.gel.org.br/estudos-linguisticos/article/download/1403/943/3703). Só vi o resumo e as primeiras páginas.
- [FATO] Há trabalhos sobre *muito* expressivo × de grau no PB ("Flavors of intensity and emphasis: the case of muito in Brazilian Portuguese") — [Caderno de Squibs (UnB)](https://periodicos.unb.br/index.php/cs/article/view/45511)
- [FATO] Briz trata a atenuação (hedging, mitigação) como estratégia pragmática ligada à cortesia e à argumentação — [Linha d'Água (USP)](https://revistas.usp.br/linhadagua/article/download/64415/71564)
- [FATO] Uma tese de Carvalho sobre advérbios graduadores na fala rural e urbana de Minas Gerais conclui que os intensificadores são muito mais frequentes que os atenuadores — [Repositório UFMG](https://repositorio.ufmg.br/bitstream/1843/31174/1/Os%20adv%c3%a9rbios%20graduadores%20na%20fala%20rural%20e%20na%20fala%20urbana%20de%20Minas%20Gerais.pdf)
- [FATO] Também há estudos sobre adjetivos intensificadores no PB (Foltran & Nóbrega) — [Alfa (Unesp)](https://periodicos.fclar.unesp.br/alfa/article/view/7868)

### Inferences
- [OPINIÃO] Tabela sugerida (valores = **decisão de projeto**, a calibrar com o responsável; não vêm da literatura):

| Expressão (normalizada) | kind | intensity |
|---|---|---|
| "colado", "junto", "ligado a", "integrado com", "do lado de" | near | 5 |
| "bem perto", "muito perto", "pertinho" | near | 4–5 |
| "perto", "proximo" | near | 3 |
| "de preferencia perto", "se possivel perto", "seria bom perto" | near | 2 |
| "longe" | far | 3 |
| "bem longe", "muito longe", "afastado" | far | 4 |
| "o mais longe possivel", "bem separado", "isolado de" | far | 5 |
| "nao quero perto", "nao perto", "evitar perto" | far | 3 (negação de near ≠ far forte) |
| "nao precisa ser perto", "tanto faz" | (sem relação) | — |

- [OPINIÃO] **Composição:** `intensidade = base(predicado) + Δ(intensificador) − Δ(atenuador)`, limitada a [1, 5]. É mais compacta que listar todas as combinações, e cada Δ fica testável. Os atenuadores ("de preferência", "se possível", "se der", "talvez", "idealmente") reduzem a força, mas **não** mudam o sentido (near continua near).
- [OPINIÃO] "Não quero X perto de Y" não equivale a "quero X longe de Y" com a mesma força. Mapear para `far` com intensidade moderada (ou um `avoid_near`, se o modelo de dados aceitar) e mostrar como premissa.
- [HIPÓTESE] Como a intensidade é subjetiva, dois humanos dariam notas diferentes à mesma frase. Uma calibração rápida (o responsável pontua uns 30 exemplos) seria a "fonte" mais honesta da tabela.

### Gaps
- Não encontrei léxico computacional pt-BR de intensificadores com pontuação numérica. Recursos de análise de sentimento (por exemplo, OpLexicon, SentiLex-PT) poderiam ter listas de modificadores, mas não os pesquisei nesta rodada.

## 5. Padrões de arquitetura híbrida: regras primeiro, LLM para o resto

### Takeaway
O padrão consolidado na indústria (Rasa Pro ≥ 3.12) é **regras/NLU e LLM coexistindo no mesmo turno, com prioridade da extração determinística por slot e o LLM proibido, por padrão, de corrigir o que as regras preencheram**. Na academia, "regras primeiro, ML se falhar" aparece porque as regras têm alta precisão e baixa cobertura. Para o PyGridPlan, isso se traduz em: regras → spans cobertos + JSON parcial → LLM recebe o texto residual e os slots pré-preenchidos → merge com precedência das regras → todas as inferências do LLM viram premissas editáveis. [FATO sobre as fontes; OPINIÃO sobre a adaptação]

### Cited Findings
- [FATO] No Rasa Pro **≥ 3.12.0**, "both the LLM-based command generator and the `NLUCommandAdapter` can now issue commands by default at any given conversation turn". Um slot pode ter mapeamentos NLU e `from_llm`. Quando os dois extraem, "The NLU based mapping takes higher priority". Por padrão, "the LLM is not allowed to correct NLU-filled slots", e isso é opcional via `allow_nlu_correction: true`. **Antes da 3.12**, os dois se excluíam (comandos NLU desviavam o LLM no turno) — [Rasa docs: Slots](https://rasa.com/docs/reference/primitives/slots/)
- [FATO] A coexistência do Rasa (≥ 3.8) tem `IntentBasedRouter` e `LLMBasedRouter`. Se o LLM devolve resposta inválida ou fica inacessível, a mensagem vai para o sistema NLU, de forma "sticky" — [Rasa docs: Coexistence routers](https://rasa.com/docs/reference/config/components/coexistence-routers/); [Rasa docs: Coexistence](https://rasa.com/docs/rasa-pro/building-assistants/coexistence)
- [FATO] No Rasa clássico, regex e lookup não classificam nada sozinhos ("a regex does not act as a rule for classifying an intent"). O `RegexEntityExtractor` extrai sem modelo, mas exige pelo menos 2 exemplos anotados para registrar a entidade — [Rasa docs: NLU training data](https://legacy-docs-oss.rasa.com/docs/rasa/nlu-training-data/)
- [FATO] O pacote open source `rasa` está em 3.6.21 (14/01/2025), com Python < 3.11, o que é **incompatível com o Python 3.13** do projeto. O desenvolvimento passou para o Rasa Pro — [PyPI JSON rasa](https://pypi.org/pypi/rasa/json)
- [FATO] "When is ACL's Deadline?" usa NLU baseada em regras primeiro e cai para modelos de ML quando as regras falham, justificando que regras são precisas mas têm baixa cobertura — [arXiv 1911.10392](https://arxiv.org/pdf/1911.10392)
- [FATO] Um sistema híbrido de DST para persa combina regras com LMs para unir "precision and interpretability of rule-based approaches with the adaptability" dos LLMs (BERT para slots e intenção, GPT para o estado) — [arXiv 2510.01052](https://arxiv.org/html/2510.01052v1)
- [FATO] Um trabalho de 2026 usa regras de extração guiadas por esquema para gerar pares slot-valor candidatos e depois normaliza os valores gerados pelo LLM contra a base — [arXiv 2604.23345](https://arxiv.org/pdf/2604.23345). Vi só o resumo da busca.
- [FATO] O Duckling não tem wrapper Python oficial e roda como serviço HTTP separado — [GitHub meta/duckling](https://github.com/facebook/duckling). O padrão "Duckling + LLM" exigiria um processo Haskell paralelo, o que vai contra a simplicidade do projeto [OPINIÃO].

### Inferences
- [OPINIÃO] **Contrato sugerido entre as camadas** (é o que o mvp.md §7 já pressupõe):
  1. `parse_rules(texto) -> RuleResult{request_parcial, spans: list[(ini, fim, origem, campo)], ambiguidades}`. Funciona sem LLM e é determinístico e testável com fixtures.
  2. **Cobertura de spans:** marcar os caracteres explicados (números, cômodos, medidas, conectivos e palavras vazias como "casa com", "e", "pra"). O **resíduo** (sequências não cobertas com palavra de conteúdo) decide se o LLM é chamado. Sem resíduo, não há chamada: menos latência e nenhuma alucinação.
  3. **Prompt do LLM** = texto original + JSON parcial ("slots pré-preenchidos, não altere") + lista de ids do catálogo + trechos residuais destacados. O LLM devolve **só** os campos novos (relations, preferências), validados pelo mesmo esquema.
  4. **Merge:** campos das regras têm precedência (como no Rasa ≥ 3.12). Se o LLM tentar mudar um campo das regras, isso vira um **conflito mostrado ao usuário**, não uma sobrescrita. Ids fora do catálogo são descartados ou viram "tipo desconhecido → escolha".
  5. **Premissas:** cada item vindo do LLM, e cada default das regras (por exemplo, "sala" → `sala`, área-alvo assumida), entra no painel com origem (`regra` | `llm` | `padrão`) e o trecho do texto que o gerou, para correção em um clique.
- [OPINIÃO] **Confiança:** não confiar na autoavaliação do LLM. Usar sinais objetivos: (a) span casado por regra exata = alta; (b) fuzzy acima do corte = média, com a correção mostrada ("entendi 'cosinha' como cozinha"); (c) campo do LLM = sempre premissa a confirmar; (d) ids validados contra o catálogo e números contra faixas plausíveis (lote de 5 a 100 m; cômodo de 1 a 80 m²).
- [OPINIÃO] **Modo degradado:** sem LLM instalado, o resíduo aparece como "não interpretado: '<trecho>'" e o usuário pode criar a relação manualmente. É o mesmo comportamento sticky-fallback do Rasa, na direção inversa.
- [OPINIÃO] A **cobertura de spans** também serve de métrica de teste: em `tests/fixtures/`, cada pedido de referência pode declarar a cobertura esperada das regras, e a suíte detecta regressão quando um termo deixa de ser casado.

### Gaps
- Não encontrei um paper que descreva exatamente o padrão "regras → JSON parcial → LLM completa só o resto" com avaliação quantitativa; os mais próximos são os citados. A busca sugeriu procurar na ACL Anthology com termos como "LLM fallback rule-based slot filling".
- Não pesquisei o `spacy-llm` nem gramáticas formais (por exemplo, Lark ou parsers PEG) como alternativa às regex nesta rodada.

## 6. Onde as regras simples quebram: negação, correferência e quantidades

### Takeaway
As três quebras clássicas aparecem nos exemplos do projeto: a **negação** inverte ou anula a relação ("não quero perto"), a **correferência** ("ela", "esse quarto") liga a preferência a um cômodo citado antes, e as **quantidades compostas** ("dois quartos de solteiro", "3 quartos sendo uma suíte") exigem distributividade e inclusão. A regra prática é tratar com regex só os padrões locais e de janela curta, e mandar ao LLM ou à confirmação tudo o que depende de escopo. [OPINIÃO baseada nos FATOS e testes abaixo]

### Cited Findings
- [FATO] O NegEx decide a negação pela presença e posição de gatilhos numa janela de tokens, com regras em regex; uma adaptação para outro idioma reescreve os gatilhos. Um estudo em espanhol combinou NegEx adaptado com uma CNN e superou várias abordagens — [PMC10576331](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10576331/)
- [FATO] Em pt-BR, os marcadores de negação são majoritariamente itens lexicais, com alguns prefixos; há corpora anotados com marcador e escopo para francês e PB — [Natural Language Engineering (Cambridge), DOI 10.1017/S1351324920000352](https://api.crossref.org/works/10.1017%2FS1351324920000352)
- [FATO, teste local] Quantidades compostas e "quarto" quebram o normalizador genérico: `dois quartos de solteiro` → `dois 4ᵒˢ de solteiro`; `três quartos sendo uma suíte` → `3 4ᵒˢ sendo uma suíte` (seção 2).
- [FATO] O "um" é ambíguo entre artigo e numeral: com `threshold=0`, o text2num converte "um terço" em "1 terço" e "quero um quarto" em "quero 1 4º" (teste local, seção 2).

### Inferences
- [OPINIÃO] **Negação, o que as regras podem fazer:** detectar gatilhos ("não", "nem", "nunca", "sem", "evitar", "jamais") numa janela de cerca de 4 tokens antes do predicado de relação e inverter ou anular a relação. Casos para o LLM ou para confirmação: dupla negação ("não é que eu não queira perto"), escopo longo ("não quero nem a cozinha nem a lavanderia perto dos quartos", com coordenação de dois pares) e "sem" com outro sentido ("casa sem garagem" = remover cômodo, não relação).
- [OPINIÃO] **Correferência:** "ela", "esse quarto", "o maior", "a suíte" depois de "3 quartos sendo uma suíte". As regras não devem tentar resolver isso. Se um pronome ou demonstrativo aparece no lugar de um argumento de relação, o trecho vai para o LLM com a lista de cômodos já identificados, e o resultado vira premissa. [HIPÓTESE] Um LLM pequeno erra correferência com mais frequência que um grande, o que reforça a confirmação.
- [OPINIÃO] **Quantidades, regras sugeridas:**
  - "N quartos sendo K suítes" → N dormitórios no total, dos quais K com banheiro privativo (inclusão, não soma). "N quartos e K suítes" é ambíguo (soma? inclusão?): vai para confirmação.
  - "dois quartos de solteiro" → 2 × `quarto_solteiro` (distributivo: o modificador se aplica a todos).
  - "2 banheiros" quando há suíte: o banheiro da suíte conta nos 2? Ambíguo; registrar a premissa "inclui o banheiro da suíte" e deixar editável.
  - "garagem pra 2 carros" / "2 vagas" → garagem com contagem 2 (o catálogo já diz "por vaga").
  - "uns 15 m²" / "cerca de" / "no mínimo" / "até" → área-alvo com marcador de aproximação (`~`, `>=`, `<=`), que o modelo de dados pode precisar representar.
- [OPINIÃO] **Outras armadilhas do domínio:** números de outra natureza no mesmo texto ("2 andares", "casa para 4 pessoas", "orçamento 300 mil"), que precisam de contexto de unidade; unidades omitidas ("terreno 12x30" sem "m"; assumir metros e mostrar a premissa); ordem invertida ("30 por 12": largura × profundidade? convenção de frente × fundo, a confirmar); e "área" isolada (m² ou área de serviço).

### Gaps
- Não encontrei um NegEx específico para pt-BR de domínio geral nem um recurso pronto de correferência pt-BR leve e offline em Python; não pesquisei a fundo (por exemplo, CorefPT ou modelos do Stanza pt) nesta rodada.
- Não há corpus de pedidos de planta em pt-BR para medir a cobertura das regras. Os exemplos do `docs/design/mvp.md` e um conjunto escrito pelo responsável seriam o ponto de partida.
