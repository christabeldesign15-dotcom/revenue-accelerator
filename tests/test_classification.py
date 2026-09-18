from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "module-1"))

from classification.classifier import Classifier
from models.finding import Finding


def make_finding(finding_type: str) -> Finding:
    return Finding(
        type=finding_type,
        value="test-value",
        start=0,
        end=10,
    )


def test_api_key_is_high_risk():
    finding = make_finding("api_key")
    result = Classifier().classify(finding)
    assert result.severity == "high"


def test_password_is_high_risk():
    finding = make_finding("password")
    result = Classifier().classify(finding)
    assert result.severity == "high"


def test_token_is_high_risk():
    finding = make_finding("token")
    result = Classifier().classify(finding)
    assert result.severity == "high"


def test_email_is_medium_risk():
    finding = make_finding("email")
    result = Classifier().classify(finding)
    assert result.severity == "medium"


def test_phone_is_medium_risk():
    finding = make_finding("phone")
    result = Classifier().classify(finding)
    assert result.severity == "medium"
