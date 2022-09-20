__all__ = ["create_app"]

import os
from flask import Flask
from app.routes import bp


def create_app(test_config: dict[str, str] | None = None) -> Flask:
    """
    This is a Flask App factory.
    It will create, configure, and return a Flask Application
    """

    app = Flask(
        __name__,
        instance_relative_config=True
    )  # Creating the application to look relative to the file

    if test_config is not None:
        app.config.from_mapping(test_config)  # Configuring the app for testing

    if not os.path.exists(app.instance_path):
        os.mkdir(app.instance_path)

    app.register_blueprint(bp)

    return app
