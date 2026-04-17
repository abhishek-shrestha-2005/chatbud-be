from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.rag import repo
from app.modules.rag.embedder import embed_query
from app.modules.rag.model import Chunk


async def retrieve(db: AsyncSession, project_id: int, query: str, top_k: int = 5) -> list[Chunk]:
    """Embed query and find similar chunks from project's knowledge base."""
    query_embedding = embed_query(query)
    return await repo.search_similar(db, project_id, query_embedding, top_k)
