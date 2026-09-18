from models.finding import Finding


class DecisionEngine:
    REDACT_TYPES = {
        "api_key",
        "password",
        "secret",
        "token",
    }

    REVIEW_TYPES = {
        "email",
        "phone",
    }

    def decide(self, finding: Finding) -> str:
        if finding.type in self.REDACT_TYPES:
            return "REDACT"

        if finding.type in self.REVIEW_TYPES:
            return "REVIEW"

        return "REVIEW"
