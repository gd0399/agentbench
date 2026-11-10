"""Hidden grading suite for the toolkit library: name -> test source.

The generator splits this per task: tests that still pass on the buggy repo
become the repo's *visible* `tests/test_toolkit.py` (a regression guard the
agents may run); the full suite is held back and only used for grading.
"""

TESTS: dict[str, str] = {
    # ---- stats -------------------------------------------------------------
    "test_mean_basic": "assert stats.mean([1, 2, 3, 4]) == 2.5",
    "test_mean_single": "assert stats.mean([7]) == 7",
    "test_mean_empty": "with pytest.raises(ValueError):\n    stats.mean([])",
    "test_median_odd": "assert stats.median([3, 1, 2]) == 2",
    "test_median_even": "assert stats.median([4, 1, 3, 2]) == 2.5",
    "test_median_empty": "with pytest.raises(ValueError):\n    stats.median([])",
    "test_mode_basic": "assert stats.mode([1, 2, 2, 3]) == 2",
    "test_mode_tie_first": "assert stats.mode([5, 3, 3, 5]) == 5",
    "test_variance_sample": "assert stats.variance([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(4.571428571)",
    "test_variance_population": "assert stats.variance([2, 4, 4, 4, 5, 5, 7, 9], sample=False) == 4",
    "test_variance_too_small": "with pytest.raises(ValueError):\n    stats.variance([1])",
    "test_percentile_mid": "assert stats.percentile([15, 20, 35, 40, 50], 40) == 20",
    "test_percentile_rounds_up": "assert stats.percentile([15, 20, 35, 40, 50], 30) == 20",
    "test_percentile_max": "assert stats.percentile([15, 20, 35, 40, 50], 100) == 50",
    "test_percentile_zero": "assert stats.percentile([15, 20, 35, 40, 50], 0) == 15",
    "test_percentile_bounds": "with pytest.raises(ValueError):\n    stats.percentile([1, 2], 101)",
    "test_moving_average": "assert stats.moving_average([1, 2, 3, 4, 5], 2) == [1.5, 2.5, 3.5, 4.5]",
    "test_moving_average_full": "assert stats.moving_average([2, 4, 6], 3) == [4.0]",
    "test_moving_average_bad": "with pytest.raises(ValueError):\n    stats.moving_average([1], 0)",
    "test_clamp_inside": "assert stats.clamp(5, 0, 10) == 5",
    "test_clamp_low": "assert stats.clamp(-3, 0, 10) == 0",
    "test_clamp_high": "assert stats.clamp(30, 0, 10) == 10",
    "test_clamp_equal_bounds": "assert stats.clamp(3, 3, 3) == 3",
    "test_clamp_bad": "with pytest.raises(ValueError):\n    stats.clamp(1, 5, 0)",
    # ---- text --------------------------------------------------------------
    "test_slugify": "assert text.slugify('  Hello, World! ') == 'hello-world'",
    "test_slugify_digits": "assert text.slugify('Top 10 Tips') == 'top-10-tips'",
    "test_truncate_short": "assert text.truncate('hello', 10) == 'hello'",
    "test_truncate_long": "assert text.truncate('hello world', 8) == 'hello...'",
    "test_truncate_exact": "assert text.truncate('hello', 5) == 'hello'",
    "test_word_count": "assert text.word_count('  the quick  brown fox ') == 4",
    "test_word_count_empty": "assert text.word_count('') == 0",
    "test_palindrome_true": "assert text.is_palindrome('A man, a plan, a canal: Panama')",
    "test_palindrome_false": "assert not text.is_palindrome('hello')",
    "test_title_case": "assert text.title_case('the lord of the rings') == 'The Lord of the Rings'",
    "test_title_case_first_minor": "assert text.title_case('a tale of two cities') == 'A Tale of Two Cities'",
    "test_title_case_mixed": "assert text.title_case('hELLO wORLD') == 'Hello World'",
    "test_count_vowels":"assert text.count_vowels('Education') == 5",
    "test_initials": "assert text.initials('ada  lovelace byron') == 'ALB'",
    "test_camel_to_snake": "assert text.camel_to_snake('parseHttpResponse') == 'parse_http_response'",
    "test_camel_to_snake_leading": "assert text.camel_to_snake('Value') == 'value'",
    # ---- seq ---------------------------------------------------------------
    "test_chunk": "assert seq.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]",
    "test_chunk_exact": "assert seq.chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]",
    "test_chunk_bad": "with pytest.raises(ValueError):\n    seq.chunk([1], 0)",
    "test_flatten": "assert seq.flatten([1, [2, [3, (4, 5)]], 6]) == [1, 2, 3, 4, 5, 6]",
    "test_dedupe_order": "assert seq.dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]",
    "test_rotate": "assert seq.rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]",
    "test_rotate_zero": "assert seq.rotate([1, 2, 3], 0) == [1, 2, 3]",
    "test_rotate_wrap": "assert seq.rotate([1, 2, 3], 4) == [3, 1, 2]",
    "test_rotate_empty": "assert seq.rotate([], 3) == []",
    "test_sliding_window": "assert seq.sliding_window([1, 2, 3, 4], 3) == [(1, 2, 3), (2, 3, 4)]",
    "test_binary_search_found": "assert seq.binary_search([1, 3, 5, 7, 9], 7) == 3",
    "test_binary_search_edges": "assert seq.binary_search([1, 3, 5, 7, 9], 1) == 0 and seq.binary_search([1, 3, 5, 7, 9], 9) == 4",
    "test_binary_search_missing": "assert seq.binary_search([1, 3, 5], 4) == -1",
    "test_merge_sorted": "assert seq.merge_sorted([1, 4, 6], [2, 3, 7, 8]) == [1, 2, 3, 4, 6, 7, 8]",
    "test_merge_sorted_stable": "assert seq.merge_sorted([1, 2], [2, 3]) == [1, 2, 2, 3]",
    "test_last_n": "assert seq.last_n([1, 2, 3, 4], 2) == [3, 4]",
    "test_last_n_zero": "assert seq.last_n([1, 2, 3], 0) == []",
    # ---- money -------------------------------------------------------------
    "test_discount": "assert money.apply_discount(80.0, 25) == 60.0",
    "test_discount_full": "assert money.apply_discount(50.0, 100) == 0.0",
    "test_discount_bounds": "with pytest.raises(ValueError):\n    money.apply_discount(10, 120)",
    "test_split_bill": "assert money.split_bill(100, 4) == 25.0",
    "test_split_bill_uneven": "assert money.split_bill(100, 3) == 33.33",
    "test_split_bill_tip":"assert money.split_bill(100, 4, tip_percent=20) == 30.0",
    "test_compound_annual": "assert money.compound_interest(1000, 0.05, 2) == 1102.5",
    "test_compound_monthly": "assert money.compound_interest(1000, 0.12, 1, 12) == 1126.83",
    "test_format_currency": "assert money.format_currency(1234.5) == '$1,234.50'",
    "test_format_currency_negative": "assert money.format_currency(-5) == '-$5.00'",
    "test_tax": "assert money.tax(200, 0.08) == 16.0",
    "test_tax_zero": "assert money.tax(100, 0) == 0",
    # ---- dates -------------------------------------------------------------
    "test_leap_years": "assert [dates.is_leap_year(y) for y in (1900, 2000, 2024, 2023)] == [False, True, True, False]",
    "test_days_in_month": "assert [dates.days_in_month(2023, m) for m in (1, 2, 4, 11, 12)] == [31, 28, 30, 30, 31]",
    "test_days_in_feb_leap": "assert dates.days_in_month(2024, 2) == 29",
    "test_days_in_month_bad": "with pytest.raises(ValueError):\n    dates.days_in_month(2024, 13)",
    "test_quarter_of": "assert [dates.quarter_of(m) for m in (1, 3, 4, 6, 7, 12)] == [1, 1, 2, 2, 3, 4]",
    "test_day_of_year": "assert dates.day_of_year(2023, 3, 1) == 60",
    "test_day_of_year_leap": "assert dates.day_of_year(2024, 12, 31) == 366",
    "test_day_of_year_bad": "with pytest.raises(ValueError):\n    dates.day_of_year(2023, 2, 29)",
    # ---- report (cross-module) ----------------------------------------------
    "test_summarize": "assert report.summarize([1, 2, 3, 4]) == {'count': 4, 'mean': 2.5, 'median': 2.5, 'max': 4}",
    "test_summarize_unsorted": "assert report.summarize([3, 9, 2]) == {'count': 3, 'mean': 4.67, 'median': 3, 'max': 9}",
    "test_top_words":"assert report.top_words('b a b c a b', 2) == ['b', 'a']",
    "test_top_words_tie_alpha": "assert report.top_words('z y x', 2) == ['x', 'y']",
    "test_invoice_total": "assert report.invoice_total([(2, 10.0), (1, 5.0)], discount_percent=10, tax_rate=0.1) == 24.75",
    "test_headline": "assert report.headline('the art of war', 12) == 'The Art o...'",
    "test_pages": "assert report.pages(list(range(10)), 3) == 4",
}

HEADER = "import pytest\nfrom toolkit import stats, text, seq, money, dates, report\n\n"


def render(names) -> str:
    parts = [HEADER]
    for name in names:
        body = "\n".join("    " + line for line in TESTS[name].splitlines())
        parts.append(f"def {name}():\n{body}\n\n")
    return "".join(parts)
