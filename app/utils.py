from datetime import datetime, timedelta
from typing import Any

def calculate_next_review(level: int) -> datetime:
    today = datetime.now()

    intervals = {
        0: 1,
        1: 3,
        2: 5,
        3: 7,
        4: 10,
        5: 14
    }

    days = intervals.get(level, 30)
    return today + timedelta(days=days)

def safe_csv(value: Any) -> str:
    if value is None:
        return ""
    s = str(value)
    s = s.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    s = s.strip()
    if s and s[0] in ("=", "+", "-", "@"):
        s = "'" + s
    return s