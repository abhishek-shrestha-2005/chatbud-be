from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class DocumentBase(SQLModel):
    filename: str = Field(max_length=512)
    content_type: str = Field(max_length=128, default="text/plain")


class Document(DocumentBase, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    raw_text: str = Field(default="")
    char_count: int = Field(default=0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class DocumentRead(DocumentBase):
    id: int
    project_id: int
    char_count: int
    created_at: datetime
