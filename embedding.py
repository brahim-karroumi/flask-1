from functools import lru_cache

from openai import OpenAI

from config import EMBEDDING_MODEL, OPENROUTER_BASE_URL, required_env


@lru_cache(maxsize=1)
def get_openrouter_client():
    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=required_env("API_KEY"),
        timeout=30,
        max_retries=0,
    )


def embed_text(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Embedding input must be a nonempty string.")

    response = get_openrouter_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
        encoding_format="float",
    )

    return response.data[0].embedding