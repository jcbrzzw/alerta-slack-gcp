# 🚀 Alerta de Catálogo no Slack

Este projeto automatiza a auditoria de pedidos no Google BigQuery e notifica via Slack produtos que estão pendentes de correção de catálogo há um determinado número de dias.

# 🛠️ Arquitetura do Projeto
O script realiza uma consulta SQL no BigQuery cruzando tabelas de itens, produtos e ordens, tratando os dados em tempo real e disparando alertas visuais no Slack.

# 📋 Pré-requisitos

Python 3.x instalado.

Google Cloud Project com a API do BigQuery ativada.

Conta de Serviço (Service Account) com permissão de BigQuery Data Viewer no dataset.

Webhook do Slack configurado no seu canal de destino.

# ⚙️ Configuração Passo a Passo
1. Preparação do Ambiente
Após clonar o repositório, certifique-se de que a estrutura de arquivos esteja assim:
<img width="597" height="138" alt="image" src="https://github.com/user-attachments/assets/6ba492be-ef4f-4fe3-9d4f-8d699c74c4d4" />


2. Configuração de Segredos
Crie o arquivo .env na raiz do projeto e adicione suas variáveis:
<img width="608" height="59" alt="image" src="https://github.com/user-attachments/assets/f5fbbbb7-de58-4973-a3a8-63a126c71582" />

O arquivo credenciais.json deve ser baixado do console do Google Cloud (IAM > Contas de Serviço > Chaves) e salvo na raiz com esse nome exato.

3. Instalação de Dependências
No seu terminal dentro da pasta do projeto, execute:

<img width="324" height="42" alt="image" src="https://github.com/user-attachments/assets/1a2fb600-7b77-4fe5-80f3-4bdfe4846925" />

5. Execução
Para rodar o monitoramento manualmente:

<img width="186" height="43" alt="image" src="https://github.com/user-attachments/assets/930e1bdd-9116-41e7-bfd9-a3d9fc01fa1a" />

# 📊 Estrutura de Notificação
O sistema utiliza attachments do Slack para exibir informações detalhadas, incluindo:

Título: Indicador de urgência do prazo.

Pedido: Identificador único.

Dados do Produto: Nome, preço e quantidade.

# 🛡️ Segurança 
Nunca compartilhe seu arquivo credenciais.json ou seu .env.

Certifique-se de que o seu arquivo .gitignore contenha estas duas linhas para evitar vazamento de dados sensíveis no Git:

<img width="239" height="56" alt="image" src="https://github.com/user-attachments/assets/e778e813-018c-40a3-b174-acfa6aa06ddf" />

# 📈 Automação e Orquestração
Existem duas formas principais de colocar seu monitoramento em produção:

1. Caminho Serverless
Ideal para projetos leves, baixo custo e configuração rápida.

Cloud Functions: Aloja o seu script main.py de forma isolada na nuvem.

Cloud Scheduler: Atua como um despertador, disparando a execução da sua Cloud Function via HTTP em horários específicos (ex: diariamente às 09:00).

2. Caminho Profissional: Apache Airflow - Recomendado para escala
Se o seu volume de dados crescer ou se você precisar criar dependências ex: só notificar o Slack se o BigQuery carregar os dados primeiro, a recomendação é usar o Cloud Composer o serviço gerenciado do Airflow no GCP.

O Airflow transforma seu script em um DAG - Directed Acyclic Graph.

# Vantagens:

Se a API do Slack falhar, o Airflow tenta novamente sozinho.

Interface dedicada para ver logs e histórico de execução de cada tarefa.

Facilita a criação de fluxos de trabalho complexos onde várias etapas se conectam.


## Notificação
Abaixo, é o print de como o alerta aparece no Slack:

<img width="958" height="478" alt="image" src="https://github.com/user-attachments/assets/a99a3a41-eed8-47a5-8b71-60333ccbf3f1" />

