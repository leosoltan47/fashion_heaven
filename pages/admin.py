from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Collections, Features, ProductDetails, Products

admin.site.register(Features)
admin.site.register(Collections)


@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "color", "size", "stock"]

    # TODO: Add `color` to `list_filter`
    # TODO: Add custom `stock` filter to display greater or less than input
    list_filter = ["size", "stock"]

    # TODO: Implement low stock threshold notification, alerting admins when a
    # product's inventory falls below a specified level, triggering a warning
    # that the product is at risk of going out of stock.
    def changelist_view(self, request, extra_context=None):
        """
        Display warning if there're out of stock variants
        """
        out_of_stock_variants = ProductDetails.objects.filter(stock=0)
        if out_of_stock_variants.exists():
            message = mark_safe("There are variants that are out of stock")
            self.message_user(request, message, level="warning")
        return super().changelist_view(request, extra_context)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price_in_dollars", "gender_and_age"]
    list_filter = ["category", "gender_and_age"]
