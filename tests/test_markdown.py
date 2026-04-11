"""Tests for the markdown.py module."""

import pytest

from gh_issue_validator.markdown import _parse_segments


class TestParseSegments:
    @pytest.mark.parametrize(
        ("markdown_input", "expected_heading_keys"),
        [
            pytest.param("", [], id="empty string"),
            pytest.param(
                "### Problem statement\n\nsome content here",
                ["Problem statement"],
                id="single h3",
            ),
            pytest.param(
                "### Problem statement\n\ncontent\n\n### Proposed solution\n\ncontent",
                ["Problem statement", "Proposed solution"],
                id="two h3 sections",
            ),
            pytest.param(
                "preamble content\n\n### Problem statement\n\ncontent",
                ["Problem statement"],
                id="content before first h3 ignored",
            ),
            pytest.param(
                "## Title\n\n### Problem statement\n\ncontent",
                ["Problem statement"],
                id="h2 not a segment",
            ),
            pytest.param(
                "### Problem statement\n\n#### Sub-point\n\ncontent",
                ["Problem statement"],
                id="h4 not a segment",
            ),
        ],
    )
    def test_parse_segments_returns_expected_headings(
        self,
        markdown_input: str,
        expected_heading_keys: list[str],
    ) -> None:
        """Should parse H3 headings as segment keys in document order."""
        segments = _parse_segments(markdown_input)
        assert list(segments.keys()) == expected_heading_keys

    def test_parse_segments_section_content_is_not_empty(self) -> None:
        """Should populate each segment with its content tokens."""
        markdown_input = "### Problem statement\n\nThis is the content."
        segments = _parse_segments(markdown_input)
        assert "Problem statement" in segments
        assert len(segments["Problem statement"]) > 0
