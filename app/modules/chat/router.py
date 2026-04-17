from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.chat.models import ChatRequest, ChatResponse
from app.modules.chat.service import handle_chat
from app.modules.projects import repo as project_repo

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint — called by ChatWidget. No auth required, uses project_id (public_id)."""
    project = await project_repo.get_by_public_id(db, req.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return await handle_chat(db, project, req.message)
