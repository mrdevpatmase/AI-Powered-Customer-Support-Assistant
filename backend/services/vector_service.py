import faiss
import numpy as np
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

VECTOR_DIR = os.path.join(PROJECT_ROOT, "vector_store")

os.makedirs(VECTOR_DIR, exist_ok=True)

def save_embeddings(embeddings, chunks):

    vectors = np.array(embeddings).astype("float32")

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)

    faiss.write_index(index, f"{VECTOR_DIR}/index.faiss")

    with open(f"{VECTOR_DIR}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return len(chunks)