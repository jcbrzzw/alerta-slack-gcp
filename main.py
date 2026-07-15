import functions_framework
from google.cloud import bigquery
import requests
import os

# Pega o webhook de forma segura usando variáveis de ambiente no GCP
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "SUA_URL_PADRAO_DO_WEBHOOK_AQUI")

@functions_framework.http
def verificar_alertas_vendas(request):
    client = bigquery.Client()

    # Query direcionada para o dataset 'Vendas'
    query = """
        SELECT 
          i.order_id,
          p.name AS produto_nome,
          DATE_DIFF(CURRENT_DATE(), DATE(o.order_date), DAY) AS dias_decorridos
        FROM `seu_projeto_gcp.Vendas.items` i
        INNER JOIN `seu_projeto_gcp.Vendas.produto` p ON i.product_id = p.id
        INNER JOIN `seu_projeto_gcp.Vendas.orders` o ON i.order_id = o.id
        WHERE DATE_DIFF(CURRENT_DATE(), DATE(o.order_date), DAY) IN (120, 130, 140)
    """

    try:
        query_job = client.query(query)
        results = query_job.result()
        
        alertas_enviados = 0
        for row in results:
            enviar_alerta_slack(
                produto=row.produto_nome,
                pedido=row.order_id,
                dias=row.dias_decorridos
            )
            alertas_enviados += 1
            
        return f"Processamento concluido. {alertas_enviados} alertas enviados.", 200

    except Exception as e:
        print(f"Erro na execucao: {str(e)}")
        return f"Erro: {str(e)}", 500

def enviar_alerta_slack(produto, pedido, dias):
    if dias == 120:
        cor = "#FFCC00"  # Amarelo
    elif dias == 130:
        cor = "#FF9900"  # Laranja
    else:
        cor = "#FF0000"  # Vermelho (140 dias)

    payload = {
        "attachments": [
            {
                "color": cor,
                "title": f"🚨 Alerta {dias} dias: Corrigir Catálogo",
                "text": f"O produto *{produto}* (Pedido #{pedido}) necessita de ajuste.",
                "fields": [
                    {"title": "Dias decorridos", "value": f"{dias} dias", "short": True},
                    {"title": "Origem", "value": "Dataset Vendas (GCP)", "short": True}
                ],
                "footer": "GCP Cloud Functions & Slack Bot"
            }
        ]
    }
    
    requests.post(SLACK_WEBHOOK_URL, json=payload)