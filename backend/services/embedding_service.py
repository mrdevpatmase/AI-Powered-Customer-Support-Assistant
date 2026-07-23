import requests
from backend.config import Config

JINA_API_KEY = Config.JINA_API_KEY
URL = "https://api.jina.ai/v1/embeddings"


def create_embeddings(chunks):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JINA_API_KEY}"
    }

    payload = {
        "model": "jina-embeddings-v3",
        "input": chunks
    }

    response = requests.post(
        URL,
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    data = response.json()

    embeddings = [item["embedding"] for item in data["data"]]

    return embeddings


def create_query_embedding(question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JINA_API_KEY}"
    }

    payload = {
        "model": "jina-embeddings-v3",
        "input": [question]
    }

    response = requests.post(
        URL,
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    return response.json()["data"][0]["embedding"]