from models.finding import Finding


class Redactor:
    def redact(self, content: str, findings: list[Finding]) -> str:
        redacted = content

        # Replace from the end so earlier positions stay valid
        for finding in sorted(findings, key=lambda item: item.start, reverse=True):
            redacted = (
                redacted[:finding.start]
                + "[REDACTED]"
                + redacted[finding.end:]
            )

        return redacted
