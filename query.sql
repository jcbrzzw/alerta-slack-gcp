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
        LIMIT 3
    """