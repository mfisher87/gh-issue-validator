"""Tests for the report.py module."""

import pytest

from gh_issue_validator.report import ValidationIssue, ValidationReport


@pytest.mark.parametrize(
    ("issues", "expected_is_failure"),
    [
        pytest.param([], False, id="empty report is not a failure"),
        pytest.param(
            [ValidationIssue(code="test", message="something broke")],
            True,
            id="one issue is a failure",
        ),
        pytest.param(
            [
                ValidationIssue(code="a", message="msg a"),
                ValidationIssue(code="b", message="msg b", heading="Some heading"),
            ],
            True,
            id="multiple issues is a failure",
        ),
    ],
)
def test_report_is_failure(
    issues: list[ValidationIssue],
    expected_is_failure: bool,
) -> None:
    """Should reflect is_failure based on whether issues have been added."""
    report = ValidationReport()
    for issue in issues:
        report.add_issue(issue)
    assert report.is_failure == expected_is_failure


def test_report_success_str_contents() -> None:
    """Should include expected content in str when successful."""
    report = ValidationReport()
    assert "Validation successful" in str(report)
    assert "failed" not in str(report)


def test_report_failure_str_contents() -> None:
    """Should include expected content in str when failed."""
    report = ValidationReport()
    report.add_issue(ValidationIssue(code="test", message="something is wrong"))
    output = str(report)
    assert "Validation failed" in output
    assert "something is wrong" in output


def test_report_success_github_issue_message_contents() -> None:
    """Should include expected contents in github issue message when successful."""
    report = ValidationReport()
    msg = report.github_issue_message
    assert "UTC" in msg
    assert "Validation successful" in msg


def test_report_failure_github_issue_message_contents() -> None:
    """Should include expected contents in github issue message when failed."""
    report = ValidationReport()
    report.add_issue(ValidationIssue(code="test", message="broken"))
    msg = report.github_issue_message
    assert "UTC" in msg
    assert "<details>" in msg
    assert "broken" in msg
