"""Tests for the checks/headings.py module."""

import pytest

from gh_issue_validator.checks.headings import (
    CheckDisorderedHeadings,
    CheckMissingHeadings,
    CheckUnexpectedHeadings,
    CheckWordCount,
    HeadingRequirement,
)
from gh_issue_validator.markdown import _parse_segments
from gh_issue_validator.report import ValidationReport

REQUIREMENTS: list[HeadingRequirement] = [
    {"heading": "Problem statement", "min_words": 3},
    {"heading": "Proposed solution", "min_words": 3, "max_words": 10},
]


class TestCheckMissingHeadings:
    @pytest.mark.parametrize(
        ("markdown_input", "expected_missing"),
        [
            pytest.param(
                "### Problem statement\n\none two three\n\n### Proposed solution\n\none two three",
                [],
                id="all required headings present",
            ),
            pytest.param(
                "",
                ["Problem statement", "Proposed solution"],
                id="all headings missing",
            ),
            pytest.param(
                "### Problem statement\n\none two three",
                ["Proposed solution"],
                id="one heading missing",
            ),
        ],
    )
    def test_missing_headings_check(
        self,
        markdown_input: str,
        expected_missing: list[str],
    ) -> None:
        """Should report missing-heading issues for required headings absent from the document."""
        check = CheckMissingHeadings(requirements=REQUIREMENTS)
        segments = _parse_segments(markdown_input)

        report = ValidationReport()
        check.check(segments=segments, report=report)

        missing = [i.heading for i in report.issues if i.code == "missing-heading"]
        assert sorted(missing) == sorted(expected_missing)


class TestCheckUnexpectedHeadings:
    @pytest.mark.parametrize(
        ("markdown_input", "expected_unexpected"),
        [
            pytest.param(
                "### Problem statement\n\ncontent\n\n### Proposed solution\n\ncontent",
                [],
                id="only required headings",
            ),
            pytest.param(
                "### Problem statement\n\ncontent\n\n### Random heading\n\ncontent",
                ["Random heading"],
                id="one unexpected heading",
            ),
            pytest.param(
                "### Problem statement\n\ncontent\n\n### Other information\n\ncontent",
                [],
                id="freeform heading not unexpected",
            ),
        ],
    )
    def test_unexpected_headings_check(
        self,
        markdown_input: str,
        expected_unexpected: list[str],
    ) -> None:
        """Should report unexpected-heading issues for headings not in requirements or freeform list."""
        check = CheckUnexpectedHeadings(
            requirements=REQUIREMENTS,
            freeform_headings=["Other information"],
        )
        segments = _parse_segments(markdown_input)

        report = ValidationReport()
        check.check(segments=segments, report=report)

        unexpected = [
            i.heading for i in report.issues if i.code == "unexpected-heading"
        ]
        assert sorted(unexpected) == sorted(expected_unexpected)


class TestDisorderedHeadingsCheck:
    @pytest.mark.parametrize(
        ("markdown_input", "expect_disordered"),
        [
            pytest.param(
                "### Problem statement\n\ncontent\n\n### Proposed solution\n\ncontent",
                False,
                id="correct order",
            ),
            pytest.param(
                "### Proposed solution\n\ncontent\n\n### Problem statement\n\ncontent",
                True,
                id="reversed order",
            ),
            pytest.param(
                "### Problem statement\n\ncontent",
                False,
                id="single heading always ordered",
            ),
            pytest.param(
                "### Problem statement\n\ncontent\n\n### Proposed solution\n\ncontent\n\n### Other information\n\ncontent",
                False,
                id="freeform heading after required headings",
            ),
            pytest.param(
                "### Other information\n\ncontent\n\n### Problem statement\n\ncontent",
                True,
                id="freeform heading before required heading",
            ),
        ],
    )
    def test_disordered_heading_check(
        self,
        markdown_input: str,
        expect_disordered: bool,
    ) -> None:
        """Should report disordered-header issues when headings appear out of expected order."""
        check = CheckDisorderedHeadings(
            requirements=REQUIREMENTS,
            freeform_headings=["Other information"],
        )
        segments = _parse_segments(markdown_input)

        report = ValidationReport()
        check.check(segments=segments, report=report)

        disordered_issues = [i for i in report.issues if i.code == "disordered-header"]
        assert bool(disordered_issues) == expect_disordered


class TestCheckWordCount:
    @pytest.mark.parametrize(
        ("markdown_input", "expected_codes"),
        [
            pytest.param(
                "### Problem statement\n\none two three four\n\n### Proposed solution\n\none two three four",
                [],
                id="both sections within word count bounds",
            ),
            pytest.param(
                "### Problem statement\n\none two",
                ["incomplete-info"],
                id="too few words",
            ),
            pytest.param(
                "### Problem statement\n\none two three\n\n### Proposed solution\n\n"
                + " ".join(["word"] * 11),
                ["too-much-info"],
                id="too many words",
            ),
            pytest.param(
                "### Problem statement\n\none two three",
                [],
                id="heading with no max_words requirement not flagged",
            ),
        ],
    )
    def test_word_count_check(
        self,
        markdown_input: str,
        expected_codes: list[str],
    ) -> None:
        """Should report incomplete-info or too-much-info issues when word counts are out of bounds."""
        check = CheckWordCount(requirements=REQUIREMENTS)
        segments = _parse_segments(markdown_input)

        report = ValidationReport()
        check.check(segments=segments, report=report)

        issue_codes = [i.code for i in report.issues]
        assert sorted(issue_codes) == sorted(expected_codes)
