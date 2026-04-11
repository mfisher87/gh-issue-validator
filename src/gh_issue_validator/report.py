"""Report on issues found during validation."""

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class ValidationIssue:
    """An issue found during validation."""

    code: str
    message: str
    heading: str | None = None

    @property
    def rich_message(self) -> str:
        """Return a message with a bit of style."""
        return f"❌ {self.message}"


@dataclass
class ValidationReport:
    """A report of all issues found during validation."""

    issues: list[ValidationIssue] = field(default_factory=list)

    def add_issue(self, issue: ValidationIssue) -> None:
        """Add an issue to the report."""
        self.issues.append(issue)

    @property
    def is_failure(self) -> bool:
        """Return True if validation found any issues."""
        return len(self.issues) > 0

    @property
    def _summary_message(self) -> str:
        """Return message summarizing failures."""
        if self.is_failure:
            return f"😭 Validation failed with {len(self.issues)} issues."
        return "😁 Validation successful!"

    @property
    def _errors_message(self) -> str:
        """Return message listing errors."""
        if not self.is_failure:
            return ""

        return "\n".join([f"- {issue.rich_message}" for issue in self.issues])

    @property
    def github_issue_message(self) -> str:
        """Return a message for posting on a GitHub issue."""
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        lines: list[str] = []

        lines.append(f"**{self._summary_message}** ({timestamp})")
        if self.is_failure:
            lines.append("<details>")
            lines.append("<summary>Errors</summary>")
            lines.append("")
            lines.append(self._errors_message)
            lines.append("")
            lines.append("</details>")

        return "\n".join(lines)

    def __str__(self) -> str:
        lines: list[str] = []

        lines.append(self._summary_message)
        if self.is_failure:
            lines.append("")
            lines.append(self._errors_message)

        return "\n".join(lines)
