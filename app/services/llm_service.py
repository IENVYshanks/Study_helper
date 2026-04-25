from app.models.chunk import Chunk


class LLMService:
    def generate_answer(self, question: str, chunks: list[Chunk]) -> str:
        if not chunks:
            return "I could not find relevant content in the uploaded documents."

        context = "\n\n".join(chunk.text for chunk in chunks)
        return (
            "Based on the uploaded document context, here is the most relevant information:\n\n"
            f"{context}\n\n"
            f"Question: {question}"
        )
