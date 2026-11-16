import base64

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


def encode_cursor(last_id: int) -> str:
    return base64.urlsafe_b64encode(f"id:{last_id}".encode()).decode()


def decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    try:
        raw = base64.urlsafe_b64decode(cursor.encode()).decode()
        prefix, value = raw.split(":", 1)
        if prefix != "id":
            raise ValueError
        return int(value)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("invalid cursor") from exc


def clamp_limit(limit: int) -> int:
    return max(1, min(limit, MAX_LIMIT))
