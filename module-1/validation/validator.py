from models.finding import Finding


class Validator:
    def validate(self, content: str, findings: list[Finding]) -> bool:
        for finding in findings:
            if finding.value in content:
                return False

        return True
