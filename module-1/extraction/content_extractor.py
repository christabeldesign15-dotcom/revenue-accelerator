from pathlib import Path


class ContentExtractor:
    SUPPORTED_EXTENSIONS = {
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".json", ".xml", ".yaml", ".yml",
        ".sql", ".md", ".txt", ".env",
        ".ini", ".cfg", ".conf",
    }

    def extract(self, file_path: Path) -> dict:
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return {
                "path": file_path,
                "status": "Unsupported",
                "content": None,
            }

        try:
            content = file_path.read_text(encoding="utf-8")

            return {
                "path": file_path,
                "status": "Processed",
                "content": content,
            }

        except (OSError, UnicodeDecodeError) as error:
            return {
                "path": file_path,
                "status": "Failed to Read",
                "content": None,
                "error": str(error),
            }
