"""Tests that validate that the main package API hasn't unintentionally changed."""

import pytest

pytestmark = pytest.mark.public_api_test


def test_api() -> None:
    """Test that the public API hasn't changed."""
    from gh_issue_validator import validate  # noqa: F401, PLC0415
