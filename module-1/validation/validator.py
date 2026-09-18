from models.finding import Finding


class Validator:
    def validate(
        self,
        original: str,
        sanitized: str,
        findings: list[Finding],
        decisions: dict[str, str] | None = None,
    ) -> dict:
        decisions = decisions or {}

        sensitive_data_remaining = any(
            finding.value in sanitized
            and decisions.get(finding.finding_id, "REDACT") == "REDACT"
            for finding in findings
        )

        structural_valid = bool(sanitized.strip()) if original.strip() else True

        return {
            "sensitive_data_remaining": sensitive_data_remaining,
            "structural_valid": structural_valid,
            "valid": (
                not sensitive_data_remaining
                and structural_valid
            ),
        }
