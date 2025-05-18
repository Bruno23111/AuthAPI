import os
import uvicorn
from fastapi import FastAPI
from .routes import router

app = FastAPI()
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API FastAPI + Firebase está no ar!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Pega a porta da variável PORT ou usa 8000 por padrão
    uvicorn.run("main:app", host="0.0.0.0", port=port)
