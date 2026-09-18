import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "module-1"))

from ingestion.repository_ingestion import RepositoryIngestion


def test_repository_ingestion():
    repository_path = Path(__file__).parent / "test_data" / "sample-repository"
    files = RepositoryIngestion(str(repository_path)).ingest()
    assert len(files) == 1
    assert files[0].file_name == "hello.py"
    assert files[0].file_type == ".py"
    assert files[0].processing_status == "Pending"
