from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

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


print("Dimension:", dimension)
print("Vectors stored:", index.ntotal)


query = "What are the key features?"

query_embedding = model.encode([query])

query_embedding = np.array(query_embedding).astype("float32")


distances, indices = index.search(query_embedding, k=2)


print("\nMost Relevant Chunks\n")

for i in indices[0]:
    print(chunks[i])
    print("-" * 60)