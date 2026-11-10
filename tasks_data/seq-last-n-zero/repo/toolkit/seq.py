"""Sequence helpers."""


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
    if n < 0:
        return []
    return items[-n:]
