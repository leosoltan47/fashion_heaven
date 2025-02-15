from decimal import Decimal
from colorfield.fields import ColorField
from django.db import models
from django.contrib import admin
from django.utils.html import format_html


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
        category (CharField): Category product belongs to.
        price_in_dollars (DecimalField): The base price of the product in dollars.
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
    category = models.CharField(max_length=50, null=True)
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
        color (ColorField): The color of the variant.
        size (CharField): The size of the variant (e.g. '10' for shoes, 'XL' for clothes).
        stock (PositiveIntegerField): The number of items remaining in stock for this variant.
    """

    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="details"
    )
    color_code = ColorField(default="#FF0000")
    size = models.CharField(max_length=10)

    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Product Details"

    @admin.display
    def color(self):
        return format_html(
            '<svg width="20px" height="20px"><rect width = "20" height = "20" fill = "{}"/></svg>',
            self.color_code,
        )


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


class Collections(models.Model):
    """
    Represents a curated grouping of products, such as a seasonal collection or a themed assortment.

    This model enables :model:`pages.Products` to be associated with multiple collections, and collections to contain multiple products.

    Attributes:
        name (CharField): Name of the collection (e.g. 'Summer Sale', 'New Arrivals').
        description (TextField): A detailed description of the collection
        product (ManyToManyField): Products associated with this collection
    """

    class Meta:
        verbose_name_plural = "Collections"

    name = models.CharField(max_length=50)
    description = models.TextField()
    product = models.ManyToManyField(Products)

    def __str__(self) -> str:
        return self.name
