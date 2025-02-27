# TODO: Add logger and profiler to monitor performance
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import ProductDetails, Products


# TODO: Add search bar that renders page specified in the search
def home(request):
    in_stock = ProductDetails.objects.filter(stock__gt=0)  # type: ignore
    # Show 10 products that has at least one variant
    # as information like color are stored in variants
    products = (
        Products.objects.filter(category__isnull=False)  # type: ignore
        .prefetch_related(Prefetch("details", queryset=in_stock))
        .distinct()
        .filter(details__isnull=False)
        .order_by("id")[:10]
    )
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


def wishlist(request):
    """
    View function for the wishlist page.
    """
    return render(request, "pages/wishlist.html")


def bag(request):
    """
    View function for the shopping bag page.
    """
    return render(request, "pages/bag.html")


def blank_featured(request):
    """
    View function for the blank featured page.
    """
    return render(request, "pages/blank_featured.html")


def blank_men(request):
    """
    View function for the blank men's page.
    """
    return render(request, "pages/blank_men.html")


def blank_women(request):
    """
    View function for the blank women's page.
    """
    return render(request, "pages/blank_women.html")


def blank_kids(request):
    """
    View function for the blank kids' page.
    """
    return render(request, "pages/blank_kids.html")


def blank_shoes(request):
    """
    View function for the blank shoes page.
    """
    return render(request, "pages/blank_shoes.html")


def blank_outlet(request):
    """
    View function for the blank outlet page.
    """
    return render(request, "pages/blank_outlet.html")
