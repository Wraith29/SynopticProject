from flask import Flask
from flask.testing import FlaskClient
from pytest import fixture
from app import create_app
from app.bot import Bot


@fixture
def app() -> Flask:
    app = create_app()  # Creating an application to test
    app.config.update({"TESTING": True})  # Updating the configuration

    yield app


@fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@fixture
def bot() -> Bot:
    return Bot()
