"""Flask web app for Gesture Piano."""

from flask import Flask, render_template


def create_app(config=None):
    """Builds the flask app. Pass a `config` to override the settings for the tests."""
    app = Flask(__name__)
    if config:
        app.config.update(config)

    @app.route("/")
    def play():
        """Play page."""
        return render_template("play.html")

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
