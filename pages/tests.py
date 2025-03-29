from django.core.exceptions import ValidationError
from django.test import TestCase
from pages.admin import StockListFilter
from .models import validate_hex_color


class UtilTest(TestCase):
    def test_validator_happy(self):
        valid_colors = [
            "#FFFFFF",
            "#000000",
            "#123456",
            "#ABCDEF",
            "#789012",
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#12345678",
        ]
        for color in valid_colors:
            self.assertEqual(validate_hex_color(color), None)

    def test_validator_sad(self):
        invalid_colors = [
            "FFFFFF",  # missing #
            "#12345",  # too short
            "#1234567",  # too long (7 digits)
            "#12345G",  # invalid character (G)
            "#12345 ",  # trailing space
            " #123456",  # leading space
            "#1234567890",  # too long (10 digits)
            "123456",  # missing #
            "#",  # empty
            "#123",  # too short
        ]
        for color in invalid_colors:
            with self.assertRaises(ValidationError):
                validate_hex_color(color)

    def test_stock_list_filter_parse_happy_path(self):
        cases = [
            ("7", 7),
            ("8..", (8, StockListFilter.MAX_INT)),
            ("..9", (0, 9)),
            ("12..16", (12, 16)),
        ]
        for query, result in cases:
            self.assertEqual(StockListFilter._parse(query), result)

    def test_stock_list_filter_parse_sad_path(self):
        cases = [
            "",
            "abc",
            "..fjko",
            "kjalfdj..kdjf",
            "12..kj",
            "kj..",
            "-1..-16",
            "8...9",
        ]
        for case in cases:
            with self.assertRaises(ValueError):
                _ = StockListFilter._parse(case)
