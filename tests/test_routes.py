from flask.testing import FlaskClient


def test_index_sends_base_html(client: FlaskClient) -> None:
    response = client.get("/")
    assert "<title>Holiday Chat Bot</title>" in response.text


def test_index_loads_home_html(client: FlaskClient) -> None:
    response = client.get("/")
    assert "<div class=\"root\">" in response.text
    assert "<h4>Bot</h4>" in response.text
    assert "<p>Welcome to the holiday chat bot!</p>" in response.text


def test_recieve_message_returns_json_obj(client: FlaskClient) -> None:
    response = client.post(
        "/recieve-message",
        json={"msg": "Hi"},
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    assert response.is_json
    assert response.json.get("msg") is not None


def test_reset_returns_str(client: FlaskClient) -> None:
    response = client.post(
        "/reset"
    )
    assert response.status_code == 200
    assert not response.is_json
    assert response.data == b"Bot Reset"
