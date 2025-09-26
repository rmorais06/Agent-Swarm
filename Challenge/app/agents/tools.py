from langchain.tools import tool

@tool
def check_account_status(user_id: str) -> str:
    """
    Verifica o status da conta de um usuário. Útil para responder
    a perguntas sobre login ou problemas de acesso.
    O user_id é uma string que identifica o usuário.
    """

    if user_id == "client789":
        return f"O status da conta do usuário {user_id} é 'Ativa', mas há uma restrição de segurança pendente que impede o login."
    elif user_id == "user_no_history":
        return f"A conta do usuário {user_id} está 'Ativa' e sem restrições."
    else:
        return f"Não foi possível encontrar o usuário {user_id}."

@tool
def check_transaction_history(user_id: str) -> str:
    """
    Verifica o histórico de transações recentes para um usuário específico.
    Útil para responder a perguntas sobre transferências, pagamentos ou
    movimentações na conta. O user_id é uma string que identifica o usuário.
    """
    # Esta é uma simulação.
    if user_id == "client789":
        return f"Para o usuário {user_id}, a última tentativa de transferência foi rejeitada devido à restrição de segurança. Nenhuma outra atividade recente foi encontrada."
    elif user_id == "user_no_history":
        return f"O usuário {user_id} não tem transações recentes."
    else:
        return f"Não foi possível encontrar o histórico de transações para o usuário {user_id}."