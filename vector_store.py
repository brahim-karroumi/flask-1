from functools import lru_cache

from qdrant_client import QdrantClient, models

from config import COLLECTION_NAME, required_env
from embedding import embed_text


class IndexNotReadyError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    return QdrantClient(
        url=required_env("QDRANT_URL"),
        api_key=required_env("QDRANT_API_KEY"),
        timeout=10,
    )


def ensure_collection(vector_size):
    client = get_client()

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )
        return

    vectors = client.get_collection(COLLECTION_NAME).config.params.vectors
    if (
        not isinstance(vectors, models.VectorParams)
        or vectors.size != vector_size
        or vectors.distance != models.Distance.COSINE
    ):
        raise ValueError(
            "Collection configuration differs. Choose a new "
            "QDRANT_COLLECTION name and re-index with the chosen model."
        )


def search_chunks(question, top_k=3):
    if not isinstance(top_k, int) or not 1 <= top_k <= 10:
        raise ValueError("top_k must be an integer between 1 and 10.")

    client = get_client()
    if not client.collection_exists(COLLECTION_NAME):
        raise IndexNotReadyError("The search index is not ready.")

    if client.count(collection_name=COLLECTION_NAME, exact=True).count == 0:
        raise IndexNotReadyError("The search index has no documents.")

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embed_text(question),
        limit=top_k,
        with_payload=True,
        with_vectors=False,
    )

    matches = []
    for point in response.points:
        payload = point.payload or {}
        text = payload.get("text", "")
        if not text:
            continue
        matches.append({
            "id": str(point.id),
            "text": text,
            "metadata": payload.get("metadata", {}),
            "score": point.score,
        })

    return matches