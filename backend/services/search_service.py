import faiss
import pickle
import numpy as np

INDEX_PATH = "vector_store/index.faiss"
CHUNKS_PATH = "vector_store/chunks.pkl"


def search(query_embedding, k=5):

    index = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    query = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query, k)

    results = []

    for idx in indices[0]:
        results.append(chunks[idx])

    return results