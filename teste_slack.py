import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def enviar_teste():
    # Mensagem de teste estruturada
    payload = {
        "attachments": [
            {
                "color": "#36a64f",  
                "title": "✅ Teste de Integração: GCP -> Slack",
                "text": "Se ler esta mensagem, a do Webhook está funcionando perfeitamente!",
                "footer": "Teste Local em Python"
            }
        ]
    }
    
    print("A enviar mensagem para o Slack...")
    resposta = requests.post(SLACK_WEBHOOK_URL, json=payload)
    
    if resposta.status_code == 200:
        print("Sucesso! Verifique o seu canal do Slack.")
    else:
        print(f"Erro ao enviar. Código de status: {resposta.status_code}")
        print(f"Resposta do Slack: {resposta.text}")

# Executa o teste
if __name__ == "__main__":
    enviar_teste()