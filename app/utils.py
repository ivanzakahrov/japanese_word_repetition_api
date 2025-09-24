from datetime import datetime, timedelta

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