import os
import json

from fastapi import FastAPI, UploadFile, File

from src.models import QueryRequest
from src.hybrid_search import search
from src.upload import index_single_pdf
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse
from src.gemini import stream_answer
from src.prompt_builder import build_prompt
from src.hybrid_search import retrieve


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

        answer, sources = search(
            request.question,
            request.papers
        )

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        return {
            "answer": str(e),
            "sources": []
        }


@app.post("/query/stream")
def query_stream(request: QueryRequest):

    retrieved_chunks, sources = retrieve(
        request.question,
        request.papers
    )

    prompt = build_prompt(
        retrieved_chunks,
        request.question
    )

    def event_stream():

        for token in stream_answer(prompt):

            yield json.dumps(
                {
                    "type": "token",
                    "content": token
                }
            ) + "\n"

        yield json.dumps(
            {
                "type": "sources",
                "content": sources
            }
        ) + "\n"

    return StreamingResponse(
        event_stream(),
        media_type="application/x-ndjson"
    )


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
    
@app.get("/papers")
def get_papers():

    with open(
        "indexes/chunks.json",
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    papers = []

    seen = set()

    for chunk in chunks:

        if chunk["paper_name"] not in seen:

            papers.append(chunk["paper_name"])

            seen.add(chunk["paper_name"])

    return papers