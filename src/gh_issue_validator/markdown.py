"""Parse markdown."""

from collections.abc import Iterable

from mistletoe.block_token import Document, Heading
from mistletoe.markdown_renderer import MarkdownRenderer
from mistletoe.token import Token

from gh_issue_validator.types import SegmentsMap

# Using header level 3 because that's what GitHub issues use when the user fills out an
# issue template form.
HEADER_LEVEL = 3


def _parse_segments(markdown: str) -> SegmentsMap:
    """Parse `markdown` into segments separated by H3 headings.

    Returns:
        A dictionary where keys are H3 heading text and values are the token lists for
        each heading's content, in document order.

    """
    doc = Document(markdown)
    if not doc.children:
        return {}

    document_segments: SegmentsMap = {}
    current_segment_header: str | None = None
    current_segment_content: list[Token] = []

    for child in doc.children:
        is_h3 = isinstance(child, Heading) and child.level == HEADER_LEVEL

        if is_h3:
            if current_segment_header is not None:
                # TODO: Confusing! Adding content from previous iteration?
                document_segments[current_segment_header] = current_segment_content
            current_segment_header = _render_tokens_as_md(child.children).strip()
            current_segment_content = []
        else:
            current_segment_content.append(child)

    # Add the last segment
    # TODO: Confusing! Adding content after the end of the loop...
    if current_segment_header is not None:
        # TODO: Can we refactor to remove this typeguard
        document_segments[current_segment_header] = current_segment_content

    return document_segments


def _render_tokens_as_md(tokens: Iterable[Token] | None) -> str:
    """Render a sequence of tokens back to markdown text."""
    if not tokens:
        return ""
    with MarkdownRenderer() as renderer:
        return "".join([renderer.render(c) for c in tokens])
