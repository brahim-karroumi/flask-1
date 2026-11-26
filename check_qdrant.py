from vector_store import get_client


if __name__ == "__main__":
    response = get_client().get_collections()
    print("Connected to Qdrant Cloud!")
    print("Collections:", [item.name for item in response.collections])