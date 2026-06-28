# Research RAG Platform

A full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural language questions. The system retrieves the most relevant document chunks using Hybrid Search (Semantic Search + BM25), reranks them using a Cross-Encoder, and generates accurate answers using Google Gemini.

---

## Features

* Upload PDF documents dynamically
* Extract text from PDFs using PyMuPDF
* Fixed-size document chunking
* Generate sentence embeddings using Sentence Transformers
* Semantic retrieval using FAISS
* Keyword retrieval using BM25
* Hybrid retrieval (FAISS + BM25)
* Cross-Encoder reranking for improved retrieval quality
* Answer generation using Google Gemini 2.5 Flash
* Source citations with document name and chunk number
* REST API built with FastAPI
* React frontend for interacting with the system

---

## Tech Stack

### Backend

* Python
* FastAPI
* PyMuPDF
* FAISS
* Sentence Transformers
* Rank-BM25
* Cross Encoder (MS MARCO MiniLM)
* Google Gemini API

### Frontend

* React
* Vite
* Axios
* CSS

---

## Project Structure

```
research-rag-platform/

├── data/                 # PDF documents
├── frontend/             # React frontend
├── indexes/              # FAISS index + chunk metadata
├── output/               # Generated outputs
├── src/
│   ├── api.py
│   ├── chunk.py
│   ├── extract.py
│   ├── gemini.py
│   ├── hybrid_search.py
│   ├── index_documents.py
│   ├── models.py
│   ├── prompt_builder.py
│   ├── reranker.py
│   ├── upload.py
│   └── ...
│
├── requirements.txt
└── README.md
```

---

## Retrieval Pipeline

```
User Question
       │
       ▼
Sentence Embedding
       │
       ▼
FAISS Semantic Search
       │
       ├──────────────┐
       ▼              │
BM25 Keyword Search   │
       │              │
       └────Merge─────┘
             │
             ▼
Cross Encoder Reranker
             │
             ▼
Top Relevant Chunks
             │
             ▼
Prompt Builder
             │
             ▼
Google Gemini
             │
             ▼
Final Answer + Sources
```

---

## API Endpoints

### Query the RAG System

**POST**

```
/query
```

Request

```json
{
    "question": "What is a process?"
}
```

Response

```json
{
    "answer": "...",
    "sources": [
        {
            "paper_name": "OSN_L02.pdf",
            "chunk_id": 9
        }
    ]
}
```

---

### Upload a PDF

**POST**

```
/upload
```

Uploads a PDF, extracts text, generates embeddings, updates the FAISS index, refreshes the BM25 index, and immediately makes the document searchable.

---

## Frontend

The React frontend allows users to

* Upload PDFs
* Ask questions
* View generated answers
* View source citations

---

## Current Capabilities

* Multi-document retrieval
* Dynamic PDF uploads
* Hybrid Search
* Cross-Encoder reranking
* Source-aware answer generation
* REST API
* Interactive React frontend

---

## Future Improvements

* Chat history
* Conversation memory
* Streaming responses
* Metadata filtering
* PostgreSQL integration
* Docker support
* User authentication
* Deployment on cloud
* Advanced chunking strategies

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd research-rag-platform
```

### Backend

```bash
python -m venv venv

source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn src.api:app --reload
```

Backend

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

## Screenshots

(Add frontend screenshots here.)

---

## License

This project is for educational and research purposes.
