from fastapi import FastAPI

from src.models import QueryRequest
from src.hybrid_search import search


app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "Research RAG API is running"
    }


@app.post("/query")
def query(request: QueryRequest):

    answer, sources = search(request.question)

    return {
        "answer": answer,
        "sources": sources
    }