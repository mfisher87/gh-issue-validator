# `gh-issue-validator`

`gh-issue-validator` is a customizable "linter" for issues in a GitHub repository.
It ensures issues conform to a specified format.


## Installation

You typically wouldn't install this package on your local machine.
It expects to be used in GitHub Actions.


## Usage

### Write your validation script

To get started, you'll need to write a validation script.
We suggest creating it at `.github/issue_validator.py`.

At the top of the script, include PEP723 metadata to enable automated installation of
dependencies.
At minimum, we'll need to add this project, `gh-issue-validator`, as a dependency.

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "gh-issue-validator",
# ]
# ///
import typing

from gh_issue_validator import ValidationCheck, ValidationIssue, ValidationReport, validate
from gh_issue_validator.checks.headings import CheckMissingHeadings, HeadingRequirement
from gh_issue_validator.types import SegmentsMap


# Optional: Create your own validator based on the ValidationCheck ABC.
class ProblemStatementQualityCheck(ValidationCheck):
    """Reject problem statements that are just a URL."""

    @typing.override
    def check(self, *, segments: SegmentsMap, report: ValidationReport) -> None:
        heading_to_check = "Problem statement"
        content = segments.get(heading_to_check, [])
        if not content:
            return  # Empty content is handled by first-party CheckWordCount check.

        text = str(content).strip()
        if text.startswith("http") and " " not in text:
            # Our custom "issue" to report:
            report.add_issue(ValidationIssue(
                code="problem-statement-is-url",
                message="Problem statement should be a description, not just a URL.",
                heading=heading_to_check,
            ))

HEADING_REQUIREMENTS =[
    {"heading": "Problem statement", "min_words": 10},
    {"heading": "Proposed solution", "min_words": 5, "max_words": 100},
]

validate(checks=[
    CheckMissingHeadings(requirements=HEADING_REQUIREMENTS),
    CheckWordCount(requirements=HEADING_REQUIREMENTS),
    ProblemStatementQualityCheck(),
])
```


### Call it from GitHub Actions

```yaml
on:
  issues:
    types:
      - "opened"
      - "edited"
      - "labeled"
      - "unlabeled"

jobs:
  validate:
    # Filter for only issues labeled as "initiative"
    if: "contains(github.event.issue.labels.*.name, 'initiative')"
    runs-on: "ubuntu-latest"
    permissions:
      issues: "write"
    steps:
      - uses: "actions/checkout@v4"
      - uses: "astral-sh/setup-uv@v5"
      - run: "uv run .github/issue_validator.py"
        env:
          GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}"
          GITHUB_ISSUE_NUMBER: "${{ github.event.issue.number }}"
```


## Development

Tools: [uv](https://github.com/astral-sh/uv), [prek](https://prek.j178.dev/)


### Get started

```bash
uv sync
prek install
```


### Run tests

```bash
prek run -a
uv run mypy
uv run pytest
```


## Acknowledgement

This validator is inspired by the <https://github.com/2i2c-org/initiatives> project.
