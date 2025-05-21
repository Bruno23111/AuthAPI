import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from fastapi.responses import JSONResponse

# aqui [e criada a instancia da API. Todas as configurações são feitas a partir desse objeto app
app = FastAPI()

# define quais são os dominios que podem fazer requisições nessa API
origins = [
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# adicona o middleware Cors a aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,     
    allow_methods=["*"],
    allow_headers=["*"],
)

# incluindo o roteador definido no arquivo routes.py
app.include_router(router, prefix="/api")

# define uma rota para o caminho raiz e retorna um json
@app.get("/")
def root():
    return {"message": "API FastAPI + Firebase está no ar!"}

# esta condição permite que o script seja executado executado diretamente via python main.py
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Pega a porta da variável PORT ou usa 8000 por padrão
    uvicorn.run("main:app", host="0.0.0.0", port=port)
