import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

# URLs para a base de conhecimento
urls = [
    "https://www.infinitepay.io",
    "https://www.infinitepay.io/maquininha",
    "https://www.infinitepay.io/maquininha-celular",
    "https://www.infinitepay.io/tap-to-pay",
    "https://www.infinitepay.io/pdv",
    "https://www.infinitepay.io/receba-na-hora",
    "https://www.infinitepay.io/gestao-de-cobranca-2",
    "https://www.infinitepay.io/gestao-de-cobranca",
    "https://www.infinitepay.io/link-de-pagamento",
    "https://www.infinitepay.io/loja-online",
    "https://www.infinitepay.io/boleto",
    "https://www.infinitepay.io/conta-digital",
    "https://www.infinitepay.io/conta-pj",
    "https://www.infinitepay.io/pix",
    "https://www.infinitepay.io/pix-parcelado",
    "https://www.infinitepay.io/emprestimo",
    "https://www.infinitepay.io/cartao",
    "https://www.infinitepay.io/rendimento",
]

# Configurações do LLM e do modelo de embedding
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-002", google_api_key=os.getenv("GOOGLE_API_KEY"))

# ----------------- Construção do Pipeline RAG -----------------
def create_knowledge_base():
    """
    Função que carrega, divide, e armazena os dados da base de conhecimento.
    Esta função deve ser executada apenas uma vez (e.g., na inicialização).
    """
    # 1. Carregar os dados das URLs
    print("Carregando documentos...")
    loader = WebBaseLoader(urls)
    documents = loader.load()

    # 2. Dividir os documentos em pedaços (chunks)
    print("Dividindo documentos...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    # 3. Criar e armazenar os embeddings em um vector store
    print("Criando e armazenando embeddings...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    return vectorstore

# Cria a base de conhecimento (pode levar um tempo)
vectorstore = create_knowledge_base()

# Cria a cadeia de RAG
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# ----------------- Função do Agente do Conhecimento -----------------
def knowledge_agent(full_input: dict):
    """
    Função principal do agente de conhecimento.
    Recebe o input e o processa usando a cadeia de RAG.
    """
    user_message = full_input.get("input")
    response = qa_chain.run(user_message)
    return response