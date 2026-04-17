from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.projects.model import Project, ProjectCreate, ProjectUpdate


async def create_project(db: AsyncSession, owner_id: int, data: ProjectCreate) -> Project:
    project = Project(**data.model_dump(), owner_id=owner_id)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def get_by_id(db: AsyncSession, project_id: int) -> Project | None:
    return await db.get(Project, project_id)


async def get_by_public_id(db: AsyncSession, public_id: str) -> Project | None:
    result = await db.execute(select(Project).where(Project.public_id == public_id))
    return result.scalar_one_or_none()


async def list_by_owner(db: AsyncSession, owner_id: int) -> list[Project]:
    result = await db.execute(
        select(Project).where(Project.owner_id == owner_id).order_by(Project.created_at.desc())
    )
    return list(result.scalars().all())


async def update_project(db: AsyncSession, project: Project, data: ProjectUpdate) -> Project:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(project, field, value)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project: Project) -> None:
    await db.delete(project)
    await db.commit()
