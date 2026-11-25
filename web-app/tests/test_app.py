"""Tests for the web app."""

from app import create_app


def test_play_page_loads(client):
    """The play page renders."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data


def test_play_page_rejects_post(client):
    """The play page only allows GET."""
    response = client.post("/")
    assert response.status_code == 405


def test_unknown_page_is_404(client):
    """A path with no route returns 404."""
    response = client.get("/not-a-page")
    assert response.status_code == 404


def test_config_override():
    """Values passed to create_app end up in app.config."""
    app = create_app({"TESTING": True, "ML_CLIENT_URL": "http://test"})
    assert app.config["ML_CLIENT_URL"] == "http://test"


def test_no_config_uses_defaults():
    """Without a config, the app is not in testing mode."""
    assert create_app().config["TESTING"] is False
