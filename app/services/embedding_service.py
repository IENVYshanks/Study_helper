import hashlib
import math


class EmbeddingService:
    """Small deterministic embedder for local development.

    Replace this service with OpenAI, sentence-transformers, or another
    embedding provider when you are ready for production-quality retrieval.
    """

    dimensions = 64

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions

        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:2], "big") % self.dimensions
            weight = 1.0 + (digest[2] / 255.0)
            vector[index] += weight

        return self._normalize(vector)

    def _normalize(self, vector: list[float]) -> list[float]:
        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector
        return [value / magnitude for value in vector]
