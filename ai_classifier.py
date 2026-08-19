import sqlite3

class DatabricksAIEngine:
    def __init__(self, db_path='database/central_dados.db'):
        self.db_path = db_path

    def scan_and_catalog(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Metadados Gerais da Tabela (Pertencente ao Domínio de Varejo)
        cursor.execute("SELECT tabela, owner_dominio FROM table_metadata WHERE tabela='gold_vendas'")
        table_info = cursor.fetchone()

        # 2. Mapeamento de Colunas + Identificação de Lacunas/Pontos Cegos da IA
        column_catalog = [
            {
                "coluna": "id_venda",
                "descricao": "Identificador único da transação de venda.",
                "tag": "PUBLICO",
                "status_ia": "AUTOMATICO",
                "nota": "IA identificou como Chave Primária."
            },
            {
                "coluna": "cpf_cliente",
                "descricao": "Número do CPF do comprador para identificação no PDV.",
                "tag": "PII.CPF (Sensível)",
                "status_ia": "AUTOMATICO",
                "nota": "IA detectou padrão PII com 99% de confiança."
            },
            {
                "coluna": "vlr_desc_mkt",
                "descricao": "⚠️ [PENDENTE] Descrição ausente / Incompleta",
                "tag": "CONFIDENCIAL",
                "status_ia": "REQUER_AJUSTE_OWNER",
                "nota": "⚠️ Ponto Cego da IA: Coluna abreviada. Requer que o Data Owner defina a regra de negócio do desconto."
            },
            {
                "coluna": "regiao",
                "descricao": "Região geográfica da filial onde o pedido foi faturado.",
                "tag": "PUBLICO",
                "status_ia": "AUTOMATICO",
                "nota": "IA categorizou com base nos valores (ex: SP, RJ, PR)."
            }
        ]

        # 3. Sugestões para o Glossário de Negócio
        glossary_suggestions = [
            {
                "termo": "Valor Líquido de Vendas",
                "definicao": "Receita bruta deduzida de impostos e cupons promocionais.",
                "status": "Sugerido por IA (Aguardando Aprovação)"
            },
            {
                "termo": "Cliente Ativo PII",
                "definicao": "Consumidor cadastrado no programa de fidelidade com CPF validado.",
                "status": "Aprovado pelo Data Owner"
            }
        ]

        conn.close()
        
        return {
            "table_info": {
                "tabela": table_info[0] if table_info else "gold_vendas",
                "owner_dominio": table_info[1] if table_info else "Domínio de Varejo & Vendas"
            },
            "columns": column_catalog,
            "glossary": glossary_suggestions
        }