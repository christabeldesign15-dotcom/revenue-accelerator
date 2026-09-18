from models.finding import Finding


class TraceabilityRecord:
    def create(
        self,
        finding: Finding,
        decision: str,
        replacement: str | None = None,
    ) -> dict:
        return {
            "finding_id": finding.finding_id,
            "finding_type": finding.type,
            "severity": finding.severity,
            "decision": decision,
            "replacement": replacement,
            "start": finding.start,
            "end": finding.end,
        }
