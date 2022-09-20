from app import create_app


def test_config() -> None:
    """
    This is a simple test to ensure that the configuration is correctly set
    """
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
