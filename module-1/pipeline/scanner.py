from ingestion.repository_ingestion import RepositoryIngestion
from detection.secret_detector import SecretDetector
from detection.pii_detector import PIIDetector
from classification.classifier import Classifier
from redaction.redactor import Redactor
from validation.validator import Validator
from reporting.report_generator import ReportGenerator


class Scanner:
    def __init__(self, repository_path: str):
        self.repository_path = repository_path

        self.ingestion = RepositoryIngestion(repository_path)
        self.detector = SecretDetector()
        self.pii_detector = PIIDetector()
        self.classifier = Classifier()
        self.redactor = Redactor()
        self.validator = Validator()
        self.report_generator = ReportGenerator()

    def scan(self):
        files = self.ingestion.ingest()

        all_findings = []
        redaction_statuses = []
        validation_passed = True

        for file in files:
            if not file.extracted_content:
                continue

            findings = self.detector.detect(file.extracted_content)
            findings.extend(self.pii_detector.detect(file.extracted_content))

            for finding in findings:
                self.classifier.classify(finding)

            redacted_content = self.redactor.redact(
                file.extracted_content,
                findings,
            )

            for finding in findings:
                redaction_statuses.append(
                    finding.value not in redacted_content
                )

            if not self.validator.validate(redacted_content, findings):
                validation_passed = False

            all_findings.extend(findings)

        return self.report_generator.generate(
            files_scanned=len(files),
            findings=all_findings,
            validation_passed=validation_passed,
            redaction_statuses=redaction_statuses,
        )
