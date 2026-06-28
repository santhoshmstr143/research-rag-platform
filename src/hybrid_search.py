import json
import faiss
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder

from src.prompt_builder import build_prompt
from src.gemini import generate_answer


index = faiss.read_index("indexes/faiss_index.bin")

with open("indexes/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


tokenized_chunks = []

for chunk in chunks:
    tokenized_chunks.append(
        chunk["text"].lower().split()
    )

bm25 = BM25Okapi(tokenized_chunks)


def search(query):

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    _, faiss_indices = index.search(query_embedding, k=5)

    bm25_scores = bm25.get_scores(
        query.lower().split()
    )

    bm25_indices = np.argsort(bm25_scores)[::-1][:5]

    merged_indices = []

    for i in faiss_indices[0]:

        if i not in merged_indices:
            merged_indices.append(i)

    for i in bm25_indices:

        if i not in merged_indices:
            merged_indices.append(i)

    pairs = []

    for i in merged_indices:

        pairs.append(
            (
                query,
                chunks[i]["text"]
            )
        )

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(scores, merged_indices),
        reverse=True
    )

    retrieved_chunks = []
    retrieved_metadata = []

    for _, idx in ranked[:3]:

        retrieved_chunks.append(
            chunks[idx]["text"]
        )

        retrieved_metadata.append(
            {
                "paper_name": chunks[idx]["paper_name"],
                "chunk_id": chunks[idx]["chunk_id"]
            }
        )

    prompt = build_prompt(
        retrieved_chunks,
        query
    )

    answer = generate_answer(prompt)

    return answer, retrieved_metadata


if __name__ == "__main__":

    query = input("Enter your question: ")

    answer, sources = search(query)

    print("\nAnswer\n")
    print(answer)

    print("\nSources\n")

    seen = set()

    for source in sources:

        citation = (
            f"{source['paper_name']} | "
            f"Chunk {source['chunk_id']}"
        )

        if citation not in seen:
            print(citation)
            seen.add(citation)