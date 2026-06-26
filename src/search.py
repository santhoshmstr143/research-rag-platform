import numpy as np

from vector_store import build_vector_store
from prompt_builder import build_prompt
from gemini import generate_answer


index, model, chunks = build_vector_store()


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