from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Collections, Features, ProductDetails, Products

admin.site.register(Features)
admin.site.register(Collections)


@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "product__name", "color", "size", "stock"]
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
    list_display = ["name", "category", "displayed_price", "gender_and_age"]
    list_filter = ["category", "gender_and_age", "currency"]

    @admin.display(description="Price")
    def displayed_price(self, obj):
        return f"{obj.price} {obj.currency}"

    def changelist_view(self, request, extra_context=None):
        """
        Display warning if there exists products without variants
        """
        products_with_variants = ProductDetails.objects.values_list(
            "product_id", flat=True
        )
        products_without_variants = Products.objects.exclude(
            pk__in=products_with_variants
        )
        if products_without_variants.exists():
            message = mark_safe("There're are products that doest have any variants")
            self.message_user(request, message, level="warning")
        return super().changelist_view(request, extra_context)
