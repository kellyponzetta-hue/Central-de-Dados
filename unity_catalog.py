import sqlite3

class UnityCatalogGovernance:
    def __init__(self, db_path='database/central_dados.db'):
        self.db_path = db_path

    def mask_cpf(self, cpf):
        if not cpf or len(str(cpf)) < 11:
            return "***.***.***-**"
        cpf_str = str(cpf)
        return f"***.***.{cpf_str[-4:-2]}-{cpf_str[-2:]}"

    def get_gold_vendas_data(self, has_full_access=False):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id_venda, cliente_nome, cpf_cliente, valor_venda, vlr_desc_mkt, regiao FROM gold_vendas")
        rows = cursor.fetchall()
        conn.close()

        processed_rows = []
        for row in rows:
            id_venda, cliente, cpf, valor, desc, regiao = row
            
            # Se a flag de acesso for verdadeira, mostra o CPF real; caso contrário, mascara
            display_cpf = str(cpf) if has_full_access else self.mask_cpf(cpf)
            
            # Retorna como DICIONÁRIO para o JavaScript conseguir ler os nomes dos campos diretamente
            processed_rows.append({
                "id_venda": id_venda,
                "cliente_nome": cliente,
                "cpf_cliente": display_cpf,
                "valor_venda": valor,
                "vlr_desc_mkt": desc,
                "regiao": regiao
            })

        return {
            "access_granted": has_full_access,
            "data": processed_rows
        }