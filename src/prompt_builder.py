def build_prompt(chunks, question):

    context = "\n\n".join(chunks)

    prompt = f"""
You are a helpful research assistant.

Answer the question using ONLY the context below.

If the answer is not found in the context, reply:

"I don't know based on the provided document."

Context:

{context}

Question:

{question}

Answer:
"""

    return prompt