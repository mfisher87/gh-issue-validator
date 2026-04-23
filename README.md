# `gh-issue-validator`

`gh-issue-validator` is a customizable "linter" for issues in a GitHub repository.
It ensures issues conform to a specified format.

When an issue doesn't conform to the desired format, a bot will post a comment including
all errors found.


## Installation

You typically wouldn't install this package on your local machine.
It expects to be used in GitHub Actions.


## Usage

`gh-issue-validator` allows you to use first-party checks or custom checks.
The following example uses some of the included first-party checks:


```python
from gh_issue_validator import validate
from gh_issue_validator.checks.headings import CheckMissingHeadings, HeadingRequirement

HEADING_REQUIREMENTS =[
    {"heading": "Problem statement", "min_words": 10},
    {"heading": "Proposed solution", "min_words": 5, "max_words": 100},
]

validate(checks=[
    CheckMissingHeadings(requirements=HEADING_REQUIREMENTS),
    CheckWordCount(requirements=HEADING_REQUIREMENTS),
])
```

If the file above lives at `.github/issue_validator.py`, you can write a GitHub Actions
workflow like so to run it:

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

Check out our
[quickstart documentation](https://gh-issue-validator.readthedocs.io/en/latest/user-guide/quickstart/)
for full usage instructions, including defining custom checks!

See the [API documentation](https://gh-issue-validator.readthedocs.io/en/latest/api/)
for full descriptions of the toolkit.


## Development

Please see our
[contributor guide](https://gh-issue-validator.readthedocs.io/en/latest/contributor-guide/)
to get started with development.


## Acknowledgement

This validator is inspired by the <https://github.com/2i2c-org/initiatives> project.
