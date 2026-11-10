"""Higher-level report helpers built on the other modules."""
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
