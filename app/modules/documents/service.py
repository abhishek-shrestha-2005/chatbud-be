from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.documents import repo
from app.modules.documents.model import Document
from app.modules.rag.chunker import chunk_text
from app.modules.rag.embedder import embed_texts
from app.modules.rag.model import Chunk
from app.modules.rag import repo as rag_repo


async def upload_document(
    db: AsyncSession,
    project_id: int,
    file: UploadFile,
) -> Document:
    """Read file, store document, chunk, embed, store vectors."""
    content = await file.read()
    raw_text = content.decode("utf-8", errors="replace")

    doc = await repo.create_document(
        db,
        project_id=project_id,
        filename=file.filename or "untitled",
        content_type=file.content_type or "text/plain",
        raw_text=raw_text,
    )

    # chunk + embed
    text_chunks = chunk_text(raw_text)
    if text_chunks:
        embeddings = embed_texts(text_chunks)
        chunks = [
            Chunk(
                document_id=doc.id,
                project_id=project_id,
                content=text,
                chunk_index=i,
                embedding=emb,
            )
            for i, (text, emb) in enumerate(zip(text_chunks, embeddings))
        ]
        await rag_repo.insert_chunks(db, chunks)

    return doc
