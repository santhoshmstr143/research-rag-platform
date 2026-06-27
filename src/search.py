import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from prompt_builder import build_prompt
from gemini import generate_answer


index = faiss.read_index("indexes/faiss_index.bin")


with open("indexes/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


model = SentenceTransformer("all-MiniLM-L6-v2")


query = input("Enter your question: ")


query_embedding = model.encode([query])

query_embedding = np.array(query_embedding).astype("float32")


distances, indices = index.search(query_embedding, k=2)


retrieved_chunks = []

for i in indices[0]:
    retrieved_chunks.append(chunks[i])


prompt = build_prompt(retrieved_chunks, query)


answer = generate_answer(prompt)


print("\nAnswer\n")
print(answer)