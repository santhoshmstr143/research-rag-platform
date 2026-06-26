import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from extract import extract_text
from chunk import create_chunks


def build_vector_store():

    text = extract_text("text1.pdf")

    chunks = create_chunks(text)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(chunks)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, model, chunks


if __name__ == "__main__":

    index, model, chunks = build_vector_store()

    print("Dimension:", index.d)
    print("Vectors Stored:", index.ntotal)