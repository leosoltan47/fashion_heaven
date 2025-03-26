from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from pages.admin import StockListFilter
from .models import Features, Products, Categories, ProductDetails, Collections, validate_hex_color


class CollectionsModelTests(TestCase):
    def setUp(self) -> None:
        feat = Features.objects.create(name="Comfy")
        var = ProductDetails.objects.create(color_code="#FF0000", size="S", stock=10)
        prd = Products.objects.create(
            name="T-Shirt",
            category=Categories.objects.create(name="Topper"),
            price_in_dollars=Decimal(29.00),
            description="Placeholder",
            gender_and_age=Products.GenderAndAge.UNISEX,
        )
        prd.feature.add(feat)
        prd.details.add(var)
        col = Collections.objects.create(name="Summer", description="Placeholder")
        col.product.add(prd)

    def test_creation(self):
        self.assertEqual(2 + 2, 4)


class FeaturesModelTests(TestCase):
    def setUp(self) -> None:
        _ = Features.objects.create(name="Fast-Drying")

    def test_creation(self):
        self.assertEqual(2 + 2, 4)


class ProductDetailsModelTests(TestCase):
    def setUp(self) -> None:
        _ = ProductDetails.objects.create(color_code="#FF0000", size="M", stock=10)

    def test_creation(self):
        self.assertEqual(2 + 2, 4)

    def test_validator_happy(self):
        valid_colors = [
            '#FFFFFF',
            '#000000',
            '#123456',
            '#ABCDEF',
            '#789012',
            '#FF0000',
            '#00FF00',
            '#0000FF',
            '#12345678',
        ]
        for color in valid_colors:
            self.assertEqual(validate_hex_color(color), None)

    def test_validator_sad(self):
        invalid_colors = [
            'FFFFFF',  # missing #
            '#12345',  # too short
            '#1234567',  # too long (7 digits)
            '#12345G',  # invalid character (G)
            '#12345 ',  # trailing space
            ' #123456',  # leading space
            '#1234567890',  # too long (10 digits)
            '123456',  # missing #
            '#',  # empty
            '#123',  # too short
        ]
        for color in invalid_colors:
            with self.assertRaises(ValidationError):
                validate_hex_color(color)



class CategoriesModelTests(TestCase):
    def setUp(self) -> None:
        parent = Categories.objects.create(name="Category")
        _ = Categories.objects.create(name="Sub-Category", parent=parent)

    def test_creation(self):
        self.assertEqual(2 + 2, 4)


class ProductsModelTests(TestCase):
    def setUp(self) -> None:
        feat = Features.objects.create(name="Comfy")
        var = ProductDetails.objects.create(color_code="#FF0000", size="S", stock=10)
        prd = Products.objects.create(
            name="T-Shirt",
            category=Categories.objects.create(name="Topper"),
            price_in_dollars=Decimal(29.00),
            description="Placeholder",
            gender_and_age=Products.GenderAndAge.UNISEX,
        )
        prd.feature.add(feat)
        prd.details.add(var)

    def test_basic(self):
        self.assertEqual(2 + 2, 4)


class StockFilterTest(TestCase):
    def setUp(self) -> None:
        # Populate database with test data
        self.COLORS = [
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#FFFF00",
            "#FF00FF",
            "#00FFFF",
            "#800000",
            "#008000",
            "#000080",
            "#808000",
            "#800080",
            "#008080",
            "#C0C0C0",
            "#808080",
            "#999999",
        ]
        self.SIZES = [
            "XS",
            "S",
            "M",
            "L",
            "XL",
            "XXL",
            "XXXL",
            "4XL",
            "5XL",
            "6XL",
            "7XL",
            "8XL",
            "9XL",
            "10XL",
            "11XL",
        ]
        self.STOCKS = [3, 1, 5, 2, 6, 15, 25, 11, 46, 98, 27, 63, 75, 31, 58]
        for color_code, size, stock in zip(self.COLORS, self.SIZES, self.STOCKS):
            ProductDetails.objects.create(color_code=color_code, size=size, stock=stock)

        self.variants = ProductDetails.objects.all()

    def test_parse_happy_path(self):
        cases = [
            ("7", 7),
            ("8..", (8, StockListFilter.MAX_INT)),
            ("..9", (0, 9)),
            ("12..16", (12, 16)),
        ]
        for query, result in cases:
            self.assertEqual(StockListFilter._parse(query), result)

    def test_parse_sad_path(self):
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
