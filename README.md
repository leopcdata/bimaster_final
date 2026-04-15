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
#### 3.3 Como Executar

Esta seção descreve os passos necessários para executar a ferramenta localmente. A solução foi desenhada para um ambiente corporativo específico, com acesso a uma base DB2 interna, mas pode ser adaptada para fins de avaliação ou demonstração editando os parâmetros descritos abaixo.

> **Nota sobre privacidade.** O repositório público omite intencionalmente arquivos com credenciais, configurações de servidor e dados reais da empresa. Os caminhos de pastas em `config.py` foram alterados para referências locais genéricas; no uso real, esses caminhos apontam para pastas em armazenamento na nuvem (Box corporativo) compartilhadas entre funcionários autorizados. Da mesma forma, o módulo de credenciais do banco não é versionado e precisa ser recriado localmente conforme descrito em *Configuração* (3.3.3).

#### 3.3.1 Pré-requisitos

- **Python 3.10 ou superior**
- **Driver IBM DB2 instalado** (necessário para a biblioteca `ibm_db` se conectar ao banco corporativo). Em Windows, o caminho padrão usado pelo projeto é `C:\Program Files\IBM\SQLLIB\BIN`.
- **Credenciais de acesso à base corporativa DB2** (fornecidas internamente pela empresa).
- **Bibliotecas Python:** `pandas`, `openpyxl`, `rapidfuzz`, `ibm_db`.

Para instalar as bibliotecas Python:

```bash
pip install pandas openpyxl rapidfuzz ibm_db
```

#### 3.3.2 Instalação

Recomenda-se a criação de um ambiente virtual antes da instalação das dependências:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

pip install pandas openpyxl rapidfuzz ibm_db
```

#### 3.3.3 Configuração

**Passo 1 — Editar `config.py`.** Ajuste os três caminhos no topo do arquivo para pastas existentes na sua máquina:

```python
INPUT_FOLDER = r"C:\caminho\para\seus\arquivos\de\input"
RESULTS_FOLDER = r"C:\caminho\para\salvar\resultados"
CACHE_FOLDER = r"C:\caminho\para\cache"
```

**Passo 2 — Criar `utils/cmdw_config.py`.** Este arquivo não está versionado por conter dados sensíveis. Crie-o localmente com a seguinte estrutura mínima:

```python
def get_db_credentials():
    return {
        "DATABASE": "<nome_do_database>",
        "HOSTNAME": "<endereco_do_servidor>",
        "PORT": "<porta>",
        "PROTOCOL": "TCPIP",
        "UID": "<usuario>",
        "PWD": "<senha>",
    }
