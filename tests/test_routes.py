from flask.testing import FlaskClient


def test_index(client: FlaskClient) -> None:
    res = client.get("/")

    assert "Holiday Chat Bot" in res.text
