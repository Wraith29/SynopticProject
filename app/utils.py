__all__ = ["sanitise"]


def remove_punctuation(msg: str) -> str:
    out = ""
    for c in msg:
        if c not in ['!', '?', '_']:
            out += c

    return out


def sanitise(msg: str) -> str:
    msg = msg.lower()
    msg = msg.strip()

    msg = remove_punctuation(msg)

    return msg
