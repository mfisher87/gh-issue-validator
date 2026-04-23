"""Validate a GitHub issue aligns with specified standards."""

import os
import sys

from github import Auth, Github

from gh_issue_validator.checks._base import ValidationCheck, Validator
from gh_issue_validator.github import apply_error_label, post_or_update_github_comment


def validate(
    *,
    checks: list[ValidationCheck],
    error_label: str = "validation error",
    post_comment: bool = True,
) -> None:
    """Validate a GitHub issue and apply labels/comments.

    Reads `GITHUB_TOKEN`, `GITHUB_REPOSITORY`, and `GITHUB_ISSUE_NUMBER` from the
    environment.
    Exits with return code 1 if validation fails.
    """
    early_fail: bool = False
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN is not set.", file=sys.stderr)
        early_fail = True

    repo_name = os.environ.get("GITHUB_REPOSITORY")
    if not repo_name:
        print("Error: GITHUB_REPOSITORY is not set.", file=sys.stderr)
        early_fail = True

    issue_number = os.environ.get("GITHUB_ISSUE_NUMBER")
    if not issue_number:
        print("Error: GITHUB_ISSUE_NUMBER is not set.", file=sys.stderr)
        early_fail = True

    if early_fail:
        sys.exit(1)

    if not (github_token and repo_name and issue_number):
        # Typeguard -- mypy can't tell that this is unreachable
        raise RuntimeError("Programmer error.")  # noqa: EM101, TRY003

    github = Github(auth=Auth.Token(github_token))
    issue = github.get_repo(repo_name).get_issue(int(issue_number))

    report = Validator(checks=checks).validate(markdown=issue.body or "")

    print()
    print(report)
    print()

    if post_comment:
        post_or_update_github_comment(issue=issue, report=report)

    apply_error_label(issue=issue, report=report, error_label=error_label)

    if report.is_failure:
        sys.exit(1)
