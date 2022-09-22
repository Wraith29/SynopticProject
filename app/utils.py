__all__ = ["sanitise", "is_positive_message", "lower_if_str"]


def sanitise(msg: str) -> str:
    return msg.strip(" !@#$%^&*(){}:;/?>.<,£")


def is_positive_message(msg: str, positive_messages: list[str]) -> bool:
    return sanitise(msg) in positive_messages


def lower_if_str(value: str | int) -> str | int:
    if isinstance(value, int):
        return value
    return value.lower()
