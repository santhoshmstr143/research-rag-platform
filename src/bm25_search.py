import json
import re

from rank_bm25 import BM25Okapi


def tokenize(text):

    return re.findall(r"\w+", text.lower())


with open("indexes/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


corpus = []

for chunk in chunks:

    corpus.append(tokenize(chunk["text"]))


bm25 = BM25Okapi(corpus)


query = input("Enter your question: ")


tokenized_query = tokenize(query)


scores = bm25.get_scores(tokenized_query)


top_indices = sorted(
    range(len(scores)),
    key=lambda i: scores[i],
    reverse=True
)[:5]


print("\nTop BM25 Results\n")


for i in top_indices:

    print("--------------------------------------------------")
    print(chunks[i]["paper_name"])
    print("Chunk:", chunks[i]["chunk_id"])
    print("Score:", round(scores[i], 2))
    print(chunks[i]["text"])