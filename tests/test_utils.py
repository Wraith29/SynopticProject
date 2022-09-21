from app.utils import is_positive_message, lower_if_str

_positive_messages = [
    "yes", "yep", "yeah"
]


def test_is_positive_message_strips_unwanted_chars() -> None:
    msg = "   !!£%&@@@yes*(&($*&%*$"
    assert is_positive_message(msg, _positive_messages)


def test_is_positive_message_cant_read_split_word() -> None:
    msg = " y e s "
    assert not is_positive_message(msg, _positive_messages)


def test_lower_if_str_lowers_str() -> None:
    msg = "HELLO"
    assert lower_if_str(msg) == "hello"


def test_lower_if_str_returns_int() -> None:
    msg = 1
    assert lower_if_str(msg) == 1
