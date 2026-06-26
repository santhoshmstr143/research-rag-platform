from sentence_transformers import SentenceTransformer

from extract import extract_text
from chunk import create_chunks

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

pdf_path = BASE_DIR / "data" / "text1.pdf"

text = extract_text(str(pdf_path))

chunks = create_chunks(text)

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

print("Chunks:", len(chunks))
print("Embeddings:", len(embeddings))
print("Dimension:", len(embeddings[0]))