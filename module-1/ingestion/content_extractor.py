from pathlib import Path

class ContentExtractor:
    def extract(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        return path.read_text(encoding="utf-8", errors="replace")
