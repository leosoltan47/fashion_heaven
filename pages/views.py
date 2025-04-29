from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import ProductDetails, Products, ProductImages
from itertools import groupby
import re


# TODO: Add search bar that renders page specified in the search
def home(request):
    # Show 10 products that has at least one variant as information like color are stored in variants
    products = (
        Products.objects.select_related("category")
        .filter(category__isnull=False)
        .order_by("id")[:10]
    )
    images = (
        ProductImages.objects.select_related("product_detail")
        .filter(product_detail__stock__gt=0, product_detail__product__in=products)
        .prefetch_related("color_set")
        .order_by("product_detail__product")
    )
    products = [
        {
            "id": product.pk,
            "name": product.name,
            "price": product.price_in_dollars,
            "colors": [
                [color.color_code for color in image.color_set.all()]
                for image in images
                if image.product_detail.product.id == product.id
            ],
        }
        for product in products
    ]
    context = {"products": products}
    return render(request, "pages/home.html", context)


def product(request, product_id):
    """
    View function that retrieves product information from get URL
    """
    obj = get_object_or_404(Products, pk=product_id)
    product = {
        "id": obj.pk,
        "name": obj.name,
        "price": obj.price_in_dollars,
        "category": obj.category.name,
    }
    return JsonResponse(product)


def empty_wishlist(request):
    return render(request, "pages/wishlist.html")


def wishlist(request, id_list: str):
    """
    View function for the wishlist page.
    """
    regex = re.compile(r"ids\[\]=(\d+)")
    ids = regex.findall(id_list)
    if len(ids) == 0:
        return render(request, "pages/wishlist.html")
    products = Products.objects.filter(id__in=ids)
    context = {"wishlist_items": products}
    return render(request, "pages/wishlist.html", context)


def bag(request):
    """
    View function for the shopping bag page.
    """
    return render(request, "pages/bag.html")


def catalog(request, title):
    gender_filters = {"women": ["W", "U"], "men": ["M", "U"], "kids": ["K", "B", "G"]}
    gender_fullname = {
        "W": "Womem",
        "M": "Men",
        "K": "Kids",
        "U": "Unisex",
        "B": "Boys",
        "G": "Girls",
    }

    objects = (
        ProductImages.objects.select_related(
            "product_detail", "product_detail__product"
        )
        .filter(
            product_detail__stock__gt=0,
            product_detail__product__gender_and_age__in=gender_filters.get(
                title, ["W", "M", "U", "G", "B", "K"]
            ),
        )
        .prefetch_related("color_set")
        .order_by("product_detail__product__id")
    )

    products = [
        {
            "id": product_pk,
            "name": (objs := list(obj))[0].product_detail.product.name,
            "price": objs[0].product_detail.product.price_in_dollars,
            "colors": [
                [color.color_code for color in image.color_set.all()] for image in objs
            ],
        }
        for product_pk, obj in groupby(objects, lambda x: x.product_detail.product.id)
    ]

    context = {
        "products": products,
        "title": title,
        "genders": {
            gender_fullname[obj.product_detail.product.gender_and_age]
            for obj in objects
        },
        "categories": {obj.product_detail.product.category for obj in objects},
        "sizes": {obj.product_detail.size for obj in objects},
        "colors": {
            (*obj.color_set.order_by("id").values_list("color_code", flat=True),)
            for obj in objects
        },
    }
    return render(request, "pages/catalog.html", context)


def product_detail_page(request, product_id):
    """
    View function for the product detail page.
    Fetches the product and its details (images, colors, sizes)
    and renders the HTML template.
    """
    # Prefetch related details for efficiency
    details_prefetch = Prefetch(
        "details",
        queryset=ProductDetails.objects.filter(stock__gt=0).prefetch_related(
            "productimages_set", "color_set", "size_set"
        ),
    )

    product = get_object_or_404(
        Products.objects.select_related("category").prefetch_related(details_prefetch),
        pk=product_id,
    )

    # Extract images from the prefetched details
    product_images = []
    details_list = []  # Also pass details to template for color/size info
    if product.details.exists():
        details_list = list(
            product.details.all()
        )  # Convert queryset to list for template
        for detail in details_list:
            product_images.extend(list(detail.productimages_set.all()))

    context = {
        "product": product,
        "product_images": product_images,
        "details": details_list,  # Pass details for color/size buttons
    }
    return render(request, "pages/product_detail.html", context)
