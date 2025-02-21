from django.contrib import admin
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from .models import Collections, Features, ProductDetails, Products
from currency_converter import CurrencyConverter

admin.site.register(Features)
admin.site.register(Collections)


class ProductsAdminForm(forms.ModelForm):
    class Currency(models.TextChoices):
        USD = "USD"
        GBP = "GBP"
        TL = "TRY"
        EUR = "EUR"

    price = forms.DecimalField(max_digits=7, decimal_places=2)
    currency = forms.ChoiceField(choices=Currency.choices)

    class Meta:
        fields = [
            "name",
            "category",
            "gender_and_age",
            "price",
            "currency",
            "details",
            "description",
            "feature",
        ]

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.pop("price")
        currency = cleaned_data.pop("currency")
        if price and currency:
            price_in_dollars = CurrencyConverter().convert(
                price, currency, self.Currency.USD
            )
            cleaned_data["price_in_dollars"] = price_in_dollars
        return cleaned_data


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
    form = ProductsAdminForm

    list_display = ["name", "category", "price_in_dollars", "gender_and_age"]
    list_filter = ["category", "gender_and_age"]

    def save_model(self, request, obj, form, change):
        obj.price_in_dollars = form.cleaned_data.get("price_in_dollars")
        return super().save_model(request, obj, form, change)
