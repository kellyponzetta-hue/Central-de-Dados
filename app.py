from flask import Flask, render_template, jsonify, request
import sqlite3
import os

from setup_db import init_database
from ai_classifier import DatabricksAIEngine
from unity_catalog import UnityCatalogGovernance
from jira_integration import JiraIntegrationAPI
from lineage_engine import DataLineageEngine

app = Flask(__name__)

# Garante a inicialização das tabelas SQLite
init_database()

ai_engine = DatabricksAIEngine()
unity_catalog = UnityCatalogGovernance()
jira_api = JiraIntegrationAPI()
lineage_engine = DataLineageEngine()

# Dados do Usuário Logado (Integrado ao SSO / Entra ID / AD)
CURRENT_USER = {
    "nome": "Carlos Silva",
    "email": "carlos.silva@empresa.com",
    "cargo": "Analista de Negócios Varejo",
    "grupo_ad": "grp_varejo_analytics_std"
}

# Controle dos Estados de Permissão no Unity Catalog (Simulação)
# Estado Inicial: RAW (Sem acesso), GOLD (Acesso Leitura com Mascaramento)
PERMISSIONS_STATE = {
    "landing_zone.raw_tb_vnt_s3": {
        "access_level": "NO_ACCESS", # NO_ACCESS | FULL_ACCESS
        "status_label": "🔴 Sem Acesso (Access Denied)"
    },
    "gold_comercial.gold_vendas": {
        "access_level": "RESTRICTED", # RESTRICTED (PII Masked) | FULL_ACCESS
        "status_label": "🟡 Leitura Restrita (CPF Mascarado)"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

# ROTA DO USUÁRIO LOGADO
@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    return jsonify(CURRENT_USER)

# ABA 1: Dados Brutos (Data Swamp / Cenário do Caos)
@app.route('/api/raw-data', methods=['GET'])
def get_raw_data():
    try:
        # A Aba 1 SEMPRE exibe os dados brutos sem bloquear, 
        # para que você possa mostrar o contraste da bagunça inicial (c1, c2, c3).
        conn = sqlite3.connect('database/central_dados.db')
        cursor = conn.cursor()
        cursor.execute("SELECT c1, c2, c3, dt FROM raw_tb_vnt_s3")
        rows = cursor.fetchall()
        conn.close()
        return jsonify({"status": "SUCCESS", "rows": rows})
    except Exception as e:
        return jsonify({"status": "ERROR", "rows": []})

# ABA 2: Catálogo & Glossário
@app.route('/api/catalog', methods=['GET'])
def get_catalog():
    try:
        return jsonify(ai_engine.scan_and_catalog())
    except Exception as e:
        return jsonify({"table_info": {}, "columns": [], "glossary": []})

@app.route('/api/search', methods=['GET'])
def search_catalog():
    try:
        query = request.args.get('q', '').lower()
        conn = sqlite3.connect('database/central_dados.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tabela, coluna, descricao_coluna, tag_seguranca 
            FROM catalog_metadata 
            WHERE LOWER(tabela) LIKE ? OR LOWER(coluna) LIKE ? OR LOWER(descricao_coluna) LIKE ?
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        results = cursor.fetchall()
        conn.close()
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"results": []})

# ABA 3: Linhagem
@app.route('/api/lineage-complex', methods=['GET'])
def get_lineage_complex():
    try:
        return jsonify(lineage_engine.get_complex_lineage())
    except Exception as e:
        return jsonify({})

# ABA 4: Lista de Tabelas do Catalog e Permissões
@app.route('/api/catalog-permissions', methods=['GET'])
def get_catalog_permissions():
    return jsonify(PERMISSIONS_STATE)

# ABA 4: Preview da Tabela Gold
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        is_full = PERMISSIONS_STATE["gold_comercial.gold_vendas"]["access_level"] == "FULL_ACCESS"
        result = unity_catalog.get_gold_vendas_data(has_full_access=is_full)
        return jsonify(result)
    except Exception as e:
        return jsonify({"access_granted": False, "data": []})

# APROVAÇÃO JIRA (ELEVAÇÃO DE ACESSO)
@app.route('/api/jira/approve', methods=['POST'])
def approve_jira_ticket():
    try:
        target = request.json.get('target', 'gold')
        
        if target == 'raw':
            PERMISSIONS_STATE["landing_zone.raw_tb_vnt_s3"]["access_level"] = "FULL_ACCESS"
            PERMISSIONS_STATE["landing_zone.raw_tb_vnt_s3"]["status_label"] = "🟢 Acesso de Leitura Concedido"
        else:
            PERMISSIONS_STATE["gold_comercial.gold_vendas"]["access_level"] = "FULL_ACCESS"
            PERMISSIONS_STATE["gold_comercial.gold_vendas"]["status_label"] = "🟢 Acesso Total (PII Desmascarado)"
            
        print(f"⚡ Policy Jira Executada: Acesso liberado no Unity Catalog para {target}")
        return jsonify({"status": "SUCCESS", "message": "Acesso concedido com sucesso via Política Automática do Jira!"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)})
@app.route('/api/glossary', methods=['GET'])
def get_glossary():
    try:
        conn = sqlite3.connect('database/central_dados.db')
        cursor = conn.cursor()
        cursor.execute("SELECT termo, definicao, status FROM glossary")
        rows = cursor.fetchall()
        conn.close()
        
        # Mapeia para o formato que o front-end espera
        glossary_items = [
            {"termo": r[0], "definicao": r[1], "status": r[2]} 
            for r in rows
        ]
        return jsonify(glossary_items)
    except Exception as e:
        print(f"Erro ao buscar glossário: {e}")
        return jsonify([])
# RESET DA SIMULAÇÃO
@app.route('/api/jira/reset', methods=['POST'])
def reset_jira_ticket():
    try:
        PERMISSIONS_STATE["landing_zone.raw_tb_vnt_s3"]["access_level"] = "NO_ACCESS"
        PERMISSIONS_STATE["landing_zone.raw_tb_vnt_s3"]["status_label"] = "🔴 Sem Acesso (Access Denied)"
        PERMISSIONS_STATE["gold_comercial.gold_vendas"]["access_level"] = "RESTRICTED"
        PERMISSIONS_STATE["gold_comercial.gold_vendas"]["status_label"] = "🟡 Leitura Restrita (CPF Mascarado)"
        
        print("🔄 Simulação Resetada: Permissões voltaram ao padrão do perfil AD.")
        return jsonify({"status": "SUCCESS", "message": "Acessos resetados para o perfil padrão!"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)