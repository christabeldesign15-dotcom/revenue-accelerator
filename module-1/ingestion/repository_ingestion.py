from .content_extractor import ContentExtractor
from pathlib import Path
from typing import List

from .file_metadata import FileMetadata


class RepositoryIngestion:
    """Handles repository ingestion for Module 1."""

    SUPPORTED_EXTENSIONS = {
        ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".cs",
        ".go", ".rs", ".php", ".rb", ".swift", ".kt", ".json",
        ".xml", ".yaml", ".yml", ".sql", ".md", ".txt", ".env",
        ".conf", ".ini", ".properties",
    }

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

        if not self.repository_path.exists():
            raise FileNotFoundError(f"Repository not found: {self.repository_path}")

        if not self.repository_path.is_dir():
            raise ValueError(f"Repository path is not a directory: {self.repository_path}")

    def ingest(self) -> List[FileMetadata]:
        """Scan the repository and collect metadata for each file."""
        files: List[FileMetadata] = []
        extractor = ContentExtractor()

        for file_path in self.repository_path.rglob("*"):
            if not file_path.is_file():
                continue

            try:
                metadata = FileMetadata.from_path(file_path, self.repository_path)

                if self._is_supported(file_path):
                    metadata.processing_status = "Pending"
                    metadata.extracted_content = extractor.extract(file_path)
                else:
                    metadata.processing_status = "Unsupported"

                files.append(metadata)

            except (OSError, ValueError):
                metadata = FileMetadata(
                    file_path=str(file_path),
                    file_name=file_path.name,
                    file_type=file_path.suffix.lower(),
                    file_size=0,
                    processing_status="Failed to Read",
                )
                files.append(metadata)

        return files

    def _is_supported(self, file_path: Path) -> bool:
        """Determine whether the file type is supported."""
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
