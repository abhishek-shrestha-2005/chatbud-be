from google import genai

from app.core.config import settings

_client: genai.Client | None = None

MODEL_NAME = "gemini-embedding-001"
EMBEDDING_DIM = 3072


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed list of texts via Google embedding API."""
    client = _get_client()
    result = client.models.embed_content(
        model=MODEL_NAME,
        contents=texts,
    )
    return [e.values for e in result.embeddings]


def embed_query(query: str) -> list[float]:
    """Embed single query string."""
    return embed_texts([query])[0]
