from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(max_length=255, index=True)
    name: str | None = Field(default=None, max_length=255)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    firebase_uid: str = Field(
        max_length=128,
        unique=True,
        index=True,
        description="Firebase Authentication UID",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class UserCreate(UserBase):
    firebase_uid: str = Field(max_length=128)


class UserRead(UserBase):
    id: int
    firebase_uid: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
