"""Generate a validation comment and post/update it on GitHub."""

from github.Issue import Issue
from github.IssueComment import IssueComment

from gh_issue_validator.report import ValidationReport

_BOT_COMMENT_HEADER = "### Validation history"
_BOT_COMMENT_SENTINEL = "<!-- gh-issue-validator -->"
_REPORT_START_SENTINEL = "<!-- report-start -->"


def _find_bot_comment(*, issue: Issue) -> IssueComment | None:
    """Find an existing bot comment, if any exists."""
    for comment in issue.get_comments():
        if _BOT_COMMENT_SENTINEL in comment.body:
            return comment

    return None


def _parse_comment_reports(*, comment_body: str) -> list[str]:
    """Extract a list of report entries from comment body.

    Each report is introduced with a sentinel value (as HTML comment).
    """
    # Skip the anything before the first sentinel value; we just want the reports, not
    # the header.
    parts = comment_body.split(_REPORT_START_SENTINEL)[1:]

    # Strip newlines from start and end of each report
    return [part.strip() for part in parts]


def _make_new_comment_body(
    *,
    existing_comment_body: str | None,
    report: ValidationReport,
) -> str:
    new_comment_reports = [report.github_issue_message]

    if existing_comment_body:
        old_comment_reports = _parse_comment_reports(comment_body=existing_comment_body)
        new_comment_reports.extend(old_comment_reports)

    # Prepend sentinel value to each report, and limit to 10 reports
    new_comment_reports = [
        f"{_REPORT_START_SENTINEL}\n{report}" for report in new_comment_reports[:10]
    ]

    return "\n".join(
        [
            _BOT_COMMENT_SENTINEL,
            _BOT_COMMENT_HEADER,
            "",
            "\n\n".join(new_comment_reports),
            "",
        ]
    )


def post_or_update_github_comment(
    *,
    issue: Issue,
    report: ValidationReport,
) -> None:
    """Post a new validation comment or update the existing one.

    Keeps the last 10 reports.
    """
    existing_comment = _find_bot_comment(issue=issue)

    new_comment_body = _make_new_comment_body(
        existing_comment_body=existing_comment.body if existing_comment else None,
        report=report,
    )

    if existing_comment is None:
        issue.create_comment(new_comment_body)
        print(f"ℹ️ Created new comment in {issue.html_url}")  # noqa: RUF001
    else:
        existing_comment.edit(new_comment_body)
        print(f"ℹ️ Updated comment in {issue.html_url}")  # noqa: RUF001


def apply_error_label(
    *,
    issue: Issue,
    report: ValidationReport,
    error_label: str,
) -> None:
    """Ensure error label present on failure, absent on success."""
    issue_label_names = [label.name for label in issue.labels]
    has_error_label = error_label in issue_label_names

    if report.is_failure and not has_error_label:
        issue.add_to_labels(error_label)
        print(f"ℹ️ Added label '{error_label}' to {issue.html_url}")  # noqa: RUF001
    elif not report.is_failure and has_error_label:
        issue.remove_from_labels(error_label)
        print(f"ℹ️ Removed label '{error_label}' from {issue.html_url}")  # noqa: RUF001
