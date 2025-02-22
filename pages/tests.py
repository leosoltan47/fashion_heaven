from decimal import Decimal
from django.test import TestCase
from .models import Features, Products, Categories, ProductDetails, Collections


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
