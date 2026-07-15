# 🚀 Alerta de Catálogo no Slack

Este projeto automatiza a auditoria de pedidos no Google BigQuery e notifica via Slack produtos que estão pendentes de correção de catálogo há um determinado número de dias.

# 🛠️ Arquitetura do Projeto
O script realiza uma consulta SQL no BigQuery cruzando tabelas de itens, produtos e ordens, tratando os dados em tempo real e disparando alertas visuais no Slack.

# 📋 Pré-requisitos

- Python 3.x instalado.
- Google Cloud Project com a API do BigQuery ativada.
- Conta de Serviço (Service Account) com permissão de BigQuery Data Viewer no dataset.
- Webhook do Slack configurado no seu canal de destino.

# ⚙️ Configuração Passo a Passo
1. Preparação do Ambiente
Após clonar o repositório, certifique-se de que a estrutura de arquivos esteja assim:

```
alerta-catalogo-gcp/
├── main.py            # Script principal
├── .env               # Variáveis de ambiente (não versionar)
├── credenciais.json   # Chave da conta de serviço (não versionar)
├── .gitignore         # Deve conter .env e credenciais.json
└── requirements.txt   # Dependências
```

3. Configuração de Segredos
Crie o arquivo .env na raiz do projeto e adicione suas variáveis:
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX
GCP_PROJECT_ID=seu-id-do-projeto-gcp
```

O arquivo credenciais.json deve ser baixado do console do Google Cloud (IAM > Contas de Serviço > Chaves) e salvo na raiz com esse nome exato.

3. Instalação de Dependências
No seu terminal dentro da pasta do projeto, execute:
``` Bash
pip install -r requirements.txt
```

5. Execução
Para rodar o monitoramento manualmente:
``` Bash
python main.py
```

# 📊 Estrutura de Notificação
O sistema utiliza attachments do Slack para exibir informações detalhadas, incluindo:

- Título: Indicador de urgência do prazo.
- Pedido: Identificador único.
- Dados do Produto: Nome, preço e quantidade.

# 🛡️ Segurança 
Nunca compartilhe seu arquivo credenciais.json ou seu .env.

Certifique-se de que o seu arquivo .gitignore contenha estas duas linhas para evitar vazamento de dados sensíveis no Git:

``` Plaintext
.env
credenciais.json
```

# 📈 Automação e Orquestração
Existem duas formas principais de colocar seu monitoramento em produção:

# 1. Serverless
Ideal para projetos leves, baixo custo e configuração rápida.

- Cloud Functions: Aloja o seu script main.py de forma isolada na nuvem.
- Cloud Scheduler: Atua como um despertador, disparando a execução da sua Cloud Function via HTTP em horários específicos como diariamente às 09:00.

# 2.  Apache Airflow 
Se o seu volume de dados crescer ou se você precisar criar dependências, só notificar o Slack se o BigQuery carregar os dados primeiro, a recomendação é usar o Cloud Composer o serviço gerenciado do Airflow no GCP. O Airflow transforma seu script em um DAG - Directed Acyclic Graph.

# Vantagens:

- Se a API do Slack falhar, o Airflow tenta novamente sozinho.
- Interface dedicada para ver logs e histórico de execução de cada tarefa.
-Facilita a criação de fluxos de trabalho complexos onde várias etapas se conectam.


## Notificação
Abaixo, é o print de como o alerta aparece no Slack:

<img width="958" height="478" alt="image" src="https://github.com/user-attachments/assets/a99a3a41-eed8-47a5-8b71-60333ccbf3f1" />


Abaixo visualizamos a dag, caso o processo seja automatizado:
<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/7696ebe9-d747-4b24-b6a6-9c8160c972dc" />


