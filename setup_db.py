import sqlite3
import os

def init_database():
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect('database/central_dados.db')
    cursor = conn.cursor()

    # 1. REMOVE TABELAS ANTIGAS PARA EVITAR CONFLITO DE COLUNAS
    cursor.execute('DROP TABLE IF EXISTS table_metadata')
    cursor.execute('DROP TABLE IF EXISTS catalog_metadata')
    cursor.execute('DROP TABLE IF EXISTS raw_tb_vnt_s3')
    cursor.execute('DROP TABLE IF EXISTS gold_vendas')
    cursor.execute('DROP TABLE IF EXISTS glossary')  # <-- ADICIONADO!

    # 2. CRIA AS TABELAS COM A ESTRUTURA CORRETA
    cursor.execute('''
        CREATE TABLE table_metadata (
            tabela TEXT PRIMARY KEY,
            owner_dominio TEXT,
            status_governanca TEXT,
            descricao TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE catalog_metadata (
            tabela TEXT,
            coluna TEXT,
            descricao_coluna TEXT,
            tag_seguranca TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE raw_tb_vnt_s3 (
            c1 TEXT, 
            c2 REAL, 
            c3 REAL, 
            dt TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE gold_vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_nome TEXT,
            cpf_cliente TEXT,
            valor_venda REAL,
            vlr_desc_mkt REAL,
            regiao TEXT
        )
    ''')

    # Nova tabela para o Glossário de Negócio!
    cursor.execute('''
        CREATE TABLE glossary (
            termo TEXT PRIMARY KEY,
            definicao TEXT,
            status TEXT
        )
    ''')

    # 3. POPULA OS DADOS
    cursor.execute('INSERT INTO table_metadata VALUES (?, ?, ?, ?)', 
        ('gold_vendas', 'Domínio de Varejo & Vendas (Data Owner)', 'REQUER_VALIDACAO_HUMANA', 'Tabela Gold de Pedidos Consolidados de E-commerce e Lojas Físicas.'))

    cursor.executemany('INSERT INTO catalog_metadata VALUES (?, ?, ?, ?)', [
        ('gold_vendas', 'cpf_cliente', 'CPF do cliente final para identificação no PDV', 'PII.CPF'),
        ('gold_vendas', 'vlr_desc_mkt', 'Desconto concedido em campanhas de Varejo', 'CONFIDENCIAL'),
        ('gold_vendas', 'valor_venda', 'Valor total pago na transação', 'PUBLICO')
    ])

    cursor.executemany('INSERT INTO raw_tb_vnt_s3 VALUES (?, ?, ?, ?)', [
        ('12345678901', 250.50, 15.00, '2026-08-10'),
        ('98765432100', 1200.00, 100.00, '2026-08-11')
    ])

    cursor.executemany('INSERT INTO gold_vendas VALUES (NULL, ?, ?, ?, ?, ?)', [
        ('Ana Silva', '12345678901', 250.50, 15.00, 'SP - Sudeste'),
        ('Carlos Eduardo', '98765432100', 1200.00, 100.00, 'RJ - Sudeste'),
        ('Fernanda Lima', '45678912344', 89.90, 0.00, 'PR - Sul')
    ])

    # Popula o Glossário!
    cursor.executemany('INSERT INTO glossary VALUES (?, ?, ?)', [
        ('Ticket Médio', 'Soma total de vendas dividida pela quantidade total de pedidos.', 'APROVADO'),
        ('PII (Dado Pessoal)', 'Informação Pessoal Identificável sujeita à regulamentação da LGPD.', 'REGULADO'),
        ('Churn de Clientes', 'Métrica que indica a taxa de cancelamento ou inatividade de usuários.', 'REVISÃO')
    ])

    conn.commit()
    conn.close()
    print("✅ Banco de dados recriado com Sucesso (Glossário e Gold inclusos)!")

if __name__ == '__main__':
    init_database()