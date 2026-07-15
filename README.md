# Alerta Slack GCP

## Descrição
Este projeto automatiza o monitoramento de datasets no Google BigQuery. Ele verifica alterações e envia alertas em tempo real para o canal no Slack, garantindo que a equipe seja notificada imediatamente.

## Funcionalidades
- [ ] Monitoramento agendado do Google BigQuery.
- [ ] Integração nativa com Webhooks do Slack.
- [ ] Tratamento de erros e logs de execução.

## Tecnologias Utilizadas
- **Python**: Linguagem principal.
- **Google Cloud BigQuery API**: Para consulta aos dados.
- **Slack API**: Para o envio das notificações.

## Como configurar
1. Clone o repositório.
2. Crie um arquivo `.env` com suas credenciais:
   - `SLACK_WEBHOOK_URL=seu_link_aqui`
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute: `python main.py`

## Notificação
Abaixo, é o print de como o alerta aparece no Slack:

![Notificação Slack](notificacao_slack1.png)
