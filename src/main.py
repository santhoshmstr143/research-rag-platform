import os
import json

from extract import extract_text
from chunk import create_chunks


text = extract_text("text1.pdf")

print("Text extracted successfully")
print("Total characters:", len(text))


chunks = create_chunks(text)

print("Total chunks:", len(chunks))


chunk_data = []

for idx, chunk in enumerate(chunks):
    chunk_data.append(
        {
            "paper_id": 1,
            "chunk_id": idx + 1,
            "text": chunk
        }
    )


os.makedirs("output", exist_ok=True)


with open("output/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunk_data, f, indent=4, ensure_ascii=False)


print("Chunks saved successfully")
print("Saved to: output/chunks.json")