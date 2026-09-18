class ComplianceAssessment:
    def assess(
        self,
        validation_valid: bool,
        unresolved_high_risk: bool,
        unresolved_review: bool,
    ) -> str:
        if not validation_valid:
            return "FAILED"

        if unresolved_high_risk:
            return "FAILED"

        if unresolved_review:
            return "REVIEW_REQUIRED"

        return "APPROVED"
