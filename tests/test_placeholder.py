"""Placeholder test to ensure pre-commit works correctly."""


def test_placeholder() -> None:
    """Placeholder test that always passes.

    This test ensures that:
    1. pytest runs successfully in pre-commit
    2. TDD principles are maintained even with automatic formatting
    3. The test suite has at least one test to run

    This test should be replaced with actual tests as the project develops.
    """
    assert True, "This is a placeholder test that always passes"


def test_python_version() -> None:
    """Verify we're running on Python 3.12+."""
    import sys

    assert sys.version_info >= (3, 12), f"Python 3.12+ required, got {sys.version_info}"
