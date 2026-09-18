from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Finding:
    type: str
    value: str
    start: int
    end: int
    severity: str = "medium"
    confidence: float = 1.0
    finding_id: str = ""

    def __post_init__(self):
        if not self.finding_id:
            self.finding_id = str(uuid4())
