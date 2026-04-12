"""For end-to-end testing of this package."""

from gh_issue_validator import validate
from gh_issue_validator.checks.headings import CheckMissingHeadings

validate(
    checks=[
        CheckMissingHeadings(
            requirements=[
                {"heading": "Problem statement", "min_words": 5},
                {"heading": "Proposed solution", "min_words": 5},
            ]
        ),
    ]
)
