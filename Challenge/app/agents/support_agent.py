import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory

# Importa as ferramentas
from .tools import check_account_status, check_transaction_history

# Configuração do modelo de linguagem
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))

# Converte as funções de ferramentas em objetos Tool que o LangChain pode usar
tools = [
    Tool(
        name="check_account_status",
        func=check_account_status,
        description="Verifica o status da conta de um usuário. Use para perguntas sobre login, acesso ou status da conta."
    ),
    Tool(
        name="check_transaction_history",
        func=check_transaction_history,
        description="Verifica o histórico de transações de um usuário. Use para perguntas sobre transferências, pagamentos ou outras atividades financeiras."
    )
]

# Inicializa o agente
support_agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True, # Define como True para ver o raciocínio do agente
    max_iterations=3,
    handle_parsing_errors=True
)

def support_agent(full_input: dict):
    """
    Função principal do agente de suporte.
    Recebe a mensagem e o user_id e passa para o executor do agente.
    """
    user_message = full_input.get("input")
    user_id = full_input.get("user_id")

    # O agente usa o 'user_id' do input para decidir qual ferramenta e com qual argumento chamar.
    prompt = f"O usuário com ID {user_id} diz: '{user_message}'"
    response = support_agent_executor.run(prompt)
    
    return response