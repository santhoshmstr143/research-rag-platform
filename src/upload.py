import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from src.extract import extract_text
from src.chunk import create_chunks


INDEX_DIR = "indexes"
model = SentenceTransformer("all-MiniLM-L6-v2")


def index_single_pdf(filename):

    text = extract_text(filename)

    chunks = create_chunks(text)

    with open(
        os.path.join(INDEX_DIR, "chunks.json"),
        "r",
        encoding="utf-8"
    ) as f:

        all_chunks = json.load(f)


    if len(all_chunks) == 0:
        paper_id = 1
    else:
        paper_id = max(chunk["paper_id"] for chunk in all_chunks) + 1



    new_vectors = model.encode(chunks)

    for idx, chunk in enumerate(chunks):

        all_chunks.append(
            {
                "paper_id": paper_id,
                "paper_name": filename,
                "chunk_id": idx + 1,
                "text": chunk,
            }
        )

    new_vectors = np.array(new_vectors).astype("float32")


    index = faiss.read_index(
        os.path.join(INDEX_DIR, "faiss_index.bin")
    )

    index.add(new_vectors)

    faiss.write_index(
        index,
        os.path.join(INDEX_DIR, "faiss_index.bin")
    )


    with open(
        os.path.join(INDEX_DIR, "chunks.json"),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_chunks,
            f,
            indent=4,
            ensure_ascii=False,
        )

    from src.hybrid_search import load_indexes
    load_indexes()

    print("Added", filename)
    print("New vectors:", len(new_vectors))