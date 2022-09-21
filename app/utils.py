__all__ = ["is_positive_message", "lower_if_str"]


def is_positive_message(msg: str) -> bool:
    return True


def lower_if_str(value: str | int) -> str | int:
    if isinstance(value, int):
        return value
    return value.lower()
