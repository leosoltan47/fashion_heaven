from decimal import Decimal
from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
import re


def validate_hex_color(value):
    regex = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$")
    if not regex.match(value):
        raise ValidationError("Invalid hex color code")


class Categories(models.Model):
    """
    Represents categories. Allows to chain categories into sub-categories

    Attributes:
        name (CharField): Name of the category
        parent (ForeighField): Parent category if exists
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.parent}/{self.name}"


class Features(models.Model):
    """
    Represents reusable product features, such as 'Fast Drying' or 'Keeping Cool'.

    These features can be associated with multiple products, allowing for efficient categorization and filtering.

    Attributes:
        name (CharField): The name of the feature (e.g. 'Fast Drying', 'Keeping Cool').
    """

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Features"


class Products(models.Model):
    """
    Represents a product with details that remain consistent across variants.

    This model stores information that is shared among all variants of a product,
    such as the product name, price, and description.

    Attributes:
        name (CharField): The name of the product.
        category (ForeignKey): Category product belongs to.
        price_in_dollars (DecimalField): The base price of the product in dollars.
        currency (CharField): Stores the currency of the product.
        description (TextField): A detailed description of the product.
        feature (ManyToManyField): The features associated with this product.
        gender_and_age (CharField): Target gender and age group of the product.
    """

    class Meta:
        verbose_name_plural = "Products"

    class GenderAndAge(models.TextChoices):
        WOMEN = "W", "Women"
        MEN = "M", "Men"
        UNISEX = "U", "Unisex"
        GIRLS = "G", "Girls"
        BOYS = "B", "Boys"
        KIDS = "K", "Kids"

    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Categories, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    # Allow to store prices up to 99999,99 dollars
    price_in_dollars = models.DecimalField(
        default=Decimal(0.00), max_digits=7, decimal_places=2
    )
    gender_and_age = models.CharField(
        max_length=1, choices=GenderAndAge.choices, default=GenderAndAge.UNISEX
    )
    description = models.TextField()
    feature = models.ManyToManyField(Features)

    def __str__(self) -> str:
        return self.name


class ProductDetails(models.Model):
    """
    Represents a variant of a product, with details that can differ among variants.

    This model stores information that is specific to a particular variant of a product
    such as color, size, and stock level. Related to :model:`pages.Products` via one-to-many relation

    Attributes:
        product (ForeignKey): The product that this variant belongs to.
        size (CharField): The size of the variant (e.g. '10' for shoes, 'XL' for clothes).
        stock (PositiveIntegerField): The number of items remaining in stock for this variant.
    """

    size = models.CharField(max_length=10)
    stock = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Product Details"


class ProductImages(models.Model):
    """
    Represents images associated with a product variant.

    This model establishes a many-to-one relationship with :model:`pages.ProductDetails`,
    allowing a product variant to have multiple images.

    Attributes:
        content (ImageField): The image file associated with the product variant.
        product_detail (ForeignKey): The product variant that this image belongs to.
    """

    class Meta:
        verbose_name_plural = "Product Images"

    content = models.ImageField()
    product_detail = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)


class Color(models.Model):
    """
    Represents colors images can take.

    Attributes:
        color_code (CharField): Hex value of the color
        images (ManyToManyField): Connection to product images
    """

    color_code = models.CharField(
        default="#FF0000", max_length=9, validators=[validate_hex_color]
    )
    images = models.ManyToManyField(ProductImages)

    @admin.display
    def color(self):
        return format_html(
            '<svg width="20px" height="20px"><rect width = "20" height = "20" fill = "{}"/></svg>',
            self.color_code,
        )


class Collections(models.Model):
    """
    Represents a curated grouping of products, such as a seasonal collection or a themed assortment.

    This model enables :model:`pages.Products` to be associated with multiple collections, and collections to contain multiple products.

    Attributes:
        name (CharField): Unique name of the collection (e.g. 'Summer Sale', 'New Arrivals').
        description (TextField): Optional description of the collection
        badge (CharField): Optional text to display on product card
        product (ManyToManyField): Products associated with this collection
    """

    class Meta:
        verbose_name_plural = "Collections"

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    badge = models.CharField(max_length=20, blank=True, null=True)
    product = models.ManyToManyField(Products)

    def __str__(self) -> str:
        return self.name
