from dataclasses import dataclass

@dataclass
class Finding:
    type: str
    value: str
    start: int
    end: int
    severity: str = "medium"
    confidence: float = 1.0
