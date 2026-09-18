from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class FileMetadata:
    file_path: str
    file_name: str
    file_type: str
    file_size: int
    processing_status: str = "Pending"
    extracted_content: Optional[str] = None

    @classmethod
    def from_path(cls, file_path: Path, repository_root: Path) -> "FileMetadata":
        relative_path = file_path.relative_to(repository_root)
        return cls(
            file_path=str(relative_path),
            file_name=file_path.name,
            file_type=file_path.suffix.lower(),
            file_size=file_path.stat().st_size,
        )
