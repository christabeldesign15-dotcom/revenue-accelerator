from models.finding import Finding

class Classifier:
    SEVERITY_MAP = {
        "api_key": "high",
        "password": "high",
        "secret": "high",
        "token": "high",
        "email": "medium",
        "phone": "medium",
    }

    def classify(self, finding: Finding) -> Finding:
        finding.severity = self.SEVERITY_MAP.get(finding.type, "medium")
        return finding
