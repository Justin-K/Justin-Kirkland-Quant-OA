from datetime import datetime, timedelta, date


def get_start_of_week(date: datetime, week_starts_on_monday=True):
    start: int = date.weekday() if week_starts_on_monday else date.weekday() + 1
    return date - timedelta(days=start)


if __name__ == "__main__":
    pass
