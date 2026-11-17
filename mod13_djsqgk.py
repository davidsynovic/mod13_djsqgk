

import re
import unittest
from datetime import datetime




def validate_symbol(symbol):
    """Symbol must be 1-7 capital letters A-Z."""
    if not isinstance(symbol, str):
        return False
    return re.fullmatch(r"[A-Z]{1,7}", symbol) is not None


def validate_chart_type(chart_type):
    """Chart type must be a single character: '1' or '2'."""
    if not isinstance(chart_type, str):
        return False
    return re.fullmatch(r"[1-2]", chart_type) is not None


def validate_time_series(time_series):
    """Time series must be a single character: '1', '2', '3', or '4'."""
    if not isinstance(time_series, str):
        return False
    return re.fullmatch(r"[1-4]", time_series) is not None


def validate_date(date_str):
    """Date must be a real calendar date in YYYY-MM-DD format."""
    if not isinstance(date_str, str):
        return False
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str) is None:
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate_start_date(date_str):
    return validate_date(date_str)


def validate_end_date(date_str):
    return validate_date(date_str)




class TestSymbol(unittest.TestCase):
    def test_valid_symbols(self):
        for s in ["A", "AAPL", "GOOG", "MSFT", "ABCDEFG"]:
            with self.subTest(symbol=s):
                self.assertTrue(validate_symbol(s))

    def test_empty_symbol(self):
        self.assertFalse(validate_symbol(""))

    def test_too_long(self):
        self.assertFalse(validate_symbol("ABCDEFGH"))  # 8 chars

    def test_lowercase_rejected(self):
        for s in ["aapl", "aAPL", "AAPl"]:
            with self.subTest(symbol=s):
                self.assertFalse(validate_symbol(s))

    def test_non_alpha_rejected(self):
        for s in ["AAP1", "123", "AA-PL", "AA PL", "AAPL!", "A.B"]:
            with self.subTest(symbol=s):
                self.assertFalse(validate_symbol(s))

    def test_whitespace_rejected(self):
        for s in [" AAPL", "AAPL ", "AAPL\n", " "]:
            with self.subTest(symbol=s):
                self.assertFalse(validate_symbol(s))

    def test_non_ascii_rejected(self):
        self.assertFalse(validate_symbol("ÀÉÎ"))

    def test_non_string_rejected(self):
        for s in [None, 123, 4.5, ["AAPL"]]:
            with self.subTest(symbol=s):
                self.assertFalse(validate_symbol(s))


class TestChartType(unittest.TestCase):
    def test_valid_chart_types(self):
        for c in ["1", "2"]:
            with self.subTest(chart_type=c):
                self.assertTrue(validate_chart_type(c))

    def test_out_of_range_numbers(self):
        for c in ["0", "3", "4", "9"]:
            with self.subTest(chart_type=c):
                self.assertFalse(validate_chart_type(c))

    def test_multiple_characters(self):
        for c in ["12", "11", "10", "01"]:
            with self.subTest(chart_type=c):
                self.assertFalse(validate_chart_type(c))

    def test_empty(self):
        self.assertFalse(validate_chart_type(""))

    def test_non_numeric(self):
        for c in ["a", "A", "!", " ", "one"]:
            with self.subTest(chart_type=c):
                self.assertFalse(validate_chart_type(c))

    def test_whitespace_padding(self):
        for c in [" 1", "1 ", "2\n"]:
            with self.subTest(chart_type=c):
                self.assertFalse(validate_chart_type(c))

    def test_non_string_rejected(self):
        for c in [None, 1, 2, 1.0]:
            with self.subTest(chart_type=c):
                self.assertFalse(validate_chart_type(c))


class TestTimeSeries(unittest.TestCase):
    def test_valid_time_series(self):
        for t in ["1", "2", "3", "4"]:
            with self.subTest(time_series=t):
                self.assertTrue(validate_time_series(t))

    def test_out_of_range_numbers(self):
        for t in ["0", "5", "6", "9"]:
            with self.subTest(time_series=t):
                self.assertFalse(validate_time_series(t))

    def test_multiple_characters(self):
        for t in ["12", "10", "44", "01"]:
            with self.subTest(time_series=t):
                self.assertFalse(validate_time_series(t))

    def test_empty(self):
        self.assertFalse(validate_time_series(""))

    def test_non_numeric(self):
        for t in ["a", "x", "-", " ", "."]:
            with self.subTest(time_series=t):
                self.assertFalse(validate_time_series(t))

    def test_negative_rejected(self):
        self.assertFalse(validate_time_series("-1"))

    def test_non_string_rejected(self):
        for t in [None, 1, 4, 2.0]:
            with self.subTest(time_series=t):
                self.assertFalse(validate_time_series(t))


class DateTestsMixin:
    """Shared date tests; subclasses set self.validate."""

    def test_valid_dates(self):
        for d in ["2024-01-01", "2023-12-31", "1999-06-15", "2026-11-17"]:
            with self.subTest(date=d):
                self.assertTrue(self.validate(d))

    def test_leap_day_valid_on_leap_year(self):
        self.assertTrue(self.validate("2024-02-29"))

    def test_leap_day_invalid_on_non_leap_year(self):
        self.assertFalse(self.validate("2023-02-29"))

    def test_invalid_month(self):
        for d in ["2024-00-10", "2024-13-10"]:
            with self.subTest(date=d):
                self.assertFalse(self.validate(d))

    def test_invalid_day(self):
        for d in ["2024-01-00", "2024-01-32", "2024-04-31"]:
            with self.subTest(date=d):
                self.assertFalse(self.validate(d))

    def test_wrong_format(self):
        for d in ["01-01-2024", "2024/01/01", "20240101", "2024-1-1",
                  "24-01-01", "Jan 1, 2024", "2024.01.01"]:
            with self.subTest(date=d):
                self.assertFalse(self.validate(d))

    def test_empty_and_whitespace(self):
        for d in ["", " ", " 2024-01-01", "2024-01-01 ", "2024-01-01\n"]:
            with self.subTest(date=d):
                self.assertFalse(self.validate(d))

    def test_non_date_text(self):
        for d in ["abcd-ef-gh", "yyyy-mm-dd", "not a date"]:
            with self.subTest(date=d):
                self.assertFalse(self.validate(d))

    def test_non_string_rejected(self):
        for d in [None, 20240101, datetime(2024, 1, 1)]:
            with self.subTest(date=d):
                self.assertFalse(self.validate(d))


class TestStartDate(DateTestsMixin, unittest.TestCase):
    def setUp(self):
        self.validate = validate_start_date


class TestEndDate(DateTestsMixin, unittest.TestCase):
    def setUp(self):
        self.validate = validate_end_date


if __name__ == "__main__":
    unittest.main(verbosity=2)