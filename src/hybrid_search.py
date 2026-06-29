import json
import faiss
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder

from src.prompt_builder import build_prompt
from src.gemini import generate_answer


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


index = None
chunks = None
bm25 = None


def load_indexes():

    global index, chunks, bm25

    index = faiss.read_index("indexes/faiss_index.bin")

    with open(
        "indexes/chunks.json",
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    tokenized_chunks = []

    for chunk in chunks:

        tokenized_chunks.append(
            chunk["text"].lower().split()
        )

    bm25 = BM25Okapi(tokenized_chunks)


load_indexes()


def retrieve(query, selected_papers=[]):

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")
    
    filtered_indices = []

    if len(selected_papers) == 0:

        filtered_indices = list(range(len(chunks)))

    else:

        for i, chunk in enumerate(chunks):

            if chunk["paper_name"] in selected_papers:

                filtered_indices.append(i)

    k = min(20, index.ntotal)

    _, faiss_indices = index.search(query_embedding, k=k)

    bm25_scores = bm25.get_scores(
        query.lower().split()
    )

    bm25_indices = np.argsort(bm25_scores)[::-1][:5]

    merged_indices = []

    for i in faiss_indices[0]:

        if i not in filtered_indices:
            continue

        if i not in merged_indices:
            merged_indices.append(i)
            
    for i in bm25_indices:

        if i not in filtered_indices:
            continue

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

    unique_sources = []
    seen = set()

    for source in retrieved_metadata:

        key = (
            source["paper_name"],
            source["chunk_id"]
        )

        if key not in seen:

            seen.add(key)
            unique_sources.append(source)

    return retrieved_chunks, unique_sources


def search(query, selected_papers=[]):

    retrieved_chunks, retrieved_metadata = retrieve(
        query,
        selected_papers
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

    for source in sources:

        print(
            f"{source['paper_name']} | "
            f"Chunk {source['chunk_id']}"
        )