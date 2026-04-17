from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.auth.deps import get_current_user
from app.modules.documents.model import DocumentRead
from app.modules.documents import repo, service
from app.modules.projects import repo as project_repo
from app.modules.users.model import User

router = APIRouter(prefix="/api/projects/{project_id}/documents", tags=["documents"])


async def _get_owned_project(project_id: int, current_user: User, db: AsyncSession):
    project = await project_repo.get_by_id(db, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def upload_document(
    project_id: int,
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_owned_project(project_id, current_user, db)
    return await service.upload_document(db, project_id, file)


@router.get("", response_model=list[DocumentRead])
async def list_documents(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_owned_project(project_id, current_user, db)
    return await repo.list_by_project(db, project_id)


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    project_id: int,
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_owned_project(project_id, current_user, db)
    doc = await repo.get_by_id(db, doc_id)
    if not doc or doc.project_id != project_id:
        raise HTTPException(status_code=404, detail="Document not found")
    await repo.delete_document(db, doc)
