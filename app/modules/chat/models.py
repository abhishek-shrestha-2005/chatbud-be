from sqlmodel import SQLModel


class ChatRequest(SQLModel):
    project_id: str  # public_id from widget
    message: str


class ChatResponse(SQLModel):
    reply: str
    sources: list[str] = []
