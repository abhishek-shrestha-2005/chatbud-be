import firebase_admin
from firebase_admin import auth, credentials

from app.core.config import settings

_app: firebase_admin.App | None = None


def init_firebase() -> None:
    global _app
    if _app is not None:
        return
    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
    _app = firebase_admin.initialize_app(cred)


def verify_id_token(id_token: str) -> dict:
    """Verify a Firebase ID token and return the decoded claims.

    Returns dict with at minimum: uid, email, name (if available).
    Raises firebase_admin.auth.InvalidIdTokenError on bad/expired tokens.
    """
    return auth.verify_id_token(id_token)
