import os
import requests
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

# Carrega apenas o Webhook e o Project ID do .env
load_dotenv()
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
project_id = os.environ.get("GCP_PROJECT_ID")

def verificar_alertas_vendas():
    caminho_credenciais = "credenciais.json"

    credentials = service_account.Credentials.from_service_account_file(caminho_credenciais)
    client = bigquery.Client(credentials=credentials, project=project_id)

    try:
        dataset_ref = client.dataset("Vendas")
        dataset = client.get_dataset(dataset_ref)
        localizacao = dataset.location
        print(f"📍 Dataset 'Vendas' encontrado na região: {localizacao}")
    except Exception as e:
        print(f"❌ Erro ao localizar o dataset 'Vendas': {str(e)}")
        return

    query = f"""
        SELECT 
          i.order_id,
          p.name AS produto_nome,
          p.price AS preco_produto,
          i.quantity AS quantidade,
          DATE_DIFF(CURRENT_DATE(), DATE(o.created_at), DAY) AS dias_decorridos
        FROM `{project_id}.Vendas.Items` i
        INNER JOIN `{project_id}.Vendas.Produto` p ON i.product_id = p.id
        INNER JOIN `{project_id}.Vendas.Ordens` o ON i.order_id = o.id
        WHERE DATE_DIFF(CURRENT_DATE(), DATE(o.created_at), DAY) >= 0
        LIMIT 1
    """

    print("🔍 Executando query na região correta...")
    try:
        query_job = client.query(query, location=localizacao)
        resultados = query_job.result()
        
        alertas_enviados = 0
        for linha in resultados:
            print(f"DEBUG: Processando pedido {linha.order_id}...")
            try:
                enviar_alerta_slack(
                    produto=linha.produto_nome,
                    pedido=linha.order_id,
                    dias=linha.dias_decorridos,
                    preco=str(linha.preco_produto),
                    qtd=str(linha.quantidade)
                )
                alertas_enviados += 1
            except Exception as e:
                print(f"❌ Erro ao chamar a função Slack para o pedido {linha.order_id}: {e}")
        
        print(f"\n🎉 Processo concluído! {alertas_enviados} alertas processados.")

    except Exception as e:
        print(f"\n❌ Erro durante a execução da query: {str(e)}")


def enviar_alerta_slack(produto, pedido, dias, preco, qtd):
    payload = {
        "attachments": [{
            "color": "#36a64f",
            "title": f"📊 Relatório de Pedidos: {dias} dias",
            "text": f"O produto *{produto}* está travado.",
            "fields": [
                {"title": "Pedido", "value": f"#{pedido}", "short": True},
                {"title": "Preço", "value": f"R$ {preco}", "short": True},
                {"title": "Qtd", "value": qtd, "short": True}
            ]
        }]
    }
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        print(f"DEBUG: Slack respondeu com código {response.status_code}")
        if response.status_code != 200:
            print(f"⚠️ Erro detalhado do Slack: {response.text}")
    except Exception as e:
        print(f"⚠️ Erro de conexão com o Slack: {e}")

if __name__ == "__main__":
    verificar_alertas_vendas()