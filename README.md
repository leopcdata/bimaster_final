#### Aluno: [Leonardo Cardoso](https://github.com/leopcdata)
#### Orientadora: Evelyn Batista
---
Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

- [Link para o código](https://github.com/leopcdata/bimaster_final)

---

### Resumo

Este trabalho apresenta o desenvolvimento de uma ferramenta em Python de apoio à decisão para automatizar e padronizar o processo de identificação e classificação de clientes no contexto de integração de empresas adquiridas (Mergers & Acquistions) em uma grande organização global. O problema surgiu a partir da aceleração da estratégia de aquisições e da redução do prazo de integração para menos de um ano, o que aumentou significativamente a pressão sobre processos operacionais da área de Sales Compensation.

Nesse contexto, a correta configuração dos territórios como parte do contrato assinado por cada vendedos é essencial para a definição dos planos de venda, cálculo de metas e pagamento de comissões. No caso de vendedores oriundos de aquisições, um dos passos críticos da integração consiste em mapear corretamente os clientes que passarão a compor seus territórios. Atualmente, esse processo é realizado manualmente, com base em planilhas enviadas pelos gestores de vendas contendo milhares de empresas, exigindo busca individual em uma base corporativa com milhões de registros ativos e análise da posição hierárquica de cada cliente dentro da estrutura comercial da organização.

A complexidade do processo decorre de diferentes fatores: variações de grafia, abreviações, sufixos societários, nomes fantasia, dados antigos ainda ativos na base e múltiplos níveis hierárquicos de segmentação comercial. A solução proposta utiliza extração de dados em DB2, normalização textual, fuzzy matching, regras de priorização por grupos de contas e geração de saídas estruturadas para apoiar a tomada de decisão. Como resultado, a ferramenta busca reduzir drasticamente o esforço manual, aumentar a consistência do processo, melhorar a acurácia do mapping e acelerar a integração comercial de empresas adquiridas.

### Abstract

This project presents the development of a Python-based decision support tool to automate and standardize the customer identification and classification process in the context of acquired-company integration within a large global organization. The problem emerged as the organization accelerated its acquisition strategy and reduced the integration timeline to less than one year, significantly increasing pressure on operational processes within Sales Compensation.

In this environment, the correct configuration of sales territories is essential for defining sales plans, calculating quotas, and enabling commission payments. For sellers joining through acquisitions, one of the most critical integration steps is accurately mapping the customer list that will compose their territories. Today this activity is performed manually, based on spreadsheets provided by sales managers and containing thousands of companies. Each company must be searched individually in a corporate customer base with millions of active records, while also being classified within the organization’s commercial hierarchy.

The complexity of the process comes from several factors: spelling variations, abbreviations, legal suffixes, trade names, outdated records that remain active in the database, and multiple hierarchical levels within the commercial segmentation model. The proposed solution uses DB2 data extraction, text normalization, fuzzy matching, account-group prioritization rules, and structured outputs to support decision-making. As a result, the tool aims to drastically reduce manual effort, improve process consistency, increase mapping accuracy, and accelerate the commercial integration of acquired companies.

### 1. Introdução

Atuo no departamento de Sales Compensation de uma grande empresa global de tecnologia, área responsável por processos que vão desde a criação dos planos de venda até o pagamento da comissão dos vendedores. Dentro desse contexto, a correta definição dos clientes que compõem o território de cada vendedor é fundamental, pois influencia diretamente o cálculo de metas, a elegibilidade de vendas e o pagamento de comissão ao longo do ano.

Nos últimos anos, a companhia acelerou sua estratégia de aquisições e reduziu o prazo de integração para menos de um ano. Essa mudança trouxe um desafio importante para minha área: integrar mais rapidamente vendedores vindos de empresas adquiridas, junto com suas respectivas carteiras de clientes, sem comprometer a qualidade do processo. Um dos passos essenciais dessa integração é mapear a carta de clientes para que os territórios dos vendedores migrando sejam configurados corretamente no sistema corporativo.

Hoje esse processo é totalmente manual. Os gerentes de vendas da empresa adquirida enviam uma planilha contendo os nomes das empresas e os países das contas que o vendedor deve cobrir. A partir dessa lista, os analistas precisam buscar individualmente cada empresa na plataforma corporativa de registro de clientes, comparar múltiplos resultados e decidir qual conta representa melhor aquela empresa dentro da hierarquia comercial vigente.

Essa atividade consome muito tempo e esforço. Em uma integração recente, cerca de 10 pessoas precisaram trabalhar durante aproximadamente uma semana inteira apenas para concluir a etapa de mapping. O esforço é alto porque a base possui milhões de entradas ativas e uma única busca pode retornar dezenas ou até centenas de resultados possíveis.

Além do volume, há também um problema de qualidade e ambiguidade dos dados. Os nomes das empresas fornecidos pelos gestores nem sempre seguem o mesmo padrão da base interna. É comum encontrar diferenças de grafia, vírgulas, sufixos como “Inc.”, “LLC”, “Ltda”, abreviações, siglas internas, nomes fantasia e outras variações. Isso inviabiliza uma solução baseada apenas em busca exata de texto.

Outro fator que torna a tarefa ainda mais complexa é que o analista não precisa apenas encontrar um nome semelhante. Ele precisa decidir em qual mercado e em qual nível da segmentação comercial aquela conta se encontra. Em outras palavras, o problema não é somente “qual registro parece mais com esse nome?”, mas sim “qual é o nível hierárquico mais adequado para configurar corretamente o território do vendedor?”.

Esse ponto é especialmente relevante porque a estrutura comercial utilizada pela organização não é plana. Em 2026, os clientes estão distribuídos em quatro grandes segmentos (Go-to-Market), que refletem diferentes níveis de dedicação comercial:

- **Enterprise**
- **Strategic**
- **Select Horizon**
- **Select Territory**

Nos segmentos Enterprise, Strategic e Horizon, é comum que clientes relevantes possuam estruturas de cobertura mais dedicadas, muitas vezes associadas a um identificador específico. Já no segmento Select Territory, milhares de clientes podem estar agrupados em estruturas mais amplas, definidas por critérios como geografia, indústria ou combinação entre ambos.

A cobertura é um dos principais blocos de construção usados para definir territórios de vendedores. Em alguns casos, uma cobertura representa praticamente um cliente individual; em outros, representa um agrupamento de dezenas ou milhares de clientes. Isso torna a decisão de mapping mais sofisticada do que uma simples comparação textual, já que é preciso escolher não só um nome correspondente, mas o nível correto dentro da estrutura comercial.

Grandes clientes costumam possuir uma hierarquia dedicada. Por isso, quando uma busca retorna tanto uma estrutura específica de um grande grupo econômico quanto uma estrutura mais genérica de mercado ou indústria, a recomendação correta deve priorizar a estrutura dedicada. Essa decisão é importante porque garante que o vendedor receba corretamente por oportunidades relacionadas a toda a organização e suas afiliadas, e não apenas por uma classificação genérica mais ampla.

Do ponto de vista de negócio, a importância desse mapping é alta. Os planos de venda são oferecidos no início do ano e, depois disso, só podem ser alterados em condições muito específicas. Esses planos são compostos basicamente pelos clientes que o vendedor deve atender e pelos produtos que deve vender. Com base nesses parâmetros, o sistema calcula metas usando histórico dos clientes e estratégia de crescimento. Por isso, é essencial atribuir o cliente corretamente já na origem, pois não é possível ir adicionando clientes e metas ao longo do ano conforme novas oportunidades surgem, já que isso seria interpretado como manipulação de comissão.

Diante desse cenário, este trabalho propõe a construção de uma ferramenta de apoio à decisão capaz de reduzir o esforço manual, padronizar o processo, aumentar a acurácia do mapping e permitir decisões mais rápidas e consistentes.

### 2. Modelagem

A proposta desenvolvida neste trabalho consiste em uma ferramenta em Python de apoio à decisão para automatizar a etapa de identificação e recomendação de contas no processo de integração de vendedores vindos de aquisições. A ferramenta não substitui totalmente o julgamento humano, mas automatiza a parte mais custosa do fluxo: busca inicial, comparação textual, classificação preliminar e priorização de candidatos.

A modelagem da solução foi construída em etapas, buscando refletir o processo real executado pelos analistas, mas de forma estruturada, mensurável e reproduzível.

O processo se inicia quando um gerente de vendas envia uma lista de clientes que devem ser adicionados ao seu território de vendas e do seu time. Segue um exemplo:

<img width="539" height="303" alt="image" src="https://github.com/user-attachments/assets/c4cf4bff-5df9-435f-a7b4-e5f035105f13" />


#### 2.1 Extração de dados

A partir da lista de clientes recebida o processo se inicia com a extração de dados.

•	Uso combinado de Python and SQL para extração de dados
•	Cache local por país para reduzir a quantidade de consultas em SQL e melhorar a performance.*
•	Parâmetros de buscas a nível de país

Quando um país é executado pela primeira vez, há conexão ao Banco de dados por meio extração por consulta SQL e armazenamento local. Quando a consulta já foi executada anteriormente para um determinado código de país, a consulta é feita diretamente ao arquivo cache anteriormente criado, evitando reconsultas desnecessárias ao banco e reduzindo o tempo de processamento. Isso foi feito considerando que esses dados são definidos para todo ano e não podem ser alterados, salvo exceções.

A consulta retorna, entre outros campos:
- identificador e nome da cobertura
- grupos globais e domésticos de buying group
- identificador e nome do global client
- nome legal do cliente
- listas de segmentação válidas
- indústria
- país

Mostrando como exemplo a base de clientes nos EUA apenas, lugar de maior volume de negócios, há registros de 470 mil clientes. Considerando o mundo todo, são milhões de registros.
- <img width="629" height="334" alt="image" src="https://github.com/user-attachments/assets/032cc20f-c483-49ce-ac72-3153b1de954c" />


#### 2.2 Normalização textual

O segundo desafio foi tratar a inconsistência dos nomes das empresas no input e na base interna. Para lidar com isso, foi criada uma rotina de normalização textual por meio de:
•	conversão para minúsculas
•	remoção de espaços extras e pontuação
•	remoção de termos societários comuns, como “Inc”, “LLC”, “Corp”, “Ltda”, “Group”, e palavras irrelevantes no contexto (stopwords)

A normalização não substitui a comparação bruta, mas complementa a análise. Essa foi uma decisão importante do projeto: preservar tanto o nome original quanto o nome normalizado, em vez de depender apenas de um formato tratado.

#### 2.3 Estratégia de matching

A solução adotada utiliza duas abordagens complementares:

**Raw matching**  
Compara o nome original da empresa fornecida no input com o nome legal original do cliente na base.

**Normalized matching**  
Compara as versões normalizadas dos dois nomes.

A execução ocorre em duas etapas:
1. primeiro é feito o raw matching
2. depois, quando necessário, é feito o normalized matching

Esse desenho foi importante porque permitiu capturar casos de igualdade textual forte sem abrir mão de uma segunda camada mais flexível para tratar variações.

Para o cálculo de similaridade, foi utilizado fuzzy matching (biblioteca RapidFuzz) como técnica de comparação aproximada de strings para medir a similaridade entre textos mesmo quando há variações, erros de digitação ou diferenças de formatação. O algoritmo gera scores de similaridade de 0 - 100 entre os nomes e registra candidatos conforme faixas de confiança. Nesta aplicação, ela compara o Nome da Empresa de entrada com os Nomes Legais dos Clientes.
- candidatos de alta confiança: score igual ou maior que 80 durante a geração
- candidatos de fallback: matches normalizados entre 60 e 80 quando não há match normalizado mais forte

Essa abordagem é especialmente importante para evitar problemas de substring simples. Um exemplo é o caso de “AON”. Se fosse usada apenas uma busca por trecho, resultados como “Kaonmedia” poderiam aparecer como candidatos indevidos. O uso de similaridade textual com critérios adicionais reduz esse risco.

Outros desafios ainda persistem, como no exemplo de entrada -  'As America, Inc' que retorna pontuações semelhantes encontradas para: 'Asm America' e 'JAS America'. Isso abre espaço para pontos de melhoria e criações de regras adicionais, considerando tanto os parâmetros hierárquicos do negócio como técnicas adicionais de comparação de string.


#### 2.4 Agrupamento por regras de negócio

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

#### 2.5 Regras de priorização

Após gerar todos os candidatos, a ferramenta precisa recomendar um resultado final por empresa no Summary. Para isso, foi criada uma lógica de priorização baseada nos grupos e na confiança dos scores.

A ordem atual de priorização é:
1. Grupo 1 e Grupo 2 com probabilidade maior ou igual a 90
2. Grupo 3 com probabilidade maior ou igual a 90
3. Grupo 4 com probabilidade maior ou igual a 90
4. melhor candidato entre 50 e 90
5. cliente não encontrado

Nos Grupos 3 e 4, quando múltiplos candidatos de alta confiança existem para a mesma conta, a ferramenta prioriza registros em nível de **GBL_BUY_GRP** quando disponíveis. Caso existam múltiplos Global Client IDs para a mesma conta, os registros são consolidados em uma única linha no Summary com a mensagem:

`Multiple Global Client IDs - check Details tab`

Essa decisão direciona a revisão humana para a aba de detalhes quando necessário.

#### 2.6 Estrutura de saída

A ferramenta produz três abas principais:

**Details**  
Contém todos os candidatos encontrados pelo motor de matching, com score, nível da conta, atributos de cobertura, buying group, global client, grupo de origem e lista de segmentação.

**Summary**  
Contém a recomendação final por empresa, respeitando as regras de prioridade.

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

Além disso, o Summary possui realces visuais para facilitar a revisão:
- **amarelo**: cliente não encontrado
- **azul claro**: empresas com múltiplas linhas no summary
- **laranja claro**: registros de Activate Unassigned

No caso de **Activate Unassigned**, demandam uma atenção importante no projeto: entradas classificadas nesse grupo necessitam etapas adicionais de processo para garantir a ativação dessas contas e consequentemente o pagamento de comissão para o vendedor.

#### 2.7 Desafios enfrentados e soluções encontradas

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
Outro desafio relevante é que a estrutura de cobertura não é universal e pode variar entre países e mercados. Cada unidade geográfica pode definir suas próprias regras e estratégias locais para agrupar clientes, desde que alinhadas ao modelo comercial global. Além disso, a estrutura de cobertura é revisada a cada ciclo de planejamento e depois permanece congelada durante o ciclo de execução. Isso reforça a necessidade de tomar a decisão correta no momento do mapping, já que a configuração inicial do território terá impacto durante todo o período de vigência do plano de venda.

### 3. Resultados

O principal resultado do projeto foi transformar um processo altamente manual e distribuído em uma solução automatizada, estruturada e orientada por regras de negócio.

A ferramenta consegue:
- receber uma lista de empresas e um país
- extrair a base relevante do banco
- normalizar nomes
- gerar candidatos com fuzzy matching
- aplicar priorização por grupos de negócio
- recomendar uma saída final por empresa
- destacar visualmente casos que exigem atenção
- produzir métricas de execução e qualidade

Do ponto de vista operacional, isso representa uma redução significativa do esforço manual. Em vez de exigir busca individual e análise isolada para cada empresa, a ferramenta entrega um conjunto estruturado de candidatos e uma recomendação inicial, permitindo que o analista concentre seu tempo apenas nos casos ambíguos ou excepcionais.

Do ponto de vista de qualidade, a solução traz mais consistência. O processo deixa de depender exclusivamente da interpretação individual de cada analista e passa a seguir regras padronizadas, replicáveis e documentadas.

Do ponto de vista analítico, a inclusão da aba de métricas trouxe valor adicional. A partir dela, passou a ser possível medir:
- percentual de empresas encontradas
- percentual de empresas não encontradas
- percentual de matches por grupo
- quantidade de resultados com alta confiança
- empresas com múltiplos resultados no Summary
- tempo por empresa processada

Os resultados do projeto mostram que a automação não apenas reduz o esforço de busca e comparação textual, mas também apoia uma decisão mais sofisticada: recomendar o nível mais adequado dentro de uma estrutura comercial hierárquica, na qual diferentes segmentos e coberturas possuem papéis distintos na definição dos territórios.

Mesmo quando a ferramenta não consegue decidir automaticamente uma única resposta ideal, ela ainda gera valor relevante ao reduzir o universo de busca e apresentar os candidatos mais plausíveis de forma organizada, deixando claro onde há conflito e onde a revisão humana é necessária. Há espaço para melhora com a inclusão de outras técnicas de comparação de string, considerando também a estrutura do modelo da empresa. A presença de registros desatualizados e irrelevantes, como no exemplo abaixo da MGM studios que foi vendida da Disney para Amazon em 2022, embora ambos registros ainda permaneçam no sistema, levou a uma discussão sobre mudança de plataforma.

<img width="975" height="100" alt="image" src="https://github.com/user-attachments/assets/0345b1f9-053f-4c58-b236-8b44f908351e" />


Output da execução no VS code:
<img width="975" height="470" alt="image" src="https://github.com/user-attachments/assets/20f987d0-7eb3-4b40-a00b-441dee1a406f" />


### 4. Conclusões

Este trabalho aplica conceitos de sistemas inteligentes de apoio à decisão diretamente em um processo corporativo real, complexo e sensível para o negócio.

A ferramenta proposta endereça um problema crítico no contexto de aquisições: a correta identificação e classificação de clientes para composição de territórios comerciais. Essa etapa, embora operacional em aparência, tem impacto estratégico na definição de metas, no alinhamento dos planos de venda e na integridade do fluxo de comissão.

Como contribuição prática, o projeto oferece uma solução que reduz drasticamente o esforço manual, melhora a consistência do processo, acelera decisões e cria uma base estruturada para evolução contínua.

Como contribuição técnica, o projeto integra:
- conexão com DB2
- extração estruturada de dados
- normalização textual
- fuzzy matching
- regras hierárquicas de priorização
- mensuração de performance e qualidade
- output estruturado para decisão

Como contribuição acadêmica, o trabalho mostra como combinar tratamento de dados, lógica de negócio e critérios de decisão em uma ferramenta aplicada a um contexto real de apoio à decisão.

Entre as limitações e próximos passos, destacam-se:
- refinamento contínuo das regras de priorização
- ampliação do conjunto de métricas
- criação de amostras validadas para medir precisão de forma mais formal
- possível incorporação de abordagens mais avançadas de NLP para melhorar o tratamento de ambiguidades
- evolução da camada de apresentação para facilitar o uso por mais analistas

Em síntese, o projeto mostra que é possível transformar um processo manual, demorado e sujeito a inconsistências em um fluxo mais inteligente, mensurável, escalável e alinhado às necessidades do negócio.

A apresentação da solução no meio corporativo resultou em duas decisões:
- Aplicação prática imediata
- Estudo inicial para simplificação do processo e potencial migração para SAP

---

Matrícula: 232100499

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
