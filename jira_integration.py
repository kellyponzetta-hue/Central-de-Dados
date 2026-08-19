class JiraIntegrationAPI:
    def __init__(self):
        # Mapeamento inicial de usuários e seus grupos de acesso no Unity Catalog
        self.user_permissions = {
            "usuario.varejo@empresa.com": ["grp_varejo_leitura_basica"]
        }

    def get_user_groups(self, user_email):
        return self.user_permissions.get(user_email, [])

    def process_webhook_approval(self, ticket_id, user_email, group_to_add):
        """
        Simula o Webhook do Jira sendo disparado quando o ticket é aprovado.
        Adiciona o usuário ao grupo restrito do Unity Catalog.
        """
        if user_email not in self.user_permissions:
            self.user_permissions[user_email] = []

        if group_to_add not in self.user_permissions[user_email]:
            self.user_permissions[user_email].append(group_to_add)

        print(f"✅ Webhook Jira [{ticket_id}]: Usuário {user_email} adicionado ao grupo {group_to_add}")
        return True