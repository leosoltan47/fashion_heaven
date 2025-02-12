from django.db import models

# TODO: Add collection table to add categories, collections and other groupings stored
# in a single table


class Features(models.Model):
    """
    Represents reusable product features, such as 'Fast Drying' or 'Keeping Cool'.

    These features can be associated with multiple products, allowing for efficient categorization and filtering.

    Attributes:
        name (CharField): The name of the feature (e.g. 'Fast Drying', 'Keeping Cool').
    """

    name = models.CharField(max_length=50)


class Products(models.Model):
    """
    Represents a product with details that remain consistent across variants.

    This model stores information that is shared among all variants of a product,
    such as the product name, price, and description.

    Attributes:
        name (CharField): The name of the product.
        price_in_dollars (DecimalField): The base price of the product in dollars.
        description (TextField): A detailed description of the product.
        feature (ManyToManyField): The features associated with this product.
    """

    name = models.CharField(max_length=50)
    # Allow to store prices up to 99999,99 dollars
    price_in_dollars = models.DecimalField(
        name="price", default=0, max_digits=7, decimal_places=2
    )
    description = models.TextField()
    feature = models.ManyToManyField(Features)


class ProductDetails(models.Model):
    """
    Represents a variant of a product, with details that can differ among variants.

    This model stores information that is specific to a particular variant of a product
    such as color, size, and stock level. Related to :model:`pages.Products` via one-to-many relation

    Attributes:
        product (ForeignKey): The product that this variant belongs to.
        color (CharField): The color of the variant.
        size (CharField): The size of the variant (e.g. '10' for shoes, 'XL' for clothes).
        stock (PositiveIntegerField): The number of items remaining in stock for this variant.
    """

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    color = models.CharField(max_length=15)
    size = models.CharField(max_length=10)

    # NOTE: `type: ignore` comment disables pyright linting on that line. It's needed to
    # remove linting error caused by assigning 0 to default field in `PositiveIntegerField`
    stock = models.PositiveIntegerField(default=0)  # type: ignore


class ProductImages(models.Model):
    """
    Represents images associated with a product variant.

    This model establishes a many-to-one relationship with :model:`pages.ProductDetails`,
    allowing a product variant to have multiple images.

    Attributes:
        content (ImageField): The image file associated with the product variant.
        product_detail (ForeignKey): The product variant that this image belongs to.
    """

    content = models.ImageField()
    product_detail = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
