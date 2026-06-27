def build_prompt(context, question):

    context = "\n\n".join(context)

    return f"""
You are an expert teaching assistant.

Answer the question using ONLY the provided context.

If the answer is spread across multiple chunks, combine the information into one complete answer.

If the answer truly does not exist in the context, reply exactly:

I don't know based on the provided documents.

Context:

{context}

Question:
{question}

Answer:
"""