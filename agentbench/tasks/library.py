"""The reference ("correct") source of the `toolkit` library that every benchmark
task repo is built from. Each task injects exactly one bug (or none, for
invalid-issue tasks) into a copy of this library.

Keep this code boring and correct: the hidden test-suite in `suite.py` must pass
against it unmodified (the generator asserts this).
"""

FILES: dict[str, str] = {}

FILES["toolkit/__init__.py"] = '''"""toolkit: a small utility library used as a benchmark target."""
'''

FILES["toolkit/stats.py"] = '''"""Basic descriptive statistics."""


def mean(values):
    if not values:
        raise ValueError("mean() of empty sequence")
    return sum(values) / len(values)


def median(values):
    if not values:
        raise ValueError("median() of empty sequence")
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def mode(values):
    """Most common value; ties are broken by first occurrence."""
    if not values:
        raise ValueError("mode() of empty sequence")
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    best = values[0]
    for v in values:
        if counts[v] > counts[best]:
            best = v
    return best


def variance(values, sample=True):
    n = len(values)
    if n < 2 and sample:
        raise ValueError("sample variance needs at least two values")
    if n == 0:
        raise ValueError("variance() of empty sequence")
    m = mean(values)
    total = sum((v - m) ** 2 for v in values)
    if sample:
        return total / (n - 1)
    return total / n


def percentile(values, p):
    """Nearest-rank percentile, p in [0, 100]."""
    if not values:
        raise ValueError("percentile() of empty sequence")
    if p < 0 or p > 100:
        raise ValueError("p must be between 0 and 100")
    ordered = sorted(values)
    if p == 0:
        return ordered[0]
    rank = -(-p * len(ordered) // 100)
    return ordered[int(rank) - 1]


def moving_average(values, window):
    if window <= 0:
        raise ValueError("window must be positive")
    out = []
    for i in range(len(values) - window + 1):
        out.append(sum(values[i:i + window]) / window)
    return out


def clamp(x, lo, hi):
    if lo > hi:
        raise ValueError("lo must be <= hi")
    return max(lo, min(x, hi))
'''

FILES["toolkit/text.py"] = '''"""String helpers."""
import re


def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def truncate(s, limit, suffix="..."):
    if limit < len(suffix):
        raise ValueError("limit too small for suffix")
    if len(s) <= limit:
        return s
    return s[:limit - len(suffix)] + suffix


def word_count(s):
    return len(s.split())


def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]


def title_case(s, minor=("a", "an", "the", "of", "and", "or", "in")):
    words = s.split()
    out = []
    for i, w in enumerate(words):
        if i > 0 and w.lower() in minor:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:].lower())
    return " ".join(out)


def count_vowels(s):
    return sum(1 for c in s.lower() if c in "aeiou")


def initials(name):
    parts = [p for p in name.split() if p]
    return "".join(p[0].upper() for p in parts)


def camel_to_snake(s):
    out = []
    for i, c in enumerate(s):
        if c.isupper() and i > 0:
            out.append("_")
        out.append(c.lower())
    return "".join(out)
'''

FILES["toolkit/seq.py"] = '''"""Sequence helpers."""


def chunk(items, size):
    if size <= 0:
        raise ValueError("size must be positive")
    return [items[i:i + size] for i in range(0, len(items), size)]


def flatten(nested):
    out = []
    for item in nested:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def dedupe(items):
    """Remove duplicates, preserving first-seen order."""
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def rotate(items, k):
    """Rotate right by k positions."""
    if not items:
        return []
    k = k % len(items)
    return items[-k:] + items[:-k]


def sliding_window(items, size):
    if size <= 0:
        raise ValueError("size must be positive")
    return [tuple(items[i:i + size]) for i in range(len(items) - size + 1)]


def binary_search(items, target):
    """Index of target in sorted items, or -1."""
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def merge_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def last_n(items, n):
    if n <= 0:
        return []
    return items[-n:]
'''

FILES["toolkit/money.py"] = '''"""Money helpers. Amounts are floats rounded to cents."""


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
    r = rate / periods_per_year
    n = periods_per_year * years
    return round(principal * (1 + r) ** n, 2)


def format_currency(amount, symbol="$"):
    sign = "-" if amount < 0 else ""
    return f"{sign}{symbol}{abs(amount):,.2f}"


def tax(amount, rate):
    if rate < 0:
        raise ValueError("rate must be non-negative")
    return round(amount * rate, 2)
'''

FILES["toolkit/dates.py"] = '''"""Calendar helpers (no datetime dependency)."""


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


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
'''

FILES["toolkit/report.py"] = '''"""Higher-level report helpers built on the other modules."""
from toolkit import stats, text, seq, money


def summarize(values):
    return {
        "count": len(values),
        "mean": round(stats.mean(values), 2),
        "median": stats.median(values),
        "max": max(values),
    }


def top_words(s, n):
    words = [w.lower() for w in s.split()]
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    ranked = sorted(counts, key=lambda w: (-counts[w], w))
    return ranked[:n]


def invoice_total(lines, discount_percent=0, tax_rate=0):
    subtotal = sum(qty * price for qty, price in lines)
    discounted = money.apply_discount(subtotal, discount_percent)
    return round(discounted + money.tax(discounted, tax_rate), 2)


def headline(title, limit=20):
    return text.truncate(text.title_case(title), limit)


def pages(items, per_page):
    return len(seq.chunk(items, per_page))
'''

PACKAGE = "toolkit"
