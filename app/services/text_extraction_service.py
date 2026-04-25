from pathlib import Path

from pypdf import PdfReader


class TextExtractionService:
    def extract(self, path: Path) -> str:
        extension = path.suffix.lower()

        if extension == ".pdf":
            return self._extract_pdf(path)
        if extension == ".txt":
            return path.read_text(encoding="utf-8", errors="ignore")

        raise ValueError(f"Unsupported file type: {extension}")

    def _extract_pdf(self, path: Path) -> str:
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)
