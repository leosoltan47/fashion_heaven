# TODO: Add logger and profiler to monitor performance
from django.db.models import Prefetch
from django.shortcuts import render
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
