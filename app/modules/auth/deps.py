from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.auth.firebase import verify_id_token
from app.modules.users.model import User
from app.modules.users.repo import upsert_user

_bearer = HTTPBearer()


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Verify Firebase token, upsert the user row, and return it.

    This is the main auth dependency — inject it in any protected route.
    """
    try:
        claims = verify_id_token(creds.credentials)
    except (InvalidIdTokenError, ExpiredIdTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
        )

    user = await upsert_user(
        db,
        firebase_uid=claims["uid"],
        email=claims.get("email", ""),
        name=claims.get("name"),
    )
    return user
