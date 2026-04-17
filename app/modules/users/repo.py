from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.users.model import User, UserUpdate


async def get_by_firebase_uid(db: AsyncSession, firebase_uid: str) -> User | None:
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    return result.scalar_one_or_none()


async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


async def upsert_user(
    db: AsyncSession,
    *,
    firebase_uid: str,
    email: str,
    name: str | None,
) -> User:
    """Find existing user by firebase_uid or create a new one."""
    user = await get_by_firebase_uid(db, firebase_uid)
    if user is None:
        user = User(firebase_uid=firebase_uid, email=email, name=name)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user: User, data: UserUpdate) -> User:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(user, field, value)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
