from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Study Helper"
    upload_dir: Path = Path("storage/uploads")
    allowed_extensions: set[str] = {".pdf", ".txt"}
    chunk_size: int = 900
    chunk_overlap: int = 150
    retrieval_limit: int = 4

    model_config = SettingsConfigDict(env_file=".env", env_prefix="STUDY_HELPER_")


settings = Settings()
