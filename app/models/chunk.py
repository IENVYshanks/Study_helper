from dataclasses import dataclass


@dataclass(slots=True)
class Chunk:
    id: str
    user_id: str
    document_id: str
    file_name: str
    chunk_number: int
    text: str
    embedding: list[float]
