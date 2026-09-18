from pathlib import Path

from extraction.content_extractor import ContentExtractor
from ingestion.repository_ingestion import RepositoryIngestion


class RepositoryProcessor:
    def __init__(self):
        self.ingestion = RepositoryIngestion()
        self.extractor = ContentExtractor()

    def process(self, repository_path: Path) -> list[dict]:
        results = []

        for item in self.ingestion.classify_files(repository_path):
            if item["status"] != "Processed":
                results.append(
                    {
                        **item,
                        "content": None,
                    }
                )
                continue

            results.append(
                self.extractor.extract(item["path"])
            )

        return results
