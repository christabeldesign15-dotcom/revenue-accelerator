from pathlib import Path

from classification.classifier import Classifier
from compliance.assessment import ComplianceAssessment
from decision.decision_engine import DecisionEngine
from detection.pii_detector import PIIDetector
from detection.secret_detector import SecretDetector
from processing.repository_processor import RepositoryProcessor
from redaction.redactor import Redactor
from traceability.record import TraceabilityRecord
from validation.validator import Validator


class CompliancePipeline:
    def __init__(self):
        self.processor = RepositoryProcessor()
        self.secret_detector = SecretDetector()
        self.pii_detector = PIIDetector()
        self.classifier = Classifier()
        self.decision_engine = DecisionEngine()
        self.redactor = Redactor()
        self.validator = Validator()
        self.traceability = TraceabilityRecord()
        self.assessment = ComplianceAssessment()

    def run(self, repository_path: Path) -> dict:
        processed_files = self.processor.process(repository_path)

        file_results = []
        unresolved_review = False
        unresolved_high_risk = False
        validation_failed = False

        for file_item in processed_files:
            if file_item["status"] != "Processed":
                file_results.append(file_item)
                continue

            content = file_item["content"]

            findings = []
            findings.extend(self.secret_detector.detect(content))
            findings.extend(self.pii_detector.detect(content))

            for finding in findings:
                self.classifier.classify(finding)

            decisions = []
            traceability = []

            for finding in findings:
                decision = self.decision_engine.decide(finding)
                replacement = None

                if decision == "REDACT":
                    replacement = self.redactor.REPLACEMENTS.get(
                        finding.type,
                        "[REDACTED_SECRET]",
                    )

                decisions.append((finding, decision))

                traceability.append(
                    self.traceability.create(
                        finding=finding,
                        decision=decision,
                        replacement=replacement,
                    )
                )

                if decision == "REVIEW":
                    unresolved_review = True

                if (
                    finding.severity == "high"
                    and decision == "REVIEW"
                ):
                    unresolved_high_risk = True

            sanitized_content = content

            for finding, decision in sorted(
                decisions,
                key=lambda item: item[0].start,
                reverse=True,
            ):
                sanitized_content = self.redactor.redact(
                    sanitized_content,
                    finding,
                    decision,
                )

            decision_map = {
                finding.finding_id: decision
                for finding, decision in decisions
            }

            validation_result = self.validator.validate(
                content,
                sanitized_content,
                findings,
                decision_map,
            )

            if not validation_result["valid"]:
                validation_failed = True

            file_results.append(
                {
                    "path": file_item["path"],
                    "status": "Processed",
                    "content": content,
                    "sanitized_content": sanitized_content,
                    "traceability": traceability,
                    "validation": validation_result,
                }
            )

        status = self.assessment.assess(
            validation_valid=not validation_failed,
            unresolved_high_risk=unresolved_high_risk,
            unresolved_review=unresolved_review,
        )

        return {
            "status": status,
            "files": file_results,
        }
