from fastapi import FastAPI

from app.api.routes import chat, documents
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(documents.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
