import json
import re
import faiss
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from prompt_builder import build_prompt
from gemini import generate_answer


def tokenize(text):
    return re.findall(r"\w+", text.lower())


def main():

    with open("indexes/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    index = faiss.read_index("indexes/faiss_index.bin")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    corpus = [tokenize(chunk["text"]) for chunk in chunks]

    bm25 = BM25Okapi(corpus)

    query = input("Enter your question: ")

    # ---------------- FAISS ----------------

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    _, faiss_indices = index.search(query_embedding, k=5)

    # ---------------- BM25 ----------------

    scores = bm25.get_scores(tokenize(query))

    bm25_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:5]

    # ---------------- Merge ----------------

    merged_indices = []

    for i in faiss_indices[0]:
        if i not in merged_indices:
            merged_indices.append(i)

    for i in bm25_indices:
        if i not in merged_indices:
            merged_indices.append(i)

    retrieved_chunks = []
    retrieved_metadata = []

    for i in merged_indices:

        retrieved_chunks.append(chunks[i]["text"])

        retrieved_metadata.append(
            {
                "paper_name": chunks[i]["paper_name"],
                "chunk_id": chunks[i]["chunk_id"]
            }
        )

    prompt = build_prompt(retrieved_chunks, query)

    answer = generate_answer(prompt)

    print("\nAnswer\n")
    print(answer)

    print("\nSources\n")

    seen = set()

    for source in retrieved_metadata:

        citation = f"{source['paper_name']} | Chunk {source['chunk_id']}"

        if citation not in seen:
            print(citation)
            seen.add(citation)


if __name__ == "__main__":
    main()