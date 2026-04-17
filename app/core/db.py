from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.core.config import settings

# ─────────────────────────────────────────────────────────────
# Engine — the connection pool to Postgres.
# Created once at import time, shared across the entire app.
# ─────────────────────────────────────────────────────────────
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.APP_ENV == "development"),  # log SQL in dev
    pool_pre_ping=True,  # verify conns before using
    pool_size=5,  # baseline pool size
    max_overflow=10,  # extra conns under load
)

# ─────────────────────────────────────────────────────────────
# Session factory — creates a new AsyncSession per request.
# expire_on_commit=False keeps objects usable after commit,
# which matters because FastAPI serializes responses *after*
# the session would normally expire attributes.
# ─────────────────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# ─────────────────────────────────────────────────────────────
# FastAPI dependency — yields a session per request, then
# closes it. Use it in routes like:
#   async def endpoint(db: AsyncSession = Depends(get_db)): ...
# ─────────────────────────────────────────────────────────────
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        # session is closed automatically by the context manager


# ─────────────────────────────────────────────────────────────
# Metadata re-export. Alembic needs this to auto-generate
# migrations by comparing our SQLModel table definitions to
# the actual DB schema.
# ─────────────────────────────────────────────────────────────
metadata = SQLModel.metadata
