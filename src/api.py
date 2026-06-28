import os

from fastapi import FastAPI, UploadFile, File

from src.models import QueryRequest
from src.hybrid_search import search
from src.upload import index_single_pdf
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "Research RAG API is running"
    }


@app.post("/query")
def query(request: QueryRequest):

    try:

        answer, sources = search(request.question)

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        return {
            "answer": str(e),
            "sources": []
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