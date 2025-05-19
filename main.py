import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI()

# Configure as origens que vão acessar sua API - substitua com as URLs corretas do seu frontend
origins = [
    "http://localhost:3000",  # Exemplo localhost React
    "http://localhost:5500",  # Exemplo localhost para outro frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Ou ["*"] para teste, mas não recomendado em produção
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API FastAPI + Firebase está no ar!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Pega a porta da variável PORT ou usa 8000 por padrão
    uvicorn.run("main:app", host="0.0.0.0", port=port)
