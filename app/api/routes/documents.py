from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.schemas.documents import DocumentResponse
from app.services.document_service import DocumentService, get_document_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = "demo-user",
    service: DocumentService = Depends(get_document_service),
) -> DocumentResponse:
    try:
        return await service.process_upload(file=file, user_id=user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
