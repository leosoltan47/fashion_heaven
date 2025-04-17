# TODO: Add logger and profiler to monitor performance
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import ProductDetails, Products
import re


# TODO: Add search bar that renders page specified in the search
def home(request):
    in_stock = ProductDetails.objects.filter(stock__gt=0)
    # Show 10 products that has at least one variant
    # as information like color are stored in variants
    objects = (
        Products.objects.filter(category__isnull=False)
        .prefetch_related(Prefetch("details", queryset=in_stock))
        .distinct()
        .filter(details__isnull=False)
        .order_by("id")[:10]
    )
    products = [
        {
            "id": obj.pk,
            "name": obj.name,
            "price": obj.price_in_dollars,
            "colors": [
                [color.color_code for color in image.color_set.all()]
                for variant in obj.details.all()
                for image in variant.productimages_set.all()
            ],
        }
        for obj in objects
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
    context = {"title": title}
    return render(request, "pages/catalog.html", context)


def featured_page(request):
    """
    View function for the featured collection page.
    """
    context = {}
    return render(request, "pages/blank_featured.html", context)
