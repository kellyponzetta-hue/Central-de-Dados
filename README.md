# 🛡️ Central de Dados & Governança de IA (Unity Catalog Sim)

Uma plataforma moderna de **Governança de Dados e Linhagem** que simula a integração entre **Databricks Unity Catalog**, **Políticas de Acesso (PII/LGPD)**, **Integração Jira** e **Classificação via Inteligência Artificial**.

---

## 📌 Visão Geral do Projeto

Este projeto foi desenvolvido para demonstrar o controle de ciclo de vida do dado, desde a sua ingestão bruta (*Camada Raw/Data Swamp*) até a sua disponibilização curada (*Camada Gold*), aplicando regras rígidas de segurança, privacidade e controle de acesso em conformidade com a LGPD.

### 💡 Principais Funcionalidades

* **📂 Camada Raw (Data Swamp):** Exibição dos dados brutos consumidos diretamente de fontes não estruturadas (ex: S3/Landing Zone).
* **✨ Camada Gold (Data Lakehouse):** Dados validados e estruturados prontos para consumo de negócios.
* **🔒 Governança de PII (Unity Catalog):** Mascaramento dinâmico de dados sensíveis (ex: CPF) com base nas permissões do perfil do usuário do Active Directory (AD).
* **🎫 Elevação de Acesso via Jira:** Simulação de solicitação e aprovação automática de permissões com auditoria em tempo real.
* **🤖 AI Classifier Engine:** Classificação inteligente de dados e geração de catálogos e metadados.
* **🕸️ Engine de Linhagem (Data Lineage):** Mapeamento do caminho percorrido pelos dados desde a origem até o consumo final.
* **📖 Glossário de Negócios:** Centralização de termos técnicos e definições regulatórias.

---

## 🏗️ Arquitetura e Tecnologias Utilizadas

* **Backend:** Python 3 (Flask)
* **Banco de Dados:** SQLite 3 (Armazenamento local dinâmico)
* **Frontend:** HTML5, CSS3 moderno e JavaScript puro (ES6 Async/Fetch API)
* **Integrações Simuladas:** Databricks Unity Catalog, Jira API, Entra ID / SSO

---

## 📁 Estrutura de Pastas

```text
Central de Dados/
├── database/
│   └── central_dados.db        # Banco de dados SQLite gerado pelo setup
├── templates/
│   └── index.html              # Interface web principal
├── ai_classifier.py            # Motor de IA para classificação e metadados
├── app.py                      # Servidor Web / Rotas da API Flask
├── jira_integration.py         # Integração e automação de chamados Jira
├── lineage_engine.py           # Engine para mapeamento de linhagem dos dados
├── setup_db.py                 # Script de criação e população inicial do SQLite
├── unity_catalog.py            # Controle de governança e mascaramento de PII
└── README.md                   # Documentação do projeto
