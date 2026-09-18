import re

from models.finding import Finding


class SecretDetector:
    PATTERNS = {
        "api_key": re.compile(
            r'(?i)\bapi[_-]?key\s*[:=]\s*["\']?([A-Za-z0-9_\-]{8,})["\']?'
        ),
        "password": re.compile(
            r'(?i)\bpassword\s*[:=]\s*["\']?([^\s"\']{6,})["\']?'
        ),
        "token": re.compile(
            r'(?i)\btoken\s*[:=]\s*["\']?([A-Za-z0-9_\-\.]{8,})["\']?'
        ),
    }

    def detect(self, content: str) -> list[Finding]:
        findings = []

        for secret_type, pattern in self.PATTERNS.items():
            for match in pattern.finditer(content):
                findings.append(
                    Finding(
                        type=secret_type,
                        value=match.group(1),
                        start=match.start(1),
                        end=match.end(1),
                    )
                )

        return findings
