"""Checks related to expectations about headings and content within them."""

import typing
from itertools import pairwise
from typing import NotRequired, TypedDict

import nltk

from gh_issue_validator.checks._base import ValidationCheck
from gh_issue_validator.markdown import _render_tokens_as_md
from gh_issue_validator.report import ValidationIssue, ValidationReport
from gh_issue_validator.types import SegmentsMap


class HeadingRequirement(TypedDict):
    """Specification of expectations for a heading and its contents."""

    heading: str
    min_words: NotRequired[int]
    max_words: NotRequired[int]


class CheckMissingHeadings(ValidationCheck):
    """Validate that expected headings are present."""

    def __init__(self, *, requirements: list[HeadingRequirement]) -> None:
        self._requirements = requirements

    @typing.override
    def check(self, segments: SegmentsMap, report: ValidationReport) -> None:
        for req in self._requirements:
            if req["heading"] in segments:
                continue
            report.add_issue(
                ValidationIssue(
                    code="missing-heading",
                    message=f"Missing required heading: '{req['heading']}'",
                    heading=req["heading"],
                )
            )


class CheckUnexpectedHeadings(ValidationCheck):
    """Validate that no unexpected headings are present."""

    def __init__(
        self,
        *,
        requirements: list[HeadingRequirement],
        freeform_headings: list[str] | None = None,
    ) -> None:
        self._allowed_headings = [req["heading"] for req in requirements] + (
            freeform_headings or []
        )

    @typing.override
    def check(self, *, segments: SegmentsMap, report: ValidationReport) -> None:
        for heading in segments:
            if heading in self._allowed_headings:
                continue
            report.add_issue(
                ValidationIssue(
                    code="unexpected-heading",
                    message=f"Unexpected heading: '{heading}'",
                    heading=heading,
                )
            )


class CheckDisorderedHeadings(ValidationCheck):
    """Validate that headings appear in the expected order."""

    def __init__(
        self,
        *,
        requirements: list[HeadingRequirement],
        freeform_headings: list[str] | None = None,
    ) -> None:
        self._expected_order = [req["heading"] for req in requirements] + (
            freeform_headings or []
        )

    @typing.override
    def check(self, *, segments: SegmentsMap, report: ValidationReport) -> None:
        expected_index = {
            heading: index for index, heading in enumerate(self._expected_order)
        }
        actual_headings = [
            heading for heading in segments if heading in self._expected_order
        ]

        for current_heading, next_heading in pairwise(actual_headings):
            if expected_index[current_heading] <= expected_index[next_heading]:
                continue

            report.add_issue(
                ValidationIssue(
                    code="disordered-header",
                    message=(
                        f"Heading '{next_heading}' should appear before"
                        f" '{current_heading}'"
                    ),
                )
            )


class CheckWordCount(ValidationCheck):
    """Check that each heading has the expected number of words."""

    def __init__(self, *, requirements: list[HeadingRequirement]) -> None:
        nltk.download("punkt_tab", quiet=True)
        self._requirements = requirements

    @typing.override
    def check(self, segments: SegmentsMap, report: ValidationReport) -> None:
        for req in self._requirements:
            heading = req["heading"]
            if heading not in segments:
                continue

            content = _render_tokens_as_md(segments[heading]).strip()
            word_count = len(nltk.word_tokenize(content.lower()))

            min_words = req.get("min_words", 0)
            if word_count < min_words:
                report.add_issue(
                    ValidationIssue(
                        code="incomplete-info",
                        message=(
                            f"Heading '{heading}' requires at least {min_words} words,"
                            f" found {word_count} words"
                        ),
                        heading=heading,
                    )
                )

            max_words = req.get("max_words")
            if max_words is not None and word_count > max_words:
                report.add_issue(
                    ValidationIssue(
                        code="too-much-info",
                        message=(
                            f"Heading '{heading}' requires at most {max_words} words,"
                            f" found {word_count} words"
                        ),
                        heading=heading,
                    )
                )
