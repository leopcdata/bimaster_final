#### Aluno: [Leonardo Cardoso](https://github.com/leopcdata)
#### Orientadora: Evelyn Batista
---
Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

- [Link para o código](https://github.com/leopcdata/bimaster_final)

---

### Resumo

Este trabalho apresenta o desenvolvimento de uma ferramenta de apoio à decisão voltada ao mapeamento da carteira de clientes oriundos de aquisições, com o objetivo de apoiar a integração mais rápida de vendedores a uma grande empresa de tecnologia. O projeto surge da necessidade de reduzir a dependência de um processo manual e demorado, no qual os clientes recebidos em processos de aquisição precisam ser associados aos respectivos registros da base de dados corporativa, considerando a estrutura comercial da organização (Go-to-Market). Para isso, a solução combina técnicas de processamento de linguagem natural e regras de negócio, com o objetivo de aumentar a eficiência operacional, padronizar as recomendações de mapeamento e contribuir para maior precisão na definição de territórios, metas e comissões, impactando de forma positiva os resultados da empresa.

### Abstract

This project presents the development of a decision-support tool focused on mapping client portfolios resulting from acquisitions, with the goal of supporting the faster integration of sellers into a large technology company. The project arises from the need to reduce dependence on a manual and time-consuming process in which clients received through acquisition processes must be matched to their corresponding records in the corporate database, while considering the organization’s commercial structure (Go-to-Market). To address this challenge, the solution combines natural language processing techniques and business rules in order to increase operational efficiency, standardize mapping recommendations, and contribute to greater accuracy in the definition of territories, targets, and commissions, with the potential to positively impact the company’s results as a consequence.

### 1. Introdução

O autor atua no departamento de Incentivos de vendas (Sales Compensation) de uma empresa global de tecnologia, responsável por processos relacionados à definição de planos de vendas, administração de territórios comerciais e cálculo de comissões. Nesse contexto, a operação comercial da empresa é organizada em territórios de vendas definidos a partir da estrutura corporativa de clientes, suas respectivas localidades e classificação dentro da estratégia da empresa. A correta designação dos territórios comerciais individuais é um elemento central, uma vez que impacta diretamente a definição de metas, a elegibilidade das vendas e a remuneração variável dos vendedores.

A companhia intensificou sua estratégia de crescimento por aquisições, com mais de 30 nos últimos cinco anos, e ao mesmo tempo tenta reduzir o prazo esperado para integração dos funcionários das empresas adquiridas, principalmente o corpo de vendas. Esse movimento ampliou a necessidade de incorporar novos vendedores e suas carteiras de clientes de forma ágil e estruturada aos sistemas corporativos. 

Entre as etapas mais críticas desse processo está o mapeamento da carteira de clientes, fornecida pelos gestores dessas empresas adquiridas, para a estrutura comercial da organização. Atualmente, esse mapeamento é realizado de forma predominantemente manual. Os analistas do setor precisam consultar individualmente cada cliente informado pelo gestor por meio de planilhas e confrontar essas informações com a base de dados corporativa composta por milhões de registros ativos, através de uma página de intranet. Além do elevado volume de dados, a atividade é dificultada pela ausência de padronização textual nos nomes das empresas informadas, que frequentemente apresentam abreviações, siglas, variações ortográficas, sufixos societários e diferenças de formatação. 

A complexidade do processo de mapeamento não se limita à comparação textual. A decisão final também depende da correta interpretação da classificação de cada cliente seguindo o modelo de Go-to-Market da empresa, o que exige conhecimento operacional e análise contextual. Em uma integração realizada ano passado, essa etapa demandou aproximadamente uma semana de trabalho de uma equipe de cerca de dez pessoas, evidenciando a baixa escalabilidade e o alto esforço operacional do modelo atual.

Diante desse cenário, este trabalho propõe o desenvolvimento de uma ferramenta de apoio à decisão voltada à automatização parcial do processo de mapeamento de clientes. A solução busca reduzir o esforço manual, aumentar a consistência das recomendações e tornar o processo de integração mais eficiente, confiável e escalável.

### 2. Regras de Negócio

Antes de seguir com a modelagem, importante evidenciar a estrutura hierárquica dos clientes da empresa. Em 2026, os clientes estão distribuídos em quatro segmentos que refletem diferentes níveis de dedicação comercial, estratégia de vendas e comissão:

- **Enterprise**
- **Strategic**
- **Select Horizon**
- **Select Territory**

Nos segmentos Enterprise, Strategic e Select Horizon, clientes de maior relevância costumam estar associados a estruturas de cobertura mais dedicadas, muitas vezes representadas por um identificador específico. Já no segmento Select Territory, é comum que milhares de clientes sejam agrupados em estruturas mais amplas, definidas por critérios como geografia, indústria ou pela combinação de ambos. São contas menores onde se busca um maior crescimento.

A cobertura constitui um dos principais elementos utilizados na definição dos territórios de vendas. Em alguns casos, ela representa praticamente um cliente individual; em outros, corresponde a agrupamentos de dezenas ou até milhares de clientes. Por esse motivo, a decisão de mapeamento vai além da similaridade textual entre nomes, exigindo também a identificação do nível mais adequado dentro da hierarquia comercial.

A modelagem deve sempre priorizar a estrutura de maior relevância quando uma busca retornar resultados em diferentes segmentos para uma mesma entrada. Do ponto de vista de negócio, esse mapeamento é altamente crítico. Os planos de vendas são definidos no início do ano e, após sua oferta, só podem ser modificados em condições bastante específicas. Esses planos são compostos, de forma geral, pelos clientes sob responsabilidade do vendedor e pelos produtos que ele deve comercializar. A partir dessas definições, o sistema calcula metas com base no histórico dos clientes e na estratégia de crescimento. 

### 3. Metodologia

A metodologia adotada neste trabalho foi estruturada para reproduzir, de forma padronizada e escalável, a etapa inicial do processo de integração de vendedores oriundos de aquisições. Na prática, esse processo começa quando um gerente de vendas envia uma lista de clientes que devem ser incorporados ao território de sua equipe, contendo apenas os nomes das empresas e o país, sem padronização e sem referência direta aos identificadores utilizados na base corporativa.

Para transformar esse fluxo manual em uma pipeline automatizada, a solução foi desenhada em duas dimensões complementares: um **fluxo de processamento** sequencial em etapas, e uma **arquitetura modular** em Python que implementa cada etapa em módulos independentes.

#### 3.1 Visão geral do fluxo

O fluxo completo da solução é composto por seis etapas sequenciais, descritas em alto nível abaixo e detalhadas nas subseções seguintes:

1. **Recebimento do input** — lista de clientes fornecida pelo gestor (Excel), contendo nomes de empresas e país.
2. **Extração de dados** — consulta à base corporativa via SQL, com filtragem por país e cache local.
3. **Normalização textual** — padronização dos nomes das empresas para reduzir diferenças de formatação.
4. **Matching** — comparação textual bruta e normalizada com cálculo de similaridade via fuzzy matching.
5. **Agrupamento e priorização** — classificação dos candidatos em quatro grupos de negócio e aplicação de regras hierárquicas para definir a recomendação final.
6. **Geração de outputs** — construção de um arquivo Excel com as abas Summary, Details e Metrics.

#### 3.2 Arquitetura modular da solução

A solução foi organizada em módulos independentes, cada um com responsabilidade única, o que facilita manutenção, testes e evolução futura. A Tabela 1 resume o papel de cada módulo:

| Módulo | Responsabilidade |
|---|---|
| `main.py` | Orquestra o fluxo completo: leitura do input, consulta ao banco, preparação dos jobs por grupo, execução, consolidação e geração do Excel final. |
| `config.py` | Centraliza parâmetros de execução (pastas de entrada/saída, thresholds de confiança, limite de candidatos) e a definição dos quatro grupos de negócio. |
| `benchmark.py` | Implementa as estratégias de execução sequencial e paralela (via `ThreadPoolExecutor`) e mede o tempo por grupo. |
| `utils/db_utils.py` | Encapsula a conexão com o banco DB2, a query SQL parametrizada por país e o mecanismo de cache local em CSV. |
| `utils/matching.py` | Contém o motor de matching (`process_group`) e os mapeamentos de saída de cada grupo. |
| `utils/normalize.py` | Implementa a rotina de normalização textual dos nomes de empresas. |
| `utils/process_utils.py` | Monta os jobs por grupo (`prepare_group_jobs`), anexa empresas não encontradas e finaliza as abas Summary e Details. |
| `utils/summary.py` | Aplica as regras de priorização, constrói o arquivo Excel final com as três abas e aplica os realces visuais de revisão. |
| `utils/metrics.py` | Calcula e formata as métricas de execução e qualidade exibidas na aba Metrics. |
| `utils/io_utils.py` | Trata a seleção do arquivo de input, a captura do código de país e a montagem do caminho de saída. |

Essa separação foi uma evolução relevante em relação à primeira versão do projeto, que concentrava grande parte da lógica em um único arquivo. A modularização permitiu isolar preocupações distintas (acesso a dados, regras de negócio, apresentação, orquestração) e tornou mais simples a adição de novas funcionalidades, como o benchmark e a aba de métricas.

O ponto de entrada da aplicação é a função `main()` em `main.py`, que executa o fluxo na seguinte ordem:

```
select_input_file → get_country_code → pd.read_excel
  → fetch_data (DB2 + cache)
    → prepare_group_jobs
      → choose_execution (sequencial | paralelo | benchmark)
        → append_unmatched_companies
          → finalize_details
            → build_metrics_df
              → write_summary_excel
```

#### 3.3 Etapa 1 — Extração de dados

A primeira etapa da solução consiste em obter, da base corporativa, o subconjunto de clientes que será utilizado como universo de busca. Essa etapa é implementada no módulo `utils/db_utils.py` e é acionada por `main.py` logo após a leitura do arquivo de input.

Ao iniciar a execução, a ferramenta solicita ao usuário, de forma interativa, a seleção do arquivo de input entre os disponíveis na pasta configurada e o código de país (3 dígitos) a ser processado. Essa abordagem simplifica o uso por analistas sem exigir edição de parâmetros no código.

A extração é estruturada com três características principais:

- **Uso combinado de Python e SQL** para consultar a base corporativa hospedada em DB2.
- **Parametrização por país**, limitando o conjunto de registros ao mercado relevante para a aquisição. Essa restrição é essencial, pois a base corporativa possui milhões de registros em escala global, e em mercados grandes como os Estados Unidos o volume ultrapassa 470 mil clientes.
- **Cache local em CSV**, armazenado em `CACHE_FOLDER`. Na primeira execução para um país, o resultado da consulta é persistido localmente; em execuções subsequentes, os dados são lidos diretamente do arquivo de cache, evitando reconsultas desnecessárias ao banco. Essa abordagem é adequada ao contexto do projeto, já que a estrutura de clientes é definida no início do ano e tende a permanecer estável ao longo do ciclo.

A consulta retorna, para cada cliente, os seguintes campos principais: identificador e nome da cobertura (`COV_TYPE_ID`), grupos globais e domésticos de buying group (`GBL_BUY_GRP`, `DOM_BUY_GRP`), identificador e nome do global client, nome legal do cliente, listas de segmentação válidas (`acct_list_ids`), indústria e país. Filtros adicionais garantem que apenas clientes ativos, em tipos de cobertura válidos e pertencentes ao grupo de listas oficial da estrutura comercial sejam retornados.

<img width="539" height="303" alt="image" src="https://github.com/user-attachments/assets/c4cf4bff-5df9-435f-a7b4-e5f035105f13" />

Figura 1. Exemplo de entrada do processo - Lista fornecida por um gestor

<img width="629" height="334" alt="image" src="https://github.com/user-attachments/assets/032cc20f-c483-49ce-ac72-3153b1de954c" />

Figura 2. Total de clientes registrados nos EUA por segmento

#### 3.4 Etapa 2 — Normalização textual

O segundo desafio da solução é lidar com a inconsistência entre os nomes de empresas informados no input e os registrados na base corporativa. Para isso, `utils/normalize.py` implementa uma rotina de normalização que reduz diferenças de formatação sem alterar a identidade da empresa. A normalização aplica as seguintes transformações:

- conversão para minúsculas;
- remoção de espaços extras e pontuação;
- remoção de sufixos societários comuns (Inc, LLC, Corp, Ltda, Group, entre outros);
- remoção de stopwords (palavras pouco relevantes para identificação).

Uma decisão importante do projeto foi **preservar simultaneamente o nome original e sua versão normalizada**. A normalização não substitui a comparação bruta; ela atua como uma camada complementar, permitindo que o matching use as duas representações em sequência.

#### 3.5 Etapa 3 — Estratégia de matching

A comparação entre os nomes do input e os registros da base foi estruturada em duas abordagens complementares e sequenciais, com o objetivo de equilibrar precisão textual e flexibilidade diante de variações de escrita:

- **Raw matching** — compara o nome original da empresa informado no input com o nome legal original do cliente na base.
- **Normalized matching** — compara as versões normalizadas dos dois nomes, capturando casos em que a comparação bruta não teria sucesso devido a sufixos societários, abreviações ou pequenas variações de formatação.

Para o cálculo de similaridade é utilizada a biblioteca **RapidFuzz**, especializada em comparação aproximada de strings, que retorna um **score de similaridade entre 0 e 100**. A técnica de fuzzy matching mede o grau de proximidade mesmo na presença de erros de digitação, variações ortográficas ou diferenças de estrutura.

A etapa de matching trabalha com duas faixas de score:

- **Alta confiança** — candidatos com score maior ou igual a **80** são gerados tanto pelo raw matching quanto pelo normalized matching, e compõem a maior parte da saída.
- **Fallback** — candidatos com score entre **60 e 79** no normalized matching são incluídos apenas quando nenhum candidato de alta confiança foi encontrado para a empresa, garantindo que entradas difíceis ainda recebam sugestões ordenadas por similaridade. Candidatos abaixo de 60 são descartados.

O número máximo de candidatos retornados por empresa é controlado pelo parâmetro `MATCH_LIMIT` (atualmente fixado em 20 em `config.py`).

O uso de similaridade textual corrige uma distorção típica de abordagens por substring em SQL. Tomando como exemplo a empresa "AON", uma busca por ocorrência parcial de texto retornaria indevidamente registros como "Kaonmedia". Com fuzzy matching combinado aos critérios adicionais de classificação, esse tipo de falso positivo é significativamente reduzido.

Ainda assim, alguns casos permanecem ambíguos. Um exemplo é a entrada "As America, Inc", que pode retornar scores semelhantes para nomes como "Asm America" e "JAS America". Situações como essa indicam espaço para evolução, seja pela criação de regras adicionais baseadas na hierarquia de negócio, seja pela incorporação de técnicas complementares como embeddings semânticos.

#### 3.6 Etapa 4 — Agrupamento por regras de negócio

Uma contribuição central da modelagem foi estruturar o problema em **grupos de contas com regras de saída e prioridades distintas**, em vez de tratar toda a base da mesma forma. Os registros são organizados em quatro grupos, configurados em `GROUP_CONFIG` dentro de `config.py`:

| Grupo | Listas de conta (`acct_list_names`) | Nível de saída principal |
|---|---|---|
| **Grupo 1** | Enterprise Client Expansion, Enterprise Non-Client Expansion, Strategic Client Expansion, Strategic Non-Client Expansion | `COV_TYPE_ID` |
| **Grupo 2** | Horizon EMEA, Horizon - non-EMEA | `COV_TYPE_ID` |
| **Grupo 3** | Activate, Growth, BP WW CEID | `GBL_BUY_GRP` (com exceção descrita abaixo) |
| **Grupo 4** | Activate Unassigned | `GBL_BUY_GRP` (com exceção descrita abaixo) |

Os Grupos 1 e 2 retornam resultados em nível de `COV_TYPE_ID`, pois nesse contexto o nível de cobertura é o mais apropriado para recomendação. Os Grupos 3 e 4 retornam, em regra geral, em nível de `GBL_BUY_GRP`.

Existe, porém, uma exceção bem definida para os Grupos 3 e 4: quando o código `GBL_BUY_GRP` tem três ou quatro caracteres e começa com o prefixo **"ST"** (indicando contas menores agrupadas por Estado (State) e Indústria), a saída é forçada para o nível `DOM_BUY_GRP`. Essa regra reflete a prática comercial da organização, em que esse subconjunto de contas é gerido com granularidade maior que o restante do grupo.

> **Nota:** esses níveis de agrupamento **não se confundem com os segmentos comerciais** apresentados na Seção 2 (Enterprise, Strategic, Select Horizon, Select Territory). Os grupos são agrupamentos operacionais internos da ferramenta, utilizados para aplicar regras de saída e priorização distintas. Os segmentos são uma classificação de negócio da própria empresa.

Para ilustrar a relação entre os níveis de saída, tomemos como exemplo a PepsiCo: a organização PepsiCo como um todo corresponde à estrutura principal (`COV_TYPE_ID`); a divisão entre bebidas e alimentos é representada por diferentes `GBL_BUY_GRP`; e suas marcas individuais correspondem a diferentes `DOM_BUY_GRP`. Essa hierarquia permite diferentes coberturas comerciais para um mesmo conglomerado.

#### 3.7 Etapa 5 — Priorização e consolidação

Após a geração dos candidatos para todos os grupos, a ferramenta precisa consolidar uma recomendação final por empresa na aba Summary. Essa lógica é implementada em `utils/summary.py` (função `build_summary`), a partir dos candidatos montados em `utils/process_utils.py`.

A priorização trabalha com um threshold mais exigente do que o utilizado na geração de candidatos: a camada de Summary considera apenas candidatos com score **maior ou igual a 90** como de "alta confiança", aplicando a seguinte ordem de decisão para cada empresa:

1. Grupo 1 ou Grupo 2 com score ≥ 90
2. Grupo 3 com score ≥ 90
3. Grupo 4 com score ≥ 90
4. Melhor candidato com score entre 50 e 89, em qualquer grupo
5. Cliente não encontrado

Nos Grupos 3 e 4, quando múltiplos candidatos de alta confiança existem para a mesma conta, a ferramenta prioriza registros em nível de `GBL_BUY_GRP`. Quando uma mesma conta (`ACCT`) aparece associada a mais de um `GBL_CLIENT_ID`, os registros são consolidados em uma única linha no Summary, preenchida com a mensagem *"Multiple Global Client IDs - check Details tab"*, direcionando o analista à aba Details para a decisão final.

Como os candidatos podem surgir a partir de mais de uma etapa de matching (raw e normalizado), foi necessário implementar uma **estratégia de deduplicação** baseada em atributos-chave do resultado, reduzindo repetições e melhorando a qualidade da saída final.

#### 3.8 Etapa 6 — Geração de outputs

A última etapa é construída em `utils/summary.py` e `utils/metrics.py`, invocadas por `main.py` ao final da execução. O resultado é um único arquivo Excel com três abas:

**Summary** — Recomendação final por empresa, respeitando as regras de priorização. Inclui realces visuais para facilitar a revisão humana:

- **amarelo**: cliente não encontrado;
- **azul claro**: empresas com múltiplas linhas no summary (exigem revisão na aba Details);
- **laranja claro**: registros de Activate Unassigned, que demandam atenção especial por não serem registros ativos no pipeline do ano corrente e exigirem etapas adicionais de processo para ativação.

<img width="886" height="250" alt="image" src="https://github.com/user-attachments/assets/af6640f2-4002-476e-9065-bd7802060717" />

Figura 3. Exemplo de um resultado prático da aplicação

**Details** — Todos os candidatos encontrados pelo motor de matching, com score, nível da conta, atributos de cobertura, buying group, global client, grupo de origem e lista de segmentação.

**Metrics** — Métricas de execução e qualidade organizadas em quatro blocos: visão geral (total de empresas processadas, encontradas e não encontradas, percentuais de cobertura, matches de alta confiança), tempos de execução (total e por grupo, incluindo comparativo entre os modos sequencial e paralelo quando o benchmark está ativo), distribuição de matches por grupo e distribuição de confiança do Summary por faixa de score.

<img width="393" height="194" alt="image" src="https://github.com/user-attachments/assets/49fc9f46-24fb-42c8-aaca-ae46ae8dbe38" />

<img width="394" height="262" alt="image" src="https://github.com/user-attachments/assets/8ffb9f3f-b657-4ef2-9ac5-a3554a40b7f9" />

Figuras 4 e 5. Resultados de métricas


#### 3.9 Estratégia de execução e benchmark

Para avaliar o desempenho da solução, `benchmark.py` implementa duas estratégias de execução que podem ser selecionadas via `config.py`:

- **Sequencial** (`run_groups_sequential`) — processa os quatro grupos um a um.
- **Paralela** (`run_groups_parallel`) — processa os grupos simultaneamente usando um `ThreadPoolExecutor` com um worker por grupo.

O modo padrão é controlado por `DEFAULT_EXECUTION_MODE = "sequential"`. Adicionalmente, ativando `RUN_BENCHMARK = True`, a função `choose_execution()` em `main.py` executa **ambas as estratégias** na mesma rodada, compara os tempos totais e seleciona automaticamente a mais rápida para gerar os outputs, registrando também os tempos comparativos na aba Metrics.

O benchmark mostrou que, no ambiente testado, a execução sequencial apresentou desempenho total superior à paralela. Esse resultado indica que o workload é predominantemente **CPU-bound** — o overhead de criação e sincronização de threads supera os ganhos potenciais de concorrência, limitados pelo GIL do Python para tarefas desse tipo. Com base nessa evidência, a execução sequencial passou a ser o modo padrão, mantendo o benchmark como opção para análises futuras (por exemplo, caso se migre a paralelização para `ProcessPoolExecutor` ou para uma execução distribuída).


### 4. Modelagem
A modelagem da solução foi estruturada para reproduzir, de forma padronizada e escalável, a etapa inicial do processo de integração de vendedores oriundos de aquisições. Na prática, esse processo começa quando um gerente de vendas envia uma lista de clientes que devem ser incorporados ao território de sua equipe. Essa lista normalmente contém apenas os nomes das empresas, sem padronização e sem referência direta aos identificadores utilizados na base corporativa. A partir dessa entrada, iniciam-se as etapas críticas do fluxo.

Diante desse cenário, a solução proposta neste trabalho consiste em uma ferramenta em Python de apoio à decisão, desenvolvida para automatizar a parte mais custosa desse processo: a busca inicial na base, a comparação textual entre nomes, a classificação preliminar dos candidatos e sua priorização para análise final do analista. A ferramenta não elimina a validação final humana, mas reduz significativamente o esforço manual e aumenta a consistência da etapa de triagem.

<img width="539" height="303" alt="image" src="https://github.com/user-attachments/assets/c4cf4bff-5df9-435f-a7b4-e5f035105f13" />

Figura 1. Exemplo de entrada do processo - Lista fornecida por um gestor


#### 4.1 Extração de dados

A partir da lista de clientes recebida, a primeira etapa da solução consiste na extração dos dados de referência que se encontram no Banco de Dados e que serão utilizados ao longo do processo de identificação e recomendação de contas. Essa etapa foi estruturada para reduzir o universo de busca logo no início e garantir melhor desempenho no processamento, utilizando:

- uso combinado de Python e SQL para extração dos dados na base corporativa;
- parametrização da busca em nível de país, limitando o conjunto de registros analisados;
- utilização de cache local por país, com o objetivo de reduzir consultas repetidas ao banco e melhorar a performance.

Quando os dados de um país são processados pela primeira vez, o código estabelece conexão com o banco de dados, executa a consulta SQL correspondente e armazena o resultado localmente. Quando esse mesmo país já foi executado anteriormente, a leitura passa a ser feita diretamente a partir do arquivo de cache gerado em csv, evitando reconsultas desnecessárias ao banco e reduzindo o tempo total de processamento. Essa abordagem é adequada ao contexto do projeto, pois esses dados são definidos para o ano corrente e tendem a permanecer estáveis, exceto em situações pontuais.

A consulta retorna, entre outros, os seguintes campos:

identificador e nome da cobertura;
grupos globais e domésticos de buying group;
identificador e nome do global client;
nome legal do cliente;
listas de segmentação válidas;
indústria;
país.

A importância dessa etapa também se explica pelo volume de dados analisado. Considerando como exemplo a base de clientes dos Estados Unidos mostrada abaixo, que representa o maior volume de negócios, são aproximadamente 470 mil registros. Em escala global, a base contém milhões de registros, o que reforça a necessidade de restringir a busca por país e reutilizar dados já extraídos para garantir viabilidade operacional e melhor desempenho.

<img width="629" height="334" alt="image" src="https://github.com/user-attachments/assets/032cc20f-c483-49ce-ac72-3153b1de954c" />

Figura 2. Total de clientes registrados nos EUA por segmento


#### 4.2 Normalização textual

O segundo desafio da solução foi tratar a inconsistência entre os nomes das empresas informados no input e aqueles registrados na base corporativa. Para lidar com isso, foi criada uma rotina de normalização textual com o objetivo de reduzir diferenças de formatação que não alteram a identidade da empresa.

A normalização inclui:

- conversão de todo o texto para minúsculas;
- remoção de espaços extras e pontuação;
- remoção de termos societários comuns, como Inc, LLC, Corp, Ltda e Group;
- remoção de palavras pouco relevantes para a identificação, como stopwords.

A normalização não substitui a comparação com o texto original, mas atua como uma camada complementar de apoio ao matching. Por esse motivo, o projeto preserva tanto o nome original quanto sua versão normalizada, permitindo que a análise considere simultaneamente a forma bruta recebida no input e uma representação mais padronizada.

#### 4.3 Estratégia de matching
A estratégia de matching foi estruturada em duas abordagens complementares e sequenciais, de forma a equilibrar precisão textual e flexibilidade no tratamento de variações de escrita.

- Raw matching: compara o nome original da empresa informado no input com o nome legal original do cliente na base;
- Normalized matching: compara as versões normalizadas dos dois nomes, quando necessário.

Esse desenho foi importante porque permite capturar casos de forte correspondência textual já na comparação direta, sem abrir mão de uma segunda camada mais flexível para tratar abreviações, sufixos societários, diferenças de grafia e pequenas variações de formatação.

Para o cálculo de similaridade, foi utilizada a biblioteca RapidFuzz, em Python, especializada em comparação aproximada de strings. A técnica de fuzzy matching permite medir o grau de similaridade de 0 a 100 entre textos mesmo quando há erros de digitação, variações ortográficas ou diferenças de estrutura. Nesta aplicação, a comparação é feita entre o nome da empresa informado no input e os nomes legais dos clientes disponíveis na base.

Os resultados são classificados conforme faixas de confiança, incluindo:

- candidatos de alta confiança: score maior ou igual a 80 durante a geração;
- candidatos de fallback: scores entre 60 e 80, utilizados quando não há correspondência mais forte na comparação normalizada.

Essa técnica ajuda a evitar distorções típicas de buscas simples por substring, uma alternativa usada anteriormente por meio de SQL. Dando como exemplo a empresa “AON” - se a busca considerasse apenas ocorrência parcial de texto, nomes como “Kaonmedia” poderiam surgir indevidamente como candidatos. O uso de similaridade textual, combinado com critérios adicionais, reduz esse risco e melhora a qualidade da recomendação.

Ainda assim, alguns casos permanecem ambíguos. Um exemplo é a entrada “As America, Inc”, que pode retornar pontuações semelhantes para nomes como “Asm America” e “JAS America”. Situações como essa mostram que ainda há espaço para evolução da solução, seja pela criação de regras adicionais baseadas na hierarquia de negócio, seja pela incorporação de técnicas complementares de comparação textual.

#### 4.4 Agrupamento por regras de negócio

Uma parte essencial da modelagem foi estruturar o problema em grupos de contas com regras de saída e prioridade diferentes. Em vez de tratar toda a base da mesma forma, os registros foram organizados em quatro grupos:

**Grupo 1**
- Enterprise Client Expansion
- Enterprise Non-Client Expansion
- Strategic Non-Client Expansion
- Strategic Client Expansion

**Grupo 2**
- Horizon EMEA
- Horizon - non-EMEA

**Grupo 3**
- Activate
- Growth

**Grupo 4**
- Activate Unassigned

Os Grupos 1 e 2 retornam resultados em nível de **COV_TYPE_ID**, pois nesse contexto o nível de cobertura é o mais apropriado para recomendação.

Os Grupos 3 e 4 retornam principalmente em nível de **GBL_BUY_GRP**, com tratamento especial para alguns casos específicos em que a melhor forma de exibição é **DOM_BUY_GRP**.

Essa separação foi uma das principais evoluções do projeto, pois permitiu refletir melhor as regras de segmentação comercial e organizar a lógica de decisão de forma mais clara.

Os termos COV_TYPE_ID, GBL_GRP_ID, DOM_BUY_GRP são a forma que a empresa classifica seus clientes. Dando como exemplo a PEPSI. Podemos classificar a organização PepsiCo como a estrutura principal (COV_TYPE_ID), a divisão entre os setores de bebidas e alimentos como diferentes GBL_BUY_GRP_ID e suas marcas individuais como diferentes DOM_BUY_GRP. Isso permite diferentes coberturas comerciais e classificações para um mesmo conglomerado. 

#### 4.5 Regras de priorização

Após gerar todos os candidatos, a ferramenta precisa recomendar um resultado final por empresa no Summary. Para isso, foi criada uma lógica de priorização baseada nos grupos e na confiança dos scores.

A ordem atual de priorização é:
1. Grupo 1 e Grupo 2 com probabilidade maior ou igual a 90
2. Grupo 3 com probabilidade maior ou igual a 90
3. Grupo 4 com probabilidade maior ou igual a 90
4. melhor candidato entre 50 e 90
5. cliente não encontrado

Nos Grupos 3 e 4, quando múltiplos candidatos de alta confiança existem para a mesma conta, a ferramenta prioriza registros em nível de **GBL_BUY_GRP** quando disponíveis. Caso existam múltiplos registros para a mesma conta, os registros são consolidados em uma única linha no Summary com uma mensagem que direciona a revisão humana para a aba de detalhes.

#### 4.6 Estrutura de saída

A ferramenta produz três abas principais:

**Summary**  
Contém a recomendação final por empresa, respeitando as regras de prioridade.

**Details**  
Contém todos os candidatos encontrados pelo motor de matching, com score, nível da conta, atributos de cobertura, buying group, global client, grupo de origem e lista de segmentação.

**Metrics**  
Contém métricas de execução e qualidade, como:
- número de empresas processadas
- empresas encontradas e não encontradas
- percentuais de cobertura
- distribuição de matches por grupo
- quantidade de matches com alta confiança
- empresas com múltiplos resultados
- tempo total de execução
- tempo por grupo
- tempo por empresa processada

<img width="393" height="194" alt="image" src="https://github.com/user-attachments/assets/49fc9f46-24fb-42c8-aaca-ae46ae8dbe38" />

<img width="394" height="262" alt="image" src="https://github.com/user-attachments/assets/8ffb9f3f-b657-4ef2-9ac5-a3554a40b7f9" />

Figuras 3 e 4.  Resultados de métricas


Além disso, o Summary possui realces visuais para facilitar a revisão:
- **amarelo**: cliente não encontrado
- **azul claro**: empresas com múltiplas linhas no summary
- **laranja claro**: registros de Activate Unassigned

As empresas classificadas como **Activate Unassigned**, demandam uma atenção importante no projeto já que não são registros ativos no pipeline do ano corrente. Entradas classificadas nesse grupo necessitam etapas adicionais de processo para garantir a ativação dessas contas e consequentemente o pagamento de comissão para o vendedor.

<img width="886" height="250" alt="image" src="https://github.com/user-attachments/assets/af6640f2-4002-476e-9065-bd7802060717" />
Figura 5. Exemplo de um resultado prático da aplicação

#### 4.7 Desafios enfrentados e soluções encontradas

Ao longo da execução do projeto, alguns desafios importantes surgiram.

**1. Diferença entre matching bruto e matching normalizado**  
Em uma versão inicial, a análise considerada como “raw” ainda estava sendo executada sobre nomes normalizados, o que eliminava parte do valor da dupla abordagem. Esse problema foi corrigido ao separar explicitamente as estruturas de comparação para nome bruto e nome normalizado.

**2. Duplicidade de resultados**  
Como os candidatos podiam surgir a partir de mais de uma etapa de matching, houve necessidade de criar uma estratégia de deduplicação com base em atributos-chave do resultado, reduzindo repetição e melhorando a qualidade da saída final.

**3. Organização do código**  
A primeira versão concentrava muitas responsabilidades no arquivo principal. Ao longo da evolução, a solução foi modularizada em arquivos separados para configuração, execução, métricas, preparação de dados, matching, summary e acesso ao banco, tornando o projeto mais limpo, mais legível e mais sustentável.

**4. Performance**  
Foi implementado benchmark entre execução sequencial e paralela (ThreadPoolExecutor). O resultado mostrou que, no ambiente testado, a execução sequencial apresentou melhor desempenho total do que a paralela. Isso indicou que o workload do projeto é predominantemente CPU-bound, e que o overhead de threads superava os ganhos potenciais de concorrência. A partir disso, a execução sequencial passou a ser o modo padrão, mantendo o benchmark como opção para análise.

**5. Representação das regras de negócio**  
Outro desafio foi traduzir corretamente as regras de priorização da estrutura comercial para uma lógica programável. A solução encontrada foi estruturar os grupos com configuração centralizada e regras explícitas no resumo final, permitindo ajustes futuros com menor esforço.

**6. Variação entre mercados e países**  
Outro desafio relevante é que a estrutura de cobertura não é universal e pode variar entre países e mercados. Cada unidade geográfica pode definir suas próprias regras e estratégias locais para agrupar clientes, desde que alinhadas ao modelo comercial global. Além disso, a estrutura de cobertura é revisada a cada planejamento anual e depois permanece congelada durante o ciclo de execução. Isso reforça a necessidade de tomar a decisão correta no momento do mapping, já que a configuração inicial do território terá impacto durante todo o período de vigência do plano de venda.

### 5. Resultados 

O principal resultado do projeto foi transformar um processo altamente manual em uma solução majoritariamente automatizada, estruturada e orientada por regras de negócio, aplicando conceitos de sistemas inteligentes de apoio à decisão diretamente em um processo corporativo real, complexo e sensível para o negócio.

A aplicação desenvolvida se mostrou capaz de processar centenas de entradas em segundos, mostrando grande aumento de eficiência em comparação a análise manual que leva cerca de 4 minutos por registro. Para alguns casos podem ser necessários algum tipo de análise individual ainda, mas o output já fornece as informações necessárias e porcentagem de similaridide para auxílio à tomada de decisão. Reduzindo o tempo gasto em um processo completo que envolvia diversas pessoas e durava dias, podendo hoje ser executado por apenas uma pessoa.

Como contribuição técnica, o projeto integra:
- conexão com DB2
- extração estruturada de dados
- normalização textual
- fuzzy matching
- classificação através de regras hierárquicas de priorização
- mensuração de performance e qualidade
- output estruturado para decisão

Os resultados do projeto mostram que a automação não apenas reduz o esforço de busca e comparação textual, mas também apoia uma decisão mais sofisticada: recomendar o nível mais adequado dentro de uma estrutura comercial hierárquica, na qual diferentes segmentos e coberturas possuem papéis distintos na definição dos territórios.

A ferramenta também fornece suporte à decisão mesmo em casos ambíguos, ao apresentar múltiplos candidatos com score de similaridade e atributos relevantes. Mesmo quando a ferramenta não consegue decidir automaticamente uma única resposta ideal, ela ainda gera valor relevante ao reduzir o universo de busca e apresentar os candidatos mais plausíveis de forma organizada, deixando claro onde há conflito e onde a revisão humana é necessária. Há espaço para melhoria com a inclusão de outras técnicas de comparação de string, considerando também a estrutura do modelo da empresa.

Um exemplo da presença de registros desatualizados e irrelevantes que dificultam o processo atual é o cliente MGM studios presente abaixo, que foi vendido da Disney para Amazon em 2022, embora ambos registros ainda permaneçam no sistema.

<img width="975" height="100" alt="image" src="https://github.com/user-attachments/assets/0345b1f9-053f-4c58-b236-8b44f908351e" />
Figura 6. Exemplo de dados desatualizados no sistema

### 6. Conclusões

Este trabalho teve como objetivo reduzir a dependência de um processo manual, demorado e pouco escalável no mapeamento de clientes oriundos de aquisições, etapa crítica para a integração de vendedores em uma grande empresa de tecnologia. 

A solução proposta demonstrou que é possível estruturar esse processo por meio da combinação de técnicas de processamento de linguagem natural e regras de negócio, transformando uma atividade predominantemente manual em uma pipeline automatizada, reprodutível e orientada à decisão.

Do ponto de vista prático, o projeto gerou ganhos relevantes de eficiência operacional, reduzindo significativamente o tempo necessário para análise e permitindo que um processo que antes demandava vários dias de trabalho de uma equipe seja executado em poucos minutos por um único analista. Além disso, a padronização das recomendações contribui para maior consistência nas decisões e melhor governança do processo.

Um dos principais diferenciais da solução está na capacidade de não apenas identificar correspondências textuais, mas também recomendar o nível mais adequado dentro de uma estrutura comercial hierárquica, respeitando as regras de segmentação e priorização da organização. Isso aproxima a ferramenta de um sistema de apoio à decisão, e não apenas de um mecanismo de busca.

Como evidência de sua aplicabilidade, a solução foi apresentada no ambiente corporativo e aprovada para uso real, sendo adotada como modelo operacional sob o nome Acquisition Client Locator (ACL). Esse resultado reforça a relevância prática do projeto e sua aderência às necessidades do negócio.

Apesar dos resultados positivos, o trabalho apresenta algumas limitações. Como trabalhos futuros, destacam-se oportunidades relevantes de evolução, incluindo:
- o refinamento contínuo das regras de priorização;
- a incorporação de técnicas mais avançadas de NLP, como embeddings semânticos, para melhorar o tratamento de ambiguidades;
- a evolução da camada de apresentação, tornando a solução mais acessível a usuários não técnicos;

Essas melhorias podem ampliar ainda mais o impacto da solução, aumentando sua precisão, escalabilidade e adoção dentro do ambiente corporativo. 

Como consequência do projeto há uma discussão inicial para simplificação do processo e estudo para migração para plataformas existentes no mercado, como SAP e SalesForce.

### 7. Referências

- Arquivos de solicitação e aplicação real armazenados na pasta [Results](https://github.com/leopcdata/bimaster_final/tree/main/results)   

- Código Python nos arquivos main.py, config.py, benchmark.py da pasta principal desse GitHub, e outras funções auxiliares na pasta [utils](https://github.com/leopcdata/bimaster_final/tree/main/utils)

<img width="975" height="470" alt="image" src="https://github.com/user-attachments/assets/20f987d0-7eb3-4b40-a00b-441dee1a406f" />
Figura 7. Terminal de execução no VS code

---
Matrícula: 232100499

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
