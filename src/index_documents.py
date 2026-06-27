import os
import faiss
import numpy as np
import json

from sentence_transformers import SentenceTransformer

from extract import extract_text
from chunk import create_chunks


text = extract_text("text1.pdf")

chunks = create_chunks(text)


model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

embeddings = np.array(embeddings).astype("float32")


dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


os.makedirs("indexes", exist_ok=True)

faiss.write_index(index, "indexes/faiss_index.bin")

with open("indexes/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print("Index saved successfully!")
print("Vectors:", index.ntotal)