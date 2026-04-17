from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.documents.model import Document


async def create_document(
    db: AsyncSession,
    project_id: int,
    filename: str,
    content_type: str,
    raw_text: str,
) -> Document:
    doc = Document(
        project_id=project_id,
        filename=filename,
        content_type=content_type,
        raw_text=raw_text,
        char_count=len(raw_text),
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


async def list_by_project(db: AsyncSession, project_id: int) -> list[Document]:
    result = await db.execute(
        select(Document).where(Document.project_id == project_id).order_by(Document.created_at.desc())
    )
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, doc_id: int) -> Document | None:
    return await db.get(Document, doc_id)


async def delete_document(db: AsyncSession, doc: Document) -> None:
    await db.delete(doc)
    await db.commit()
