"""Catalogue of benchmark issues.

Each entry injects one source change into the reference library and carries
the reproduction a user would paste into a GitHub issue. The generator
computes the *actual* (buggy) behaviour itself, so issue text is always true.

kind="bug"     -> a real defect; success = hidden suite passes + PR opened.
kind="invalid" -> the reporter is wrong (code is correct and documented);
                  success = agent closes the issue without changing source.
"""
from dataclasses import dataclass, field


@dataclass
class Spec:
    id: str
    file: str            # file containing the defect (ground truth for localization)
    old: str             # exact snippet in the reference source ('' for invalid)
    new: str             # replacement that introduces the bug
    expr: str            # reproduction expression, evaluated with `from toolkit import *modules*`
    expected: str        # python literal the reporter expects, or "raise ValueError"
    title: str
    category: str        # off-by-one | operator | logic | edge-case | arithmetic | format | cross-module | hang | invalid
    kind: str = "bug"
    note: str = ""       # extra issue prose
    tags: list = field(default_factory=list)


S = Spec
BUGS: list[Spec] = [
    # ------------------------------------------------------------------ stats
    S("stats-mean-denominator", "toolkit/stats.py", "return sum(values) / len(values)", "return sum(values) / (len(values) - 1)",
      "stats.mean([1, 2, 3, 4])", "2.5", "mean() gives the wrong average", "arithmetic"),
    S("stats-median-even-window", "toolkit/stats.py", "(ordered[mid - 1] + ordered[mid]) / 2", "(ordered[mid] + ordered[mid + 1]) / 2",
      "report.summarize([1, 2, 3, 4])", "{'count': 4, 'mean': 2.5, 'median': 2.5, 'max': 4}",
      "summarize() reports the wrong median for even-length data", "cross-module"),
    S("stats-median-parity", "toolkit/stats.py", "if n % 2 == 1:", "if n % 2 == 0:",
      "stats.median([3, 1, 2])", "2", "median of odd-length list is wrong", "operator"),
    S("stats-median-float-index", "toolkit/stats.py", "mid = n // 2", "mid = n / 2",
      "stats.median([3, 1, 2])", "2", "median() crashes with TypeError", "arithmetic"),
    S("stats-mode-counting", "toolkit/stats.py", "counts[v] = counts.get(v, 0) + 1", "counts[v] = counts.get(v, 1)",
      "stats.mode([1, 2, 2, 3])", "2", "mode() always returns the first element", "logic"),
    S("stats-variance-population", "toolkit/stats.py", "return total / (n - 1)", "return total / n",
      "stats.variance([2, 4, 4, 4, 5, 5, 7, 9])", "4.571428571428571", "sample variance uses the population formula", "arithmetic"),
    S("stats-variance-guard", "toolkit/stats.py", "if n < 2 and sample:", "if n < 2 or sample:",
      "stats.variance([1, 2, 3])", "1.0", "variance() raises for perfectly valid input", "logic"),
    S("stats-percentile-ceil", "toolkit/stats.py", "rank = -(-p * len(ordered) // 100)", "rank = p * len(ordered) // 100",
      "stats.percentile([15, 20, 35, 40, 50], 30)", "20", "percentile() rounds the rank down instead of up", "arithmetic"),
    S("stats-percentile-bound", "toolkit/stats.py", "if p < 0 or p > 100:", "if p < 0 or p >= 100:",
      "stats.percentile([1, 2, 3], 100)", "3", "percentile(…, 100) raises ValueError", "edge-case"),
    S("stats-percentile-index", "toolkit/stats.py", "return ordered[int(rank) - 1]", "return ordered[int(rank)]",
      "stats.percentile([15, 20, 35, 40, 50], 40)", "20", "percentile() is off by one", "off-by-one"),
    S("stats-moving-average-range", "toolkit/stats.py", "range(len(values) - window + 1)", "range(len(values) - window)",
      "stats.moving_average([2, 4, 6], 3)", "[4.0]", "moving_average drops the last window", "off-by-one"),
    S("stats-moving-average-zero", "toolkit/stats.py", "if window <= 0:", "if window < 0:",
      "stats.moving_average([1, 2], 0)", "raise ValueError", "moving_average(window=0) raises ZeroDivisionError instead of ValueError", "edge-case"),
    S("stats-clamp-swapped", "toolkit/stats.py", "return max(lo, min(x, hi))", "return min(lo, max(x, hi))",
      "stats.clamp(5, 0, 10)", "5", "clamp() returns the lower bound for in-range values", "logic"),
    S("stats-clamp-equal-bounds", "toolkit/stats.py", "if lo > hi:", "if lo >= hi:",
      "stats.clamp(3, 3, 3)", "3", "clamp() rejects lo == hi", "edge-case"),
    # ------------------------------------------------------------------- text
    S("text-slugify-trailing-dash", "toolkit/text.py", 'return s.strip("-")', "return s",
      "text.slugify('  Hello, World! ')", "'hello-world'", "slugify leaves a trailing dash", "edge-case"),
    S("text-slugify-digits", "toolkit/text.py", 'r"[^a-z0-9]+"', 'r"[^a-z]+"',
      "text.slugify('Top 10 Tips')", "'top-10-tips'", "slugify strips numbers", "logic"),
    S("text-truncate-exact", "toolkit/text.py", "if len(s) <= limit:", "if len(s) < limit:",
      "text.truncate('hello', 5)", "'hello'", "truncate() shortens strings that already fit", "off-by-one"),
    S("text-truncate-suffix-room", "toolkit/text.py", "s[:limit - len(suffix)]", "s[:limit]",
      "report.headline('the art of war', 12)", "'The Art o...'", "headline() is longer than the limit", "cross-module"),
    S("text-word-count-split", "toolkit/text.py", "len(s.split())", 'len(s.split(" "))',
      "text.word_count('  the quick  brown fox ')", "4", "word_count counts extra words with repeated spaces", "logic"),
    S("text-palindrome-case", "toolkit/text.py", "c.lower() for c in s if c.isalnum()", "c for c in s if c.isalnum()",
      "text.is_palindrome('Racecar')", "True", "is_palindrome is case-sensitive", "logic"),
    S("text-title-case-first-word", "toolkit/text.py", "if i > 0 and w.lower() in minor:", "if w.lower() in minor:",
      "text.title_case('the lord of the rings')", "'The Lord of the Rings'", "title_case lowercases the first word", "logic"),
    S("text-title-case-rest-lower", "toolkit/text.py", "w[:1].upper() + w[1:].lower()", "w[:1].upper() + w[1:]",
      "text.title_case('hELLO wORLD')", "'Hello World'", "title_case keeps stray capitals", "logic"),
    S("text-vowels-missing-u", "toolkit/text.py", 'c in "aeiou"', 'c in "aeio"',
      "text.count_vowels('Education')", "5", "count_vowels misses some vowels", "logic"),
    S("text-vowels-case", "toolkit/text.py", "for c in s.lower() if", "for c in s if",
      "text.count_vowels('Education')", "5", "count_vowels ignores capital vowels", "logic"),
    S("text-initials-upper", "toolkit/text.py", "p[0].upper() for p in parts", "p[0] for p in parts",
      "text.initials('ada lovelace')", "'AL'", "initials() are not capitalised", "logic"),
    S("text-camel-leading-underscore", "toolkit/text.py", "if c.isupper() and i > 0:", "if c.isupper():",
      "text.camel_to_snake('Value')", "'value'", "camel_to_snake adds a leading underscore", "edge-case"),
    # -------------------------------------------------------------------- seq
    S("seq-chunk-last", "toolkit/seq.py", "range(0, len(items), size)", "range(0, len(items) - 1, size)",
      "report.pages(list(range(5)), 2)", "3", "pages() undercounts when the last page has one item", "cross-module"),
    S("seq-flatten-tuples", "toolkit/seq.py", "isinstance(item, (list, tuple))", "isinstance(item, list)",
      "seq.flatten([1, (2, 3)])", "[1, 2, 3]", "flatten ignores tuples", "logic"),
    S("seq-flatten-recursion", "toolkit/seq.py", "out.extend(flatten(item))", "out.extend(item)",
      "seq.flatten([1, [2, [3]]])", "[1, 2, 3]", "flatten only flattens one level", "logic"),
    S("seq-dedupe-seen", "toolkit/seq.py", "seen.add(x)\n            out.append(x)", "out.append(x)",
      "seq.dedupe([3, 1, 3, 2, 1])", "[3, 1, 2]", "dedupe() does not remove duplicates", "logic"),
    S("seq-rotate-direction", "toolkit/seq.py", "return items[-k:] + items[:-k]", "return items[k:] + items[:k]",
      "seq.rotate([1, 2, 3, 4, 5], 2)", "[4, 5, 1, 2, 3]", "rotate() rotates left, docs say right", "logic"),
    S("seq-rotate-empty", "toolkit/seq.py", "    if not items:\n        return []\n    k", "    k",
      "seq.rotate([], 3)", "[]", "rotate([]) raises ZeroDivisionError", "edge-case"),
    S("seq-window-range", "toolkit/seq.py", "range(len(items) - size + 1)", "range(len(items) - size)",
      "seq.sliding_window([1, 2, 3, 4], 3)", "[(1, 2, 3), (2, 3, 4)]", "sliding_window misses the final window", "off-by-one"),
    S("seq-bsearch-loop-cond", "toolkit/seq.py", "while lo <= hi:", "while lo < hi:",
      "seq.binary_search([1, 3, 5, 7, 9], 9)", "4", "binary_search can't find the last element", "off-by-one"),
    S("seq-bsearch-hi", "toolkit/seq.py", "lo, hi = 0, len(items) - 1", "lo, hi = 0, len(items) - 2",
      "seq.binary_search([1, 3, 5, 7, 9], 9)", "4", "binary_search returns -1 for the largest element", "off-by-one"),
    S("seq-bsearch-hang", "toolkit/seq.py", "lo = mid + 1", "lo = mid",
      "seq.binary_search([1, 3, 5], 4)", "-1", "binary_search hangs forever on a missing value", "hang"),
    S("seq-merge-tail", "toolkit/seq.py", "    out.extend(a[i:])\n    out.extend(b[j:])", "    out.extend(a[i:])",
      "seq.merge_sorted([1, 4, 6], [2, 3, 7, 8])", "[1, 2, 3, 4, 6, 7, 8]", "merge_sorted drops trailing items", "logic"),
    S("seq-merge-or", "toolkit/seq.py", "while i < len(a) and j < len(b):", "while i < len(a) or j < len(b):",
      "seq.merge_sorted([1], [2, 3])", "[1, 2, 3]", "merge_sorted raises IndexError", "operator"),
    S("seq-last-n-zero", "toolkit/seq.py", "if n <= 0:", "if n < 0:",
      "seq.last_n([1, 2, 3], 0)", "[]", "last_n(items, 0) returns everything", "edge-case"),
    # ------------------------------------------------------------------ money
    S("money-discount-formula", "toolkit/money.py", "round(price * (1 - percent / 100), 2)", "round(price * percent / 100, 2)",
      "money.apply_discount(80.0, 25)", "60.0", "apply_discount returns the discount instead of the price", "arithmetic"),
    S("money-discount-full", "toolkit/money.py", "if percent < 0 or percent > 100:", "if percent < 0 or percent >= 100:",
      "money.apply_discount(50.0, 100)", "0.0", "100% discount raises ValueError", "edge-case"),
    S("money-split-floor", "toolkit/money.py", "round(with_tip / people, 2)", "round(with_tip // people, 2)",
      "money.split_bill(100, 3)", "33.33", "split_bill loses cents", "arithmetic"),
    S("money-split-tip-percent", "toolkit/money.py", "(1 + tip_percent / 100)", "(1 + tip_percent)",
      "money.split_bill(100, 4, tip_percent=20)", "30.0", "tip is applied as a multiplier, not a percent", "arithmetic"),
    S("money-compound-rate", "toolkit/money.py", "r = rate / periods_per_year", "r = rate",
      "money.compound_interest(1000, 0.12, 1, 12)", "1126.83", "monthly compounding wildly overstates interest", "arithmetic"),
    S("money-compound-periods", "toolkit/money.py", "n = periods_per_year * years", "n = years",
      "money.compound_interest(1000, 0.12, 1, 12)", "1126.83", "compound_interest ignores periods_per_year", "arithmetic"),
    S("money-format-negative", "toolkit/money.py", "{abs(amount):,.2f}", "{amount:,.2f}",
      "money.format_currency(-5)", "'-$5.00'", "negative amounts get a double minus sign", "format"),
    S("money-format-thousands", "toolkit/money.py", "{abs(amount):,.2f}", "{abs(amount):.2f}",
      "money.format_currency(1234.5)", "'$1,234.50'", "format_currency has no thousands separator", "format"),
    S("money-tax-zero", "toolkit/money.py", "if rate < 0:", "if rate <= 0:",
      "report.invoice_total([(1, 100.0)], tax_rate=0)", "100.0", "invoice_total fails for tax-free invoices", "cross-module"),
    # ------------------------------------------------------------------ dates
    S("dates-leap-and", "toolkit/dates.py", "year % 100 != 0 or year % 400 == 0", "year % 100 != 0 and year % 400 == 0",
      "dates.is_leap_year(2024)", "True", "2024 is not treated as a leap year", "operator"),
    S("dates-leap-400", "toolkit/dates.py", "year % 400 == 0", "year % 400 != 0",
      "dates.is_leap_year(2000)", "True", "is_leap_year(2000) is False", "operator"),
    S("dates-november-days", "toolkit/dates.py", "(4, 6, 9, 11)", "(4, 6, 9)",
      "dates.days_in_month(2023, 11)", "30", "November has 31 days", "logic"),
    S("dates-feb-swapped", "toolkit/dates.py", "29 if is_leap_year(year) else 28", "28 if is_leap_year(year) else 29",
      "dates.days_in_month(2024, 2)", "29", "February lengths are swapped", "logic"),
    S("dates-quarter-formula", "toolkit/dates.py", "(month - 1) // 3 + 1", "month // 3 + 1",
      "dates.quarter_of(3)", "1", "March is reported as Q2", "off-by-one"),
    S("dates-quarter-bound", "toolkit/dates.py", "if month < 1 or month > 12:\n        raise ValueError(\"month must be 1..12\")\n    return (month",
      "if month < 1 or month > 11:\n        raise ValueError(\"month must be 1..12\")\n    return (month",
      "dates.quarter_of(12)", "4", "quarter_of(12) raises ValueError", "off-by-one"),
    S("dates-doy-range", "toolkit/dates.py", "for m in range(1, month):", "for m in range(1, month + 1):",
      "dates.day_of_year(2023, 3, 1)", "60", "day_of_year counts the current month twice", "off-by-one"),
    S("dates-doy-validation", "toolkit/dates.py", "day > days_in_month(year, month)", "day > 31",
      "dates.day_of_year(2023, 2, 29)", "raise ValueError", "day_of_year accepts Feb 29 in non-leap years", "edge-case"),
    # ----------------------------------------------------------------- report
    S("report-mean-rounding", "toolkit/report.py", '"mean": round(stats.mean(values), 2)', '"mean": round(stats.mean(values))',
      "report.summarize([1, 2, 3, 4])", "{'count': 4, 'mean': 2.5, 'median': 2.5, 'max': 4}", "summarize() rounds the mean to an integer", "logic"),
    S("report-max-last", "toolkit/report.py", '"max": max(values)', '"max": values[-1]',
      "report.summarize([3, 9, 2])", "{'count': 3, 'mean': 4.67, 'median': 3, 'max': 9}", "summarize() max is wrong for unsorted input", "logic"),
    S("report-top-words-order", "toolkit/report.py", "key=lambda w: (-counts[w], w)", "key=lambda w: (counts[w], w)",
      "report.top_words('b a b c a b', 2)", "['b', 'a']", "top_words returns the least common words", "logic"),
    S("report-top-words-slice", "toolkit/report.py", "return ranked[:n]", "return ranked[:n - 1]",
      "report.top_words('z y x', 2)", "['x', 'y']", "top_words returns one word too few", "off-by-one"),
    S("report-invoice-tax-base", "toolkit/report.py", "money.tax(discounted, tax_rate)", "money.tax(subtotal, tax_rate)",
      "report.invoice_total([(2, 10.0), (1, 5.0)], discount_percent=10, tax_rate=0.1)", "24.75",
      "invoice tax is computed before the discount", "logic"),
    # ---------------------------------------------------------------- invalid
    S("invalid-median-lower", "toolkit/stats.py", "", "", "stats.median([1, 2, 3, 4])", "2",
      "median() returns a float for even lists", "invalid", kind="invalid",
      note="I think median should pick the lower middle element."),
    S("invalid-rotate-left", "toolkit/seq.py", "", "", "seq.rotate([1, 2, 3], 1)", "[2, 3, 1]",
      "rotate() goes the wrong way", "invalid", kind="invalid", note="Rotating by 1 should move the first item to the end."),
    S("invalid-leap-1900", "toolkit/dates.py", "", "", "dates.is_leap_year(1900)", "True",
      "1900 should be a leap year", "invalid", kind="invalid", note="1900 is divisible by 4."),
    S("invalid-percentile-interp", "toolkit/stats.py", "", "", "stats.percentile([1, 2, 3, 4], 50)", "2.5",
      "percentile doesn't interpolate", "invalid", kind="invalid", note="numpy gives 2.5 here."),
    S("invalid-word-count-hyphen", "toolkit/text.py", "", "", "text.word_count('state-of-the-art design')", "5",
      "word_count treats hyphenated words as one", "invalid", kind="invalid", note="Hyphenated words should count separately."),
]
