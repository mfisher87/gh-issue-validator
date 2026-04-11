"""Tests for the checks/_base.py module."""

from gh_issue_validator.checks._base import ValidationCheck, Validator
from gh_issue_validator.report import ValidationIssue, ValidationReport
from gh_issue_validator.types import SegmentsMap


class AlwaysFailsCheck(ValidationCheck):
    """Mock check that always adds one issue."""

    def check(  # noqa: D102
        self,
        *,
        segments: SegmentsMap,  # noqa: ARG002
        report: ValidationReport,
    ) -> None:
        report.add_issue(ValidationIssue(code="always-fails", message="mock failure"))


class AlwaysPassesCheck(ValidationCheck):
    """Mock check that never adds issues."""

    def check(  # noqa: D102
        self,
        *,
        segments: SegmentsMap,
        report: ValidationReport,
    ) -> None:
        pass


class TestValidator:
    def test_validator_with_failing_check_produces_failure_report(self) -> None:
        """Should produce a failure report when a check adds issues."""
        validator = Validator(checks=[AlwaysFailsCheck()])
        report = validator.validate(markdown="### Some heading\n\ncontent")
        assert report.is_failure
        assert report.issues[0].code == "always-fails"

    def test_validator_with_passing_check_produces_success_report(self) -> None:
        """Should produce a success report when no checks add issues."""
        validator = Validator(checks=[AlwaysPassesCheck()])
        report = validator.validate(markdown="### Some heading\n\ncontent")
        assert not report.is_failure

    def test_validator_runs_all_checks(self) -> None:
        """Should run every check and accumulate all issues."""
        validator = Validator(checks=[AlwaysFailsCheck(), AlwaysFailsCheck()])
        report = validator.validate(markdown="")
        assert len(report.issues) == 2

    def test_validator_with_no_checks_produces_success_report(self) -> None:
        """Should produce a success report when given an empty checks list."""
        validator = Validator(checks=[])
        report = validator.validate(markdown="anything")
        assert not report.is_failure
