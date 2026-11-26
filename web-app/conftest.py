"""pytest-flask uses the `app` fixture to give tests a client."""

import pytest

from app import create_app


@pytest.fixture
def app():
    """App set up for testing."""
    return create_app({"TESTING": True})
