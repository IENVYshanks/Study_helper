from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.models.chunk import Chunk
from app.models.document import Document
from app.schemas.documents import DocumentResponse
from app.services.embedding_service import EmbeddingService
from app.services.storage_service import StorageService
from app.services.text_extraction_service import TextExtractionService
from app.services.text_processing_service import TextProcessingService
from app.services.vector_store import vector_store


class DocumentService:
    def __init__(
        self,
        storage: StorageService,
        extractor: TextExtractionService,
        processor: TextProcessingService,
        embedder: EmbeddingService,
    ) -> None:
        self.storage = storage
        self.extractor = extractor
        self.processor = processor
        self.embedder = embedder

    async def process_upload(self, file: UploadFile, user_id: str) -> DocumentResponse:
        self._validate_file(file)
        path = await self.storage.save_upload(file)
        text = self.extractor.extract(path)
        chunks = self.processor.chunk(text)

        if not chunks:
            raise ValueError("No readable text found in uploaded document.")

        document = Document(
            id=uuid4().hex,
            user_id=user_id,
            file_name=file.filename or path.name,
            file_path=str(path),
            content_type=file.content_type,
            chunk_count=len(chunks),
        )

        vector_store.add_chunks(self._build_chunks(document, chunks))

        return DocumentResponse(
            document_id=document.id,
            user_id=document.user_id,
            file_name=document.file_name,
            chunk_count=document.chunk_count,
            created_at=document.created_at,
        )

    def _validate_file(self, file: UploadFile) -> None:
        extension = Path(file.filename or "").suffix.lower()
        if extension not in settings.allowed_extensions:
            allowed = ", ".join(sorted(settings.allowed_extensions))
            raise ValueError(f"Unsupported file type. Allowed types: {allowed}")

    def _build_chunks(self, document: Document, texts: list[str]) -> list[Chunk]:
        return [
            Chunk(
                id=uuid4().hex,
                user_id=document.user_id,
                document_id=document.id,
                file_name=document.file_name,
                chunk_number=index,
                text=text,
                embedding=self.embedder.embed(text),
            )
            for index, text in enumerate(texts, start=1)
        ]


def get_document_service() -> DocumentService:
    return DocumentService(
        storage=StorageService(),
        extractor=TextExtractionService(),
        processor=TextProcessingService(),
        embedder=EmbeddingService(),
    )
