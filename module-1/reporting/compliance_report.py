from dataclasses import dataclass, field


@dataclass
class ComplianceReport:
    files_scanned: int = 0
    findings_detected: int = 0
    findings_redacted: int = 0
    validation_passed: bool = False
    status: str = "UNKNOWN"
    findings: list[dict] = field(default_factory=list)
