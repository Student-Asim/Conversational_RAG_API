from fastapi import FastAPI
from database.database import Base, engine
from routes import chat

# create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Conversational RAG API", version="1.0")

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
def root():
    return {"message": "Conversational RAG API is alive"}
