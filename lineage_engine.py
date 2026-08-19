class DataLineageEngine:
    def __init__(self):
        pass

    def get_complex_lineage(self):
        return {
            "sources": [
                {"id": "s3_pdv", "label": "S3 Raw: PDV Lojas", "type": "JSON", "cols": 18, "rows": "1.2M", "owner": "Time Ingestão"},
                {"id": "s3_ecom", "label": "S3 Raw: E-commerce", "type": "CSV", "cols": 24, "rows": "3.5M", "owner": "Time Ingestão"},
                {"id": "s3_erp", "label": "S3 Raw: ERP SAP", "type": "Parquet", "cols": 42, "rows": "800k", "owner": "Time Ingestão"}
            ],
            "transformations": [
                {"id": "silver_vendas", "label": "Silver: tb_vendas_limpas", "type": "Delta Lake", "cols": 30, "rows": "5.0M", "owner": "Engenharia de Dados"}
            ],
            "gold": [
                {"id": "gold_vendas", "label": "Gold: fato_pedidos_vendas", "type": "Unity Catalog", "cols": 12, "rows": "5.0M", "owner": "Domínio de Varejo & Vendas"}
            ],
            "destinations": [
                {"id": "dest_pbi", "label": "Power BI: Dashboard Diretoria", "type": "Report", "cols": 8, "users": 45},
                {"id": "dest_ml", "label": "Modelos IA: Churn & LTV", "type": "Databricks ML", "cols": 10, "users": 12},
                {"id": "dest_sql", "label": "Ad-Hoc SQL Analytics", "type": "SQL Warehouse", "cols": 12, "users": 120}
            ]
        }