```

Substitua os valores entre colchetes pelos dados de acesso fornecidos internamente.

**Passo 3 — Parâmetros opcionais.** O arquivo `config.py` também expõe parâmetros de execução que podem ser ajustados conforme a necessidade:

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `MATCH_LIMIT` | `20` | Número máximo de candidatos retornados por empresa na etapa de matching. |
| `HIGH_CONFIDENCE_THRESHOLD` | `90` | Score mínimo para considerar um candidato de alta confiança. |
| `MID_CONFIDENCE_THRESHOLD` | `50` | Score mínimo para considerar um candidato de fallback. |
| `RUN_BENCHMARK` | `False` | Quando `True`, executa modos sequencial e paralelo na mesma rodada e seleciona o mais rápido. |
| `DEFAULT_EXECUTION_MODE` | `"sequential"` | Modo padrão quando o benchmark não está ativo. Aceita `"sequential"` ou `"parallel"`. |

#### 3.3.4 Formato do arquivo de input

O arquivo de input deve ser um Excel (`.xlsx`) colocado na pasta `INPUT_FOLDER`. A única coluna obrigatória é:

- **`Company`** — nome da empresa a ser mapeada (texto).

O país associado à execução é informado interativamente no momento da execução (ver 3.3.5), e não pelo arquivo de input. Cada execução opera sobre um único país.

Exemplos de inputs e outputs reais (com dados anonimizados ou de demonstração) podem ser consultados na pasta [`results/`](https://github.com/leopcdata/bimaster_final/tree/main/results) do repositório.

#### 3.3.5 Execução

A partir da raiz do projeto, execute:

```bash
python main.py
```

A ferramenta inicia um fluxo interativo no terminal, em duas perguntas:

1. **Seleção do arquivo de input.** O sistema lista todos os arquivos `.xlsx` disponíveis em `INPUT_FOLDER` e solicita que o usuário escolha um pelo número correspondente.
2. **Código do país.** Informe um código numérico de 3 dígitos correspondente ao país-alvo (campo `cca.ctrynum` na base corporativa).

Após essas duas entradas, a execução prossegue automaticamente, com mensagens de log indicando o progresso de cada etapa (extração de dados, processamento por grupo, geração do output).

O resultado é gravado na pasta `RESULTS_FOLDER` como um arquivo Excel com nome no formato:

```
<nome_do_input> ACL results - <YYYY-MM-DD_HH-MM>.xlsx
```
Esse arquivo contém as três abas descritas na Seção 3.4.6 — **Summary**, **Details** e **Metrics**.

O screenshot abaixo mostra um exemplo do fluxo interativo no terminal:
<img width="975" height="470" alt="image" src="https://github.com/user-attachments/assets/20f987d0-7eb3-4b40-a00b-441dee1a406f" />
Figura 1. Terminal de execução no VS code

#### 3.3.6 Modos de execução e benchmark

O modo de execução padrão é **sequencial**, definido por `DEFAULT_EXECUTION_MODE = "sequential"` em `config.py`. Esse modo se mostrou mais eficiente nos testes realizados, por motivos discutidos em *3.5 Estratégia de execução e benchmark*.

Para executar em modo **paralelo**, basta alterar a constante para `"parallel"`.

Para ativar o **benchmark** entre os dois modos na mesma execução, altere `RUN_BENCHMARK = True`. Nesse caso, a ferramenta executa as duas estratégias, registra os tempos comparativos na aba Metrics e usa automaticamente o resultado da estratégia mais rápida para o output final.

#### 3.4 Durante a Execução
#### 3.4.1 Extração de dados

A primeira etapa da solução consiste em obter, da base corporativa, o subconjunto de clientes que será utilizado como universo de busca. Essa etapa é implementada no módulo `utils/db_utils.py` e é acionada por `main.py` logo após a leitura do arquivo de input.

Ao iniciar a execução, a ferramenta solicita ao usuário, de forma interativa, a seleção do arquivo de input entre os disponíveis na pasta configurada e o código de país (3 dígitos) a ser processado. Essa abordagem simplifica o uso por analistas sem exigir edição de parâmetros no código.

A extração é estruturada com três características principais:

- **Uso combinado de Python e SQL** para consultar a base corporativa hospedada em DB2.
- **Parametrização por país**, limitando o conjunto de registros ao mercado relevante para a aquisição. Essa restrição é essencial, pois a base corporativa possui milhões de registros em escala global, e em mercados grandes como os Estados Unidos o volume ultrapassa 470 mil clientes.
- **Cache local em CSV**, armazenado em `CACHE_FOLDER`. Na primeira execução para um país, o resultado da consulta é persistido localmente; em execuções subsequentes, os dados são lidos diretamente do arquivo de cache, evitando reconsultas desnecessárias ao banco. Essa abordagem é adequada ao contexto do projeto, já que a estrutura de clientes é definida no início do ano e tende a permanecer estável ao longo do ciclo.

A consulta retorna, para cada cliente, os seguintes campos principais: identificador e nome da cobertura (`COV_TYPE_ID`), grupos globais e domésticos de buying group (`GBL_BUY_GRP`, `DOM_BUY_GRP`), identificador e nome do global client, nome legal do cliente, listas de segmentação válidas (`acct_list_ids`), indústria e país. Filtros adicionais garantem que apenas clientes ativos, em tipos de cobertura válidos e pertencentes ao grupo de listas oficial da estrutura comercial sejam retornados.

<img width="539" height="303" alt="image" src="https://github.com/user-attachments/assets/c4cf4bff-5df9-435f-a7b4-e5f035105f13" />

Figura 2. Exemplo de entrada do processo - Lista fornecida por um gestor

<img width="629" height="334" alt="image" src="https://github.com/user-attachments/assets/032cc20f-c483-49ce-ac72-3153b1de954c" />

Figura 3. Total de clientes registrados nos EUA por segmento

#### 3.4.2 — Normalização textual

O segundo desafio da solução é lidar com a inconsistência entre os nomes de empresas informados no input e os registrados na base corporativa. Para isso, `utils/normalize.py` implementa uma rotina de normalização que reduz diferenças de formatação sem alterar a identidade da empresa. A normalização aplica as seguintes transformações:

- conversão para minúsculas;
- remoção de espaços extras e pontuação;
- remoção de sufixos societários comuns (Inc, LLC, Corp, Ltda, Group, entre outros);
- remoção de stopwords (palavras pouco relevantes para identificação).

Uma decisão importante do projeto foi **preservar simultaneamente o nome original e sua versão normalizada**. A normalização não substitui a comparação bruta; ela atua como uma camada complementar, permitindo que o matching use as duas representações em sequência.

#### 3.4.3 — Estratégia de matching

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

#### 3.4.4 — Agrupamento por regras de negócio

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

#### 3.4.5 — Priorização e consolidação

Após a geração dos candidatos para todos os grupos, a ferramenta precisa consolidar uma recomendação final por empresa na aba Summary. Essa lógica é implementada em `utils/summary.py` (função `build_summary`), a partir dos candidatos montados em `utils/process_utils.py`.

A priorização trabalha com um threshold mais exigente do que o utilizado na geração de candidatos: a camada de Summary considera apenas candidatos com score **maior ou igual a 90** como de "alta confiança", aplicando a seguinte ordem de decisão para cada empresa:

1. Grupo 1 ou Grupo 2 com score ≥ 90
2. Grupo 3 com score ≥ 90
3. Grupo 4 com score ≥ 90
4. Melhor candidato com score entre 50 e 89, em qualquer grupo
5. Cliente não encontrado

Nos Grupos 3 e 4, quando múltiplos candidatos de alta confiança existem para a mesma conta, a ferramenta prioriza registros em nível de `GBL_BUY_GRP`. Quando uma mesma conta (`ACCT`) aparece associada a mais de um `GBL_CLIENT_ID`, os registros são consolidados em uma única linha no Summary, preenchida com a mensagem *"Multiple Global Client IDs - check Details tab"*, direcionando o analista à aba Details para a decisão final.

Como os candidatos podem surgir a partir de mais de uma etapa de matching (raw e normalizado), foi necessário implementar uma **estratégia de deduplicação** baseada em atributos-chave do resultado, reduzindo repetições e melhorando a qualidade da saída final.

#### 3.4.6 — Geração de outputs

A última etapa é construída em `utils/summary.py` e `utils/metrics.py`, invocadas por `main.py` ao final da execução. O resultado é um único arquivo Excel com três abas:

**Summary** — Recomendação final por empresa, respeitando as regras de priorização. Inclui realces visuais para facilitar a revisão humana:

- **amarelo**: cliente não encontrado;
- **azul claro**: empresas com múltiplas linhas no summary (exigem revisão na aba Details);
- **laranja claro**: registros de Activate Unassigned, que demandam atenção especial por não serem registros ativos no pipeline do ano corrente e exigirem etapas adicionais de processo para ativação.

<img width="886" height="250" alt="image" src="https://github.com/user-attachments/assets/af6640f2-4002-476e-9065-bd7802060717" />

Figura 4. Exemplo de um resultado prático da aplicação

**Details** — Todos os candidatos encontrados pelo motor de matching, com score, nível da conta, atributos de cobertura, buying group, global client, grupo de origem e lista de segmentação.

**Metrics** — Métricas de execução e qualidade organizadas em quatro blocos: visão geral (total de empresas processadas, encontradas e não encontradas, percentuais de cobertura, matches de alta confiança), tempos de execução (total e por grupo, incluindo comparativo entre os modos sequencial e paralelo quando o benchmark está ativo), distribuição de matches por grupo e distribuição de confiança do Summary por faixa de score.

<img width="393" height="194" alt="image" src="https://github.com/user-attachments/assets/49fc9f46-24fb-42c8-aaca-ae46ae8dbe38" />

<img width="394" height="262" alt="image" src="https://github.com/user-attachments/assets/8ffb9f3f-b657-4ef2-9ac5-a3554a40b7f9" />

Figuras 5 e 6. Resultados de métricas


#### 3.5 Estratégia de execução e benchmark

Para avaliar o desempenho da solução, `benchmark.py` implementa duas estratégias de execução que podem ser selecionadas via `config.py`:

- **Sequencial** (`run_groups_sequential`) — processa os quatro grupos um a um.
- **Paralela** (`run_groups_parallel`) — processa os grupos simultaneamente usando um `ThreadPoolExecutor` com um worker por grupo.

O modo padrão é controlado por `DEFAULT_EXECUTION_MODE = "sequential"`. Adicionalmente, ativando `RUN_BENCHMARK = True`, a função `choose_execution()` em `main.py` executa **ambas as estratégias** na mesma rodada, compara os tempos totais e seleciona automaticamente a mais rápida para gerar os outputs, registrando também os tempos comparativos na aba Metrics.

O benchmark mostrou que, no ambiente testado, a execução sequencial apresentou desempenho total superior à paralela. Esse resultado indica que o workload é predominantemente **CPU-bound** — o overhead de criação e sincronização de threads supera os ganhos potenciais de concorrência, limitados pelo GIL do Python para tarefas desse tipo. Com base nessa evidência, a execução sequencial passou a ser o modo padrão, mantendo o benchmark como opção para análises futuras (por exemplo, caso se migre a paralelização para `ProcessPoolExecutor` ou para uma execução distribuída).

#### 3.6 Decisões de projeto e desafios enfrentados

Ao longo do desenvolvimento, algumas decisões exigiram iteração e refinamento. Registrá-las aqui ajuda a evidenciar o raciocínio por trás da solução final e aponta caminhos naturais de evolução.

**Distinção efetiva entre matching bruto e normalizado.** Em uma versão inicial, a análise marcada como "raw" ainda estava operando sobre nomes já normalizados, o que anulava parte do valor da dupla abordagem descrita em 3.5. A correção envolveu separar explicitamente as estruturas de comparação e manter, em paralelo, duas representações do nome do cliente — original e normalizada. Essa separação é o que permite hoje capturar correspondências fortes pela via bruta e, ao mesmo tempo, recuperar casos difíceis pela via normalizada.

**Deduplicação dos candidatos.** Como o mesmo candidato pode ser atingido tanto pela etapa raw quanto pela etapa normalizada, registros repetidos começaram a aparecer na saída. Foi necessário definir uma chave de deduplicação baseada em um conjunto de atributos do resultado (empresa, grupo, nível da conta, identificador da conta, lista de segmentação e score arredondado), aplicada antes da consolidação do Summary. O resultado é uma saída mais limpa, sem linhas redundantes competindo pela atenção do analista.

**Representação das regras de negócio em código.** Traduzir a hierarquia comercial (segmentos, grupos, níveis de cobertura, exceções para contas Strategic) em uma lógica programável exigiu várias iterações. A decisão foi concentrar a configuração dos quatro grupos em `GROUP_CONFIG` dentro de `config.py`, com cada grupo associado a uma função de mapeamento de saída específica em `utils/matching.py`. Essa organização deixa explícito o que cada grupo faz e permite ajustes futuros com esforço localizado, sem propagar alterações pelo resto do código.

**Variação entre mercados e países.** A estrutura de cobertura não é universal: cada país pode definir suas próprias regras e estratégias locais para agrupar clientes, desde que alinhadas ao modelo comercial global. Além disso, a estrutura é revisada a cada planejamento anual e depois permanece congelada durante o ciclo de execução. Isso reforça a necessidade de acertar o mapeamento no momento certo, já que a configuração inicial do território terá impacto durante todo o período de vigência do plano de vendas. A parametrização por país e o cache local descritos em *3.4.1 (Extração de dados)* endereçam parte desse desafio, mas a lógica de grupos e exceções ainda reflete o modelo comercial global — uma evolução natural seria permitir configurações por país.

**Modularização do código.** A primeira versão concentrava responsabilidades de acesso a dados, matching, priorização e apresentação em um único arquivo. À medida que novas funcionalidades foram sendo adicionadas (benchmark, métricas, realces visuais), a manutenção tornou-se progressivamente mais difícil. A reorganização em módulos descrita em 3.2 foi uma refatoração importante: isolou responsabilidades, reduziu acoplamento e tornou mais simples o trabalho de evolução futura.

**Escolha entre execução sequencial e paralela.** A paralelização por grupos via `ThreadPoolExecutor` foi implementada esperando ganho de tempo, mas o benchmark descrito em 3.5 revelou que a versão sequencial é mais rápida no ambiente atual. Essa decisão baseada em medição é um bom exemplo de como a ferramenta incorporou observabilidade do próprio desempenho (aba Metrics) como critério de escolha, em vez de assumir que paralelismo seria sempre preferível.

### 4. Resultados

O principal resultado deste trabalho foi a transformação de um processo predominantemente manual, custoso e pouco escalável em uma solução automatizada, estruturada e orientada por regras de negócio, aplicando conceitos de sistemas inteligentes de apoio à decisão diretamente em um processo corporativo real, complexo e sensível para a operação comercial da empresa.

#### 4.1 Ganho operacional

O ponto mais imediato do impacto da solução é a mudança de escala temporal do processo. Sob a abordagem manual, cada cliente da lista recebida do gestor exigia em média cerca de quatro minutos de análise individual: consulta à base corporativa via intranet, comparação textual entre o nome informado e o nome legal registrado, interpretação da estrutura comercial aplicável e decisão sobre o nível mais adequado da hierarquia. Em integrações de aquisição com centenas de clientes, esse esforço se acumulava em vários dias de trabalho de uma equipe inteira.

Com a ferramenta, o mesmo volume de entradas passou a ser processado em segundos, com a análise individual restrita aos casos efetivamente ambíguos. Em termos práticos, isso significa que um processo que antes demandava o envolvimento de uma equipe ao longo de dias passou a poder ser executado por um único analista em uma sessão de trabalho. Para esses casos ambíguos, o output já entrega as informações necessárias e o score de similaridade que apoiam a tomada de decisão, eliminando a etapa de busca e estruturação manual que consumia a maior parte do tempo.

#### 4.2 Qualidade e suporte à decisão

A automação proposta vai além da simples redução de esforço operacional. A ferramenta apoia uma decisão tecnicamente mais sofisticada do que a comparação textual isolada: ela recomenda o nível mais adequado dentro de uma estrutura comercial hierárquica, na qual diferentes segmentos e tipos de cobertura possuem papéis distintos na definição dos territórios de venda. Esse tratamento por grupos de negócio, com regras de saída e priorização específicas, é o que diferencia o sistema de um simples mecanismo de busca textual.

Em casos ambíguos, em que nenhum candidato isolado é claramente o melhor, a ferramenta continua agregando valor: ao invés de uma resposta única e potencialmente errada, ela apresenta um conjunto reduzido e ordenado de candidatos plausíveis, com score de similaridade e atributos relevantes para a decisão final. O Summary destaca explicitamente essas situações por meio de realces visuais (azul claro para empresas com múltiplas linhas, amarelo para clientes não encontrados, laranja claro para registros de Activate Unassigned), direcionando a atenção do analista para onde de fato é necessária. O resultado é uma divisão de trabalho mais inteligente entre máquina e ser humano: a máquina filtra e ordena, o analista decide.

A padronização proporcionada pela ferramenta também contribui para a consistência das recomendações entre execuções e entre analistas distintos. Em vez de depender da experiência individual de quem conduz a análise, o processo passa a seguir um conjunto explícito de regras documentadas em código, o que melhora a governança e reduz a variabilidade dos mapeamentos.

#### 4.3 Limitações observadas e qualidade da base

A análise dos resultados expôs também limitações estruturais da base corporativa que vão além do escopo da ferramenta, mas que afetam diretamente a qualidade dos mapeamentos. Um exemplo ilustrativo é o caso da MGM Studios: vendida pela Disney à Amazon em 2022, ainda aparece em ambos os registros no sistema, gerando candidatos concorrentes para a mesma entrada de input. Casos como esse mostram que, mesmo com uma estratégia de matching robusta, a presença de registros desatualizados na base pode produzir ambiguidades que nenhuma técnica textual resolveria sozinha.

<img width="975" height="100" alt="image" src="https://github.com/user-attachments/assets/0345b1f9-053f-4c58-b236-8b44f908351e" />

Figura 7. Exemplo de dados desatualizados no sistema

Essa observação é, ela própria, um resultado relevante do trabalho: ao expor de forma sistemática situações que antes ficavam diluídas no esforço manual, a ferramenta evidencia oportunidades concretas de melhoria de qualidade de dados na origem.

#### 4.4 Adoção da solução no ambiente corporativo

O resultado mais significativo do projeto, do ponto de vista de validação, foi sua adoção como ferramenta operacional no ambiente corporativo. Após apresentação à área responsável e validação dos resultados em casos reais de aquisição, a solução foi formalmente aprovada para uso e incorporada ao processo de integração de vendedores sob o nome **Acquisition Client Locator (ACL)**.

Essa adoção tem várias implicações que reforçam a relevância prática do trabalho:

- **Validação por usuários reais.** A ferramenta está sendo usada por analistas que conhecem profundamente o processo manual original. A aprovação por essa audiência crítica é um indicador forte de que a solução atende às necessidades operacionais reais e não apenas às idealizadas em projeto.
- **Substituição de um processo estabelecido.** O ACL substituiu, na prática, o fluxo manual baseado em planilhas e consultas individuais. Isso exigiu não apenas a qualidade técnica da ferramenta, mas também confiança suficiente da equipe para reorganizar uma rotina consolidada.
- **Estabelecimento como padrão operacional.** Ao receber um nome próprio e ser incorporada ao fluxo oficial, a solução passou a integrar a infraestrutura informal da área, o que tende a garantir uso continuado e criar demanda natural por evolução.
- **Visibilidade interna.** A adoção transformou o projeto em um caso concreto dentro da empresa, gerando inclusive a discussão inicial sobre simplificação mais ampla do processo de mapeamento, com possibilidade de migração para plataformas corporativas como SAP e Salesforce no médio prazo.

#### 4.5 Síntese técnica

Como contribuição técnica, o projeto integra em uma única pipeline coerente um conjunto de elementos que normalmente aparecem isolados em soluções pontuais:

- conexão direta com a base corporativa em DB2 e extração estruturada de dados;
- normalização textual com preservação simultânea do nome original;
- fuzzy matching com biblioteca especializada (RapidFuzz);
- agrupamento por regras de negócio com mapeamentos de saída específicos por grupo;
- priorização hierárquica com thresholds de confiança em duas camadas;
- mensuração contínua de performance e qualidade via aba Metrics dedicada;
- output estruturado em três abas com realces visuais para revisão humana.

Essa integração é o que permite que o ACL ofereça, com o mesmo arquivo Excel de saída, uma camada de recomendação direta (Summary), uma camada de análise detalhada (Details) e uma camada de observabilidade do próprio processo (Metrics).

---

### 5. Conclusões

Este trabalho teve como objetivo reduzir a dependência de um processo manual, demorado e pouco escalável no mapeamento de clientes oriundos de aquisições — etapa crítica para a integração de vendedores em uma grande empresa de tecnologia, com impacto direto na definição de territórios, metas e remuneração variável.

A solução proposta demonstrou que é possível estruturar esse processo por meio da combinação de técnicas de processamento de linguagem natural e regras de negócio, transformando uma atividade predominantemente manual em uma pipeline automatizada, reprodutível e orientada à decisão. Os resultados obtidos confirmam a viabilidade técnica da abordagem e, principalmente, sua aderência às necessidades reais do negócio.

Do ponto de vista prático, três ganhos se destacam. O primeiro é o **ganho de eficiência operacional**: a redução de tempo é da ordem de várias dias-pessoa para uma sessão de trabalho de um único analista, liberando capacidade da equipe para atividades de maior valor agregado. O segundo é o **ganho de consistência**: ao codificar as regras de mapeamento, a solução garante que decisões equivalentes sejam tomadas para entradas equivalentes, reduzindo a variabilidade introduzida pelo julgamento individual. O terceiro é o **ganho de governança**: o output estruturado, com score de similaridade, candidatos alternativos e métricas de execução, deixa rastro auditável do raciocínio aplicado em cada recomendação.

Um diferencial importante do projeto está em ter ido além da identificação textual de correspondências. A solução incorpora a hierarquia comercial da organização, com seus segmentos, grupos e níveis de cobertura, e aplica regras de priorização que refletem a prática operacional. É essa camada de regras de negócio embutidas que aproxima a ferramenta de um efetivo sistema de apoio à decisão, e não apenas de um motor de busca aproximada.

A evidência mais forte da relevância prática do trabalho é a adoção da solução no ambiente corporativo sob o nome **Acquisition Client Locator (ACL)**. A transição de um experimento de MBA para uma ferramenta efetivamente utilizada em integrações reais de aquisição valida o desenho técnico e mostra que a solução respondeu a uma dor concreta do negócio. Essa adoção também posicionou o projeto como referência interna para discussões mais amplas sobre simplificação e modernização do processo de mapeamento.

Por fim, o trabalho reforça uma reflexão de natureza mais ampla sobre o papel de soluções de apoio à decisão em ambientes corporativos: o maior ganho não veio de algoritmos sofisticados isolados, mas da combinação cuidadosa de técnicas relativamente simples (fuzzy matching, normalização textual, regras hierárquicas) com um entendimento profundo do problema de negócio. A modelagem das regras de priorização e a estruturação dos grupos de contas exigiram tanto trabalho quanto a parte algorítmica — e foi essa integração entre técnica e domínio que permitiu o resultado final.

#### Trabalhos Futuros

Apesar dos resultados alcançados, o projeto apresenta limitações conhecidas e várias frentes naturais de evolução. Algumas delas já foram identificadas durante o uso da ferramenta no ambiente corporativo e podem ampliar significativamente o impacto da solução.

**Avaliação quantitativa sistemática.** A próxima etapa de evolução mais imediata é a construção de um conjunto de teste rotulado (golden set) com casos representativos de cada grupo de negócio, permitindo medir métricas formais como acurácia top-1, acurácia top-k, precisão e recall do matching. Essa avaliação permitiria também calibrar de forma fundamentada os thresholds de confiança hoje definidos empiricamente.

**Incorporação de técnicas avançadas de NLP.** A estratégia atual baseada em fuzzy matching textual é eficaz para a maioria dos casos, mas tem limitações em situações de ambiguidade semântica (como o exemplo "As America" descrito na Seção 3.5). A incorporação de embeddings semânticos via modelos pré-treinados (como sentence-transformers) poderia melhorar significativamente o tratamento desses casos, ao capturar similaridade de significado e não apenas de forma.

**Refinamento contínuo das regras de priorização.** A estrutura atual de quatro grupos com regras de saída específicas atende ao modelo comercial atual, mas é razoável esperar que ajustes sejam necessários a cada ciclo de planejamento. Documentar e versionar essas regras, e potencialmente extrair sua configuração para um arquivo externo editável por usuários de negócio, tornaria a manutenção menos dependente de mudanças no código.

**Adaptação por mercado e país.** Como discutido em *3.6 (Decisões de projeto)*, a estrutura de cobertura pode variar entre países. Uma evolução natural seria permitir configurações de grupos e exceções específicas por mercado, sem perder a unidade do modelo global.

**Evolução da camada de apresentação.** O output atual em Excel é eficiente para analistas familiarizados com o processo, mas limita a adoção por outros perfis. Uma interface web simples, possivelmente em Streamlit ou Flask, poderia tornar a ferramenta acessível a usuários não técnicos, com upload de arquivo, escolha de país e visualização interativa dos resultados.

**Loop de aprendizado a partir das correções manuais.** Cada vez que um analista corrige manualmente uma recomendação do Summary, está produzindo um sinal valioso sobre onde a ferramenta erra. Capturar essas correções de forma estruturada, com posterior análise agregada, permitiria identificar padrões de erro e priorizar melhorias com base em evidência, em vez de intuição.

**Integração com plataformas corporativas.** No médio e longo prazo, há discussão interna sobre simplificação mais ampla do processo de mapeamento, possivelmente migrando partes da lógica para plataformas estabelecidas como SAP ou Salesforce. O ACL, nesse cenário, pode servir tanto como referência funcional quanto como prova de conceito do tipo de regras de negócio que precisariam ser implementadas nessas plataformas.

Essas frentes não são mutuamente exclusivas e podem ser priorizadas conforme as necessidades do negócio e a disponibilidade de tempo de desenvolvimento. Em conjunto, sinalizam que o ACL, embora já em produção, ainda tem espaço significativo para crescer em precisão, escalabilidade e alcance dentro da organização.

---
Matrícula: 232100499

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
