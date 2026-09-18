import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "module-1"))

from detection.secret_detector import SecretDetector


def test_detects_fake_api_key():
    content = "API_KEY=sk_test_FAKE_123456789"
    findings = SecretDetector().detect(content)
    assert len(findings) >= 1
