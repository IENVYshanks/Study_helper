import re

from app.core.config import settings


class TextProcessingService:
    def __init__(
        self,
        chunk_size: int = settings.chunk_size,
        chunk_overlap: int = settings.chunk_overlap,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def clean(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def chunk(self, text: str) -> list[str]:
        cleaned = self.clean(text)
        if not cleaned:
            return []

        chunks: list[str] = []
        start = 0

        while start < len(cleaned):
            end = start + self.chunk_size
            chunks.append(cleaned[start:end].strip())
            start = end - self.chunk_overlap

            if start <= 0:
                start = end

        return [chunk for chunk in chunks if chunk]
