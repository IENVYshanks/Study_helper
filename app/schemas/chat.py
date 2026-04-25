from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    user_id: str = "demo-user"
    document_id: str | None = None


class SourceChunk(BaseModel):
    document_id: str
    file_name: str
    chunk_number: int
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
