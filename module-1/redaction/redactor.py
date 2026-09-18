from models.finding import Finding


class Redactor:
    REPLACEMENTS = {
        "api_key": "[REDACTED_SECRET]",
        "password": "[REDACTED_SECRET]",
        "secret": "[REDACTED_SECRET]",
        "token": "[REDACTED_TOKEN]",
    }

    def redact(self, content: str, finding: Finding, decision: str) -> str:
        if decision != "REDACT":
            return content

        replacement = self.REPLACEMENTS.get(
            finding.type,
            "[REDACTED_SECRET]",
        )

        return (
            content[:finding.start]
            + replacement
            + content[finding.end:]
        )
