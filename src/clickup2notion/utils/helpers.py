from datetime import UTC
from datetime import datetime


def split_text(text, max_length=2000):
    if not text:
        return [""]
    return [text[i : i + max_length] for i in range(0, len(text), max_length)]


def timestamp_to_ISO8601(timestamp_ms: int | str) -> str:
    dt = datetime.fromtimestamp(int(timestamp_ms) / 1000, UTC)
    return dt.isoformat()
