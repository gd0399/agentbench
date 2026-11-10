"""String helpers."""
import re


def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z]+", "-", s)
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
