"""Basic descriptive statistics."""


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
    rank = p * len(ordered) // 100
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
