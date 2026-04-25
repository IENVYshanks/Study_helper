from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    def __init__(self, upload_dir: Path = settings.upload_dir) -> None:
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, file: UploadFile) -> Path:
        extension = Path(file.filename or "").suffix.lower()
        stored_name = f"{uuid4().hex}{extension}"
        destination = self.upload_dir / stored_name

        content = await file.read()
        destination.write_bytes(content)
        await file.seek(0)
        return destination
