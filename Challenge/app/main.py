from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from typing import Dict
import os

# Importa o modelo
from .models.request_models import UserMessage

# Importa a lógica do agente roteador
from .agents.router_agent import router_agent

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

@app.post("/process_message", response_model=Dict)
async def process_user_message(data: UserMessage):
    """
    Endpoint para processar mensagens do usuário através do enxame de agentes.
    """
    try:
        # A lógica para passar a mensagem para o agente roteador
        # e obter a resposta final
        response = router_agent(data.message, data.user_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)