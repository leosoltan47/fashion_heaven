from django.db import models

# NOTE: `type: ignore` comment disables pyright linting on that line. It's needed to
# remove linting error caused by assigning 0 to default field in `PositiveIntegerField`
# TODO: Add collection table to add categories, collections and other groupings stored
# in a singel table


class Features(models.Model):
    """
    Represents tag like features like 'Fast Drying' and 'Keeping Cool'
    used by different products, related to :model:`pages.Products`
    """

    name = models.CharField(max_length=50)


class Products(models.Model):
    """
    Represents product with details that doesn't change among variants,
    related to :model:`pages.ProductDetails` and :model:`pages.Features`
    """

    name = models.CharField(max_length=50)
    price_in_dollars = models.PositiveIntegerField(name="price", default=0)  # type: ignore
    description = models.TextField()
    feature = models.ManyToManyField(Features)


class ProductDetails(models.Model):
    """
    Represents product'd details that changes among variants,
    related to :model:`pages.Products` and :model:`pages.ProductImages`
    """

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    color = models.CharField(max_length=15)
    size = models.CharField(
        max_length=10,
        help_text="Stores sizes for both shoes (number) and clothes (XL, XXL, etc)",
    )
    stock = models.PositiveIntegerField(default=0, help_text="Number of items remaining in stock")  # type: ignore


class ProductImages(models.Model):
    content = models.ImageField(
        help_text="Stores image into folder specified in `MEDIA_ROOT`"
    )
    product_detail = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
