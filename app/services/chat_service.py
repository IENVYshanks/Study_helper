from app.core.config import settings
from app.schemas.chat import ChatRequest, ChatResponse, SourceChunk
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_store import vector_store


class ChatService:
    def __init__(self, embedder: EmbeddingService, llm: LLMService) -> None:
        self.embedder = embedder
        self.llm = llm

    def answer(self, request: ChatRequest) -> ChatResponse:
        query_embedding = self.embedder.embed(request.question)
        results = vector_store.search(
            query_embedding=query_embedding,
            user_id=request.user_id,
            document_id=request.document_id,
            limit=settings.retrieval_limit,
        )

        chunks = [chunk for chunk, _score in results]
        answer = self.llm.generate_answer(request.question, chunks)

        return ChatResponse(
            answer=answer,
            sources=[
                SourceChunk(
                    document_id=chunk.document_id,
                    file_name=chunk.file_name,
                    chunk_number=chunk.chunk_number,
                    text=chunk.text,
                    score=round(score, 4),
                )
                for chunk, score in results
            ],
        )


def get_chat_service() -> ChatService:
    return ChatService(embedder=EmbeddingService(), llm=LLMService())
