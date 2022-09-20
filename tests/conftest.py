from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from pytest import fixture
from app import create_app


@fixture
def app() -> Flask:
    app = create_app()  # Creating an application to test
    app.config.update({"TESTING": True})  # Updating the configuration

    yield app


@fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
