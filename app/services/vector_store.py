from math import fsum

from app.models.chunk import Chunk


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks: list[Chunk] = []

    def add_chunks(self, chunks: list[Chunk]) -> None:
        self._chunks.extend(chunks)

    def search(
        self,
        query_embedding: list[float],
        user_id: str,
        document_id: str | None = None,
        limit: int = 4,
    ) -> list[tuple[Chunk, float]]:
        candidates = [
            chunk
            for chunk in self._chunks
            if chunk.user_id == user_id and (document_id is None or chunk.document_id == document_id)
        ]

        scored = [
            (chunk, self._cosine_similarity(query_embedding, chunk.embedding))
            for chunk in candidates
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:limit]

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        return fsum(a * b for a, b in zip(left, right))


vector_store = InMemoryVectorStore()
