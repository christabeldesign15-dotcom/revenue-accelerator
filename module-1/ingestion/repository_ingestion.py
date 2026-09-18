from pathlib import Path
from ingestion.file_metadata import FileMetadata


class RepositoryIngestion:
    SUPPORTED_EXTENSIONS = {
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".json", ".xml", ".yaml", ".yml",
        ".sql", ".md", ".txt", ".env",
        ".ini", ".cfg", ".conf",
    }

    def __init__(self, repository_path: str | Path | None = None):
        self.repository_path = (
            Path(repository_path)
            if repository_path is not None
            else None
        )

    def ingest(self) -> list[Path]:
        if self.repository_path is None:
            raise ValueError("repository_path is required for ingest()")

        return [FileMetadata.from_path(path, self.repository_path) for path in self.discover_files(self.repository_path)]

    def discover_files(self, repository_path: Path) -> list[Path]:
        if not repository_path.exists():
            raise FileNotFoundError(
                f"Repository not found: {repository_path}"
            )

        if not repository_path.is_dir():
            raise NotADirectoryError(
                f"Repository path is not a directory: {repository_path}"
            )

        return [
            path
            for path in repository_path.rglob("*")
            if path.is_file()
        ]

    def classify_files(self, repository_path: Path) -> list[dict]:
        results = []

        for path in self.discover_files(repository_path):
            if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                results.append({
                    "path": path,
                    "status": "Unsupported",
                })
                continue

            try:
                path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as error:
                results.append({
                    "path": path,
                    "status": "Failed to Read",
                    "error": str(error),
                })
                continue

            results.append({
                "path": path,
                "status": "Processed",
            })

        return results
