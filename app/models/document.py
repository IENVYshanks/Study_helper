from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class Document:
    id: str
    user_id: str
    file_name: str
    file_path: str
    content_type: str | None
    chunk_count: int
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
