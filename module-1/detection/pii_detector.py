import re
from models.finding import Finding


class PIIDetector:
    PATTERNS = {
        "email": re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        ),
        "phone": re.compile(
            r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)'
        ),
    }

    def detect(self, content: str) -> list[Finding]:
        findings = []

        for pii_type, pattern in self.PATTERNS.items():
            for match in pattern.finditer(content):
                findings.append(
                    Finding(
                        type=pii_type,
                        value=match.group(0),
                        start=match.start(),
                        end=match.end(),
                    )
                )

        return findings
