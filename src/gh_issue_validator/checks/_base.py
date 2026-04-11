from abc import ABC, abstractmethod

from gh_issue_validator.markdown import _parse_segments
from gh_issue_validator.report import ValidationReport
from gh_issue_validator.types import SegmentsMap


class ValidationCheck(ABC):
    @abstractmethod
    def check(self, *, segments: SegmentsMap, report: ValidationReport) -> None:
        pass


class Validator:
    def __init__(self, *, checks: list[ValidationCheck]) -> None:
        self.checks = checks

    def validate(self, *, markdown: str) -> ValidationReport:
        report = ValidationReport()
        segments = _parse_segments(markdown)

        for check in self.checks:
            check.check(segments=segments, report=report)

        return report
