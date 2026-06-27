import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from extract import extract_text
from chunk import create_chunks


DATA_DIR = "data"
INDEX_DIR = "indexes"

all_chunks = []

paper_id = 1


for file in os.listdir(DATA_DIR):

    if not file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(DATA_DIR, file)

    print(f"Processing {file}")

    text = extract_text(pdf_path)

    chunks = create_chunks(text)

    for idx, chunk in enumerate(chunks):

        all_chunks.append(
            {
                "paper_id": paper_id,
                "paper_name": file,
                "chunk_id": idx + 1,
                "text": chunk,
            }
        )

    paper_id += 1


texts = [chunk["text"] for chunk in all_chunks]


model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")


dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


os.makedirs(INDEX_DIR, exist_ok=True)

faiss.write_index(index, os.path.join(INDEX_DIR, "faiss_index.bin"))

with open(
    os.path.join(INDEX_DIR, "chunks.json"),
    "w",
    encoding="utf-8",
) as f:

    json.dump(all_chunks, f, indent=4, ensure_ascii=False)


print("\nIndexing Complete")
print("Papers:", paper_id - 1)
print("Total Chunks:", len(all_chunks))
print("Vectors:", index.ntotal)