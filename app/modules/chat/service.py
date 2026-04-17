from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.llm import generate_response
from app.modules.chat.models import ChatResponse
from app.modules.projects.model import Project
from app.modules.rag.retreiver import retrieve


async def handle_chat(db: AsyncSession, project: Project, message: str) -> ChatResponse:
    """RAG pipeline: retrieve chunks → build context → call LLM."""
    chunks = await retrieve(db, project.id, message, top_k=5)

    if not chunks:
        return ChatResponse(
            reply="I don't have any knowledge base content to answer from yet.",
            sources=[],
        )

    context = "\n\n---\n\n".join(c.content for c in chunks)
    sources = list({c.content[:80] + "..." for c in chunks})

    reply = await generate_response(project.system_prompt, context, message)

    return ChatResponse(reply=reply, sources=sources)
