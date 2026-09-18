from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "module-1"))

from classification.classifier import Classifier


def test_api_key_is_high_risk():
    result = Classifier().classify("API_KEY")
    assert result == "HIGH"
