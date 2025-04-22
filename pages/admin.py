from django.contrib import admin
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy
from Pylette import extract_colors
from .models import (
    Categories,
    Collections,
    Color,
    Features,
    ProductDetails,
    ProductImages,
    Products,
    Color,
)
from currency_converter import CurrencyConverter

admin.site.register(Features)
admin.site.register(Collections)
admin.site.register(Categories)
admin.site.register(Color)
admin.site.register(ProductImages)


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


class ColorListFilter(admin.SimpleListFilter):
    title = gettext_lazy("Color")
    parameter_name = "color_code"

    def lookups(self, request, model_admin):
        colors = (
            Color.objects.only("color_code").all().distinct().order_by("color_code")
        )

        return [(color.color_code, color.color()) for color in colors]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.prefetch_related().filter(
            productimages__color__color_code=self.value()
        )


class StockListFilter(admin.SimpleListFilter):
    title = gettext_lazy("Stock ranges")
    parameter_name = "stock"
    template = "admin/stock_filter.html"
    MAX_INT = 2147483647

    def lookups(self, request, model_admin):  # type: ignore
        return ((),)

    @staticmethod
    def _parse(query: str) -> int | tuple[int, int]:
        """
        Parse query string with '..' as separator to get the range. If separator
        is not present the parsed number is returned. If starting point is no
        specified '0' is assumed. If end point is not specified biggest integer
        that `django.models.PositiveIntegerField` can store is returned.

        Raises `ValueError` if string can't be parsed or if multiple
        separators provided
        """
        query = query.strip()
        if query == "":
            raise ValueError("Query string is empty")

        if len(temp := query.split(sep="..")) == 1:
            if not temp[0].isdigit():
                raise ValueError("Only digits and '..' separator are allowed")

            return int(temp[0])
        elif len(temp) == 2:
            not_valid = lambda value: not value.isdigit() and value != ""
            if not_valid(temp[0]) or not_valid(temp[1]):
                raise ValueError("Only digits and '..' separator are allowed")

            return int(temp[0] or 0), int(temp[1] or StockListFilter.MAX_INT)
        else:
            raise ValueError(
                f"There could be only 1 '..' seperator. Found: {len(temp)}"
            )

    def queryset(self, request, queryset):
        req = request.GET.get("stock") or ""
        if req == "":
            return queryset.order_by("id")
        range_ = StockListFilter._parse(req)
        if type(range_) == int:
            kwargs = {"stock": range_}
        elif type(range_) == tuple:
            kwargs = {"stock__gte": range_[0], "stock__lt": range_[1]}
        else:
            return queryset.order_by("id")
        return queryset.filter(**kwargs).order_by("id")

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))  # type: ignore
        all_choice["query_parts"] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )

        yield all_choice


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):

    list_display = ["id", "productimages__color__color_code", "size", "stock"]
    list_filter = ["size", StockListFilter, ColorListFilter]
    inlines = [ProductImagesInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if instance.pk is None:
                instance.save()
                # NOTE: In the future replace 2 with a constant to detemine how colors
                # will be shown for a particular product
                img = instance.content.path
                pallete = extract_colors(img, 2, sort_mode="frequency")
                for color in pallete.colors:
                    # Convert rgb to hex
                    red, green, blue = color.rgb
                    color_code = f"#{hex(red)[-2:]}{hex(green)[-2:]}{hex(blue)[-2:]}"
                    color, created = Color.objects.get_or_create(color_code=color_code)
                    print(created)
                    print(color)
                    color.images.add(instance)
            else:
                instance.save()

    # TODO: Implement low stock threshold notification, alerting admins when a
    # product's inventory falls below a specified level, triggering a warning
    # that the product is at risk of going out of stock.
    def changelist_view(self, request, extra_context=None):
        """
        Display warning if there're out of stock variants
        """

        # Warn if stock is empty
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
