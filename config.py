import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
EMBEDDING_MODEL = "openai/text-embedding-3-large"
CHAT_MODEL = os.getenv("CHAT_MODEL", "openai/gpt-5-mini")
COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION", "champions_league_large_v1"
)


def required_env(name):
    value = os.getenv(name)
    if not value or not value.strip():
        raise RuntimeError(f"Missing environment variable: {name}")
    return value.strip()