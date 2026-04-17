from google import genai

from app.core.config import settings

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


async def generate_response(system_prompt: str | None, context: str, question: str) -> str:
    """Call Gemini Flash to generate answer from context + question."""
    client = _get_client()

    prompt = (
        f"Answer the user's question using ONLY the context below. "
        f"If the context doesn't contain the answer, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )

    config = {}
    if system_prompt:
        config["system_instruction"] = system_prompt

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=config,
    )
    return response.text
