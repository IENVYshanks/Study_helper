from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    document_id: str
    user_id: str
    file_name: str
    chunk_count: int
    created_at: datetime
