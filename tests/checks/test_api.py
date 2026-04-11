"""Tests that validate that the checks subpackage API hasn't unintentionally changed."""

import pytest

pytestmark = pytest.mark.public_api_test


def test_api() -> None:
    """Test that the public API hasn't changed."""
    from gh_issue_validator.checks import (  # noqa: F401, PLC0415
        ValidationCheck,
        Validator,
    )
