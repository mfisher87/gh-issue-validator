"""For end-to-end testing of this package."""

from gh_issue_validator.checks.headings import CheckMissingHeadings
from gh_issue_validator.validate import validate

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
