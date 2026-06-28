import os

from fastapi import FastAPI, UploadFile, File

from src.models import QueryRequest
from src.hybrid_search import search
from src.upload import index_single_pdf


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


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    save_path = os.path.join("data", file.filename)

    with open(save_path, "wb") as f:
        f.write(await file.read())

    index_single_pdf(file.filename)

    return {
        "message": "Document uploaded and indexed successfully",
        "filename": file.filename
    }