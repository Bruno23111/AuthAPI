from fastapi import FastAPI
from .routes import router

app = FastAPI()
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API FastAPI + Firebase está no ar!"}