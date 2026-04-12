"""Tests for the github.py module."""

import pytest

from gh_issue_validator.github import (
    _BOT_COMMENT_SENTINEL,
    _REPORT_START_SENTINEL,
    _make_new_comment_body,
    _parse_comment_reports,
)
from gh_issue_validator.report import ValidationReport


class TestParseCommentReports:
    @pytest.mark.parametrize(
        ("comment_body", "expected"),
        [
            pytest.param("", [], id="empty string"),
            pytest.param("some header\n\nno reports here", [], id="no sentinel"),
            pytest.param(
                f"{_REPORT_START_SENTINEL}\nreport content",
                ["report content"],
                id="single report",
            ),
            pytest.param(
                f"{_REPORT_START_SENTINEL}\nfirst\n\n{_REPORT_START_SENTINEL}\nsecond",
                ["first", "second"],
                id="multiple reports in order",
            ),
            pytest.param(
                f"{_REPORT_START_SENTINEL}\n\n  report content  \n\n",
                ["report content"],
                id="whitespace stripped",
            ),
        ],
    )
    def test_parse_comment_reports(
        self,
        comment_body: str,
        expected: list[str],
    ) -> None:
        """Should extract report entries from the comment body."""
        actual = _parse_comment_reports(comment_body=comment_body)
        assert actual == expected


class TestMakeNewCommentBody:
    def test_make_new_comment_body_no_existing_contents(self) -> None:
        """Should include the bot comment sentinel when there is no existing comment."""
        report = ValidationReport()

        body = _make_new_comment_body(existing_comment_body=None, report=report)

        assert _BOT_COMMENT_SENTINEL in body
        assert report.github_issue_message in body

    def test_make_new_comment_body_with_existing_prepends_new_report(self) -> None:
        """Should place the new report before existing reports."""
        old_body = f"{_REPORT_START_SENTINEL}\nold report"
        report = ValidationReport()

        body = _make_new_comment_body(existing_comment_body=old_body, report=report)
        new_reports = _parse_comment_reports(comment_body=body)

        assert new_reports[0] == report.github_issue_message
        assert new_reports[1] == "old report"

    def test_make_new_comment_body_caps_at_ten_reports(self) -> None:
        """Should keep at most 10 reports."""
        expected_num_reports = 10
        num_reports = 12
        old_body = "\n\n".join(
            f"{_REPORT_START_SENTINEL}\nreport {i}" for i in range(num_reports)
        )

        body = _make_new_comment_body(
            existing_comment_body=old_body,
            report=ValidationReport(),
        )

        assert len(_parse_comment_reports(comment_body=body)) == expected_num_reports
