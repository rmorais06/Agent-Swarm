import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_init import get_llm_chain

# Importamos os outros agentes que vamos criar depois
from .knowledge_agent import knowledge_agent
from .support_agent import support_agent

# Configuração do modelo de linguagem
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
# ----- Estrutura do Roteamento -----
# O prompt que o roteador vai usar.
# Ele instrui o LLM a decidir qual agente é o mais adequado.
# Cada destino (destination) tem um nome e uma descrição.

router_prompt_template = """
Você é um agente roteador inteligente, responsável por direcionar mensagens de usuários para o agente especializado mais adequado.
Sua tarefa é analisar a mensagem do usuário e decidir para qual dos seguintes agentes ela deve ser encaminhada:

{destinations}

Qualquer pergunta que não se encaixe nas categorias acima deve ser direcionada para o agente de 'default'.

Siga o formato de saída do roteador, com 'destination' sendo o nome do agente e 'next_inputs' a mensagem original do usuário.
Não inclua nenhuma outra informação na sua resposta.

---
Mensagem do Usuário: {input}
"""

# As informações sobre cada agente de destino
destinations = [
    {
        "name": "knowledge_agent",
        "description": "Bom para responder perguntas sobre produtos, serviços, taxas, e informações públicas do site da InfinitePay. Use este agente para consultas que requerem a recuperação de informações e a geração de respostas com base em um conjunto de dados.",
        "agent": knowledge_agent
    },
    {
        "name": "support_agent",
        "description": "Bom para resolver problemas específicos do usuário, como 'não consigo fazer login', 'problemas com transferências', ou consultas que precisam de acesso a dados específicos do cliente (usando o user_id).",
        "agent": support_agent
    }
]

# A lógica do roteamento
router_chain = LLMRouterChain.from_llm(llm, destinations, router_prompt_template)
combined_chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains={d["name"]: d["agent"] for d in destinations},
    default_chain=get_llm_chain(llm, "Não consegui entender sua solicitação. Por favor, tente reformular a pergunta.")
)

def router_agent(user_message: str, user_id: str):
    """
    Função principal do agente roteador.
    Recebe a mensagem do usuário e a encaminha para o agente correto.
    """
    # Adiciona user_id ao input para que os agentes de destino possam usá-lo.
    full_input = {"input": user_message, "user_id": user_id}
    
    # A chain de LangChain lida com a execução e o roteamento.
    return combined_chain.run(full_input)