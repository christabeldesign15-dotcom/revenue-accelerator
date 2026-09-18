from reporting.compliance_report import ComplianceReport
from models.finding import Finding


class ReportGenerator:
    def generate(
        self,
        files_scanned: int,
        findings: list[Finding],
        validation_passed: bool,
        redaction_statuses: list[bool],
    ) -> ComplianceReport:

        report_findings = []

        for finding, was_redacted in zip(findings, redaction_statuses):
            report_findings.append({
                "type": finding.type,
                "severity": finding.severity,
                "redacted": was_redacted,
            })

        findings_redacted = sum(redaction_statuses)

        status = "PASS" if validation_passed else "FAIL"

        return ComplianceReport(
            files_scanned=files_scanned,
            findings_detected=len(findings),
            findings_redacted=findings_redacted,
            validation_passed=validation_passed,
            status=status,
            findings=report_findings,
        )
