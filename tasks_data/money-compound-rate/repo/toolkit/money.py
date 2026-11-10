"""Money helpers. Amounts are floats rounded to cents."""


def apply_discount(price, percent):
    if percent < 0 or percent > 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)


def split_bill(total, people, tip_percent=0):
    if people <= 0:
        raise ValueError("people must be positive")
    with_tip = total * (1 + tip_percent / 100)
    return round(with_tip / people, 2)


def compound_interest(principal, rate, years, periods_per_year=1):
    if years < 0:
        raise ValueError("years must be non-negative")
    r = rate
    n = periods_per_year * years
    return round(principal * (1 + r) ** n, 2)


def format_currency(amount, symbol="$"):
    sign = "-" if amount < 0 else ""
    return f"{sign}{symbol}{abs(amount):,.2f}"


def tax(amount, rate):
    if rate < 0:
        raise ValueError("rate must be non-negative")
    return round(amount * rate, 2)
