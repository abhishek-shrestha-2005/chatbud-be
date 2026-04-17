from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.rag.model import Chunk


async def insert_chunks(db: AsyncSession, chunks: list[Chunk]) -> list[Chunk]:
    for chunk in chunks:
        db.add(chunk)
    await db.commit()
    for chunk in chunks:
        await db.refresh(chunk)
    return chunks


async def delete_by_document(db: AsyncSession, document_id: int) -> None:
    result = await db.execute(select(Chunk).where(Chunk.document_id == document_id))
    for chunk in result.scalars().all():
        await db.delete(chunk)
    await db.commit()


async def search_similar(
    db: AsyncSession,
    project_id: int,
    query_embedding: list[float],
    top_k: int = 5,
) -> list[Chunk]:
    """Find top_k most similar chunks for a project using cosine distance."""
    stmt = (
        select(Chunk)
        .where(Chunk.project_id == project_id)
        .order_by(Chunk.embedding.cosine_distance(query_embedding))
        .limit(top_k)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())
