"""Calendar helpers (no datetime dependency)."""


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 != 0)


def days_in_month(year, month):
    if month < 1 or month > 12:
        raise ValueError("month must be 1..12")
    if month == 2:
        return 29 if is_leap_year(year) else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


def quarter_of(month):
    if month < 1 or month > 12:
        raise ValueError("month must be 1..12")
    return (month - 1) // 3 + 1


def day_of_year(year, month, day):
    if day < 1 or day > days_in_month(year, month):
        raise ValueError("invalid day")
    total = 0
    for m in range(1, month):
        total += days_in_month(year, m)
    return total + day
