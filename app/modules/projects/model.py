import secrets
from datetime import datetime, timezone

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def _generate_public_id() -> str:
    return f"proj_{secrets.token_urlsafe(12)}"


class ProjectBase(SQLModel):
    name: str = Field(max_length=255)
    system_prompt: str | None = Field(default=None)
    allowed_domains: list[str] = Field(default_factory=list, sa_column=Column(JSON, default=[]))
    theme: dict | None = Field(default=None, sa_column=Column(JSON, nullable=True))


class Project(ProjectBase, table=True):
    __tablename__ = "projects"

    id: int | None = Field(default=None, primary_key=True)
    public_id: str = Field(
        default_factory=_generate_public_id,
        max_length=64,
        unique=True,
        index=True,
    )
    owner_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class ProjectCreate(SQLModel):
    name: str = Field(max_length=255)
    system_prompt: str | None = None
    allowed_domains: list[str] = Field(default_factory=list)
    theme: dict | None = None


class ProjectRead(SQLModel):
    id: int
    public_id: str
    name: str
    system_prompt: str | None
    allowed_domains: list[str]
    theme: dict | None
    owner_id: int
    created_at: datetime
    updated_at: datetime


class ProjectUpdate(SQLModel):
    name: str | None = None
    system_prompt: str | None = None
    allowed_domains: list[str] | None = None
    theme: dict | None = None
