import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.auth.firebase import init_firebase


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase()
    print(f"[startup] env={settings.APP_ENV}")
    yield
    print("[shutdown] bye")


app = FastAPI(title="EmbedChat API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"service": "embedchat-api", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.APP_ENV}


from app.modules.chat.router import router as chat_router  # noqa: E402
from app.modules.documents.router import router as documents_router  # noqa: E402
from app.modules.projects.router import router as projects_router  # noqa: E402

# --- routers ---
from app.modules.users.router import router as users_router  # noqa: E402

app.include_router(users_router)
app.include_router(projects_router)
app.include_router(documents_router)
app.include_router(chat_router)

# test
