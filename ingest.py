from uuid import NAMESPACE_URL, uuid5

from qdrant_client import models

from config import COLLECTION_NAME, EMBEDDING_MODEL
from data.champions_league import RESULTS
from embedding import embed_text
from vector_store import ensure_collection, get_client

SOURCE_ID = "champions_league/2026-11-25"


def ingest():
    chunks = [
        paragraph.strip()
        for paragraph in RESULTS.split("\n\n")
        if paragraph.strip()
    ]
    if not chunks:
        raise ValueError("No source text to index.")

    points = []
    for index, chunk in enumerate(chunks):
        vector = embed_text(chunk)
        point_id = str(uuid5(
            NAMESPACE_URL, f"{SOURCE_ID}/chunk/{index}"
        ))

        points.append(models.PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "text": chunk,
                "metadata": {
                    "source": SOURCE_ID,
                    "chunk_index": index,
                    "embedding_model": EMBEDDING_MODEL,
                },
            },
        ))
        print(f"Embedded {index + 1}/{len(chunks)}")

    ensure_collection(vector_size=len(points[0].vector))
    client = get_client()
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True,
    )

    count = client.count(
        collection_name=COLLECTION_NAME, exact=True
    ).count
    print(f"Stored chunks in {COLLECTION_NAME}: {count}")


if __name__ == "__main__":
    ingest()