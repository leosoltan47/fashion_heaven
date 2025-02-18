# TODO: Add logger and profiler to monitor performance
from django.db.models import Prefetch
from django.shortcuts import render
from .models import ProductDetails, Products


# TODO: Add search bar that renders page specified in the search
def home(request):
    in_stock = ProductDetails.objects.filter(stock__gt=0)
    # Show at max 10 products that has at least one variant
    # as information like color are stored in variants
    products = (
        Products.objects.filter(category__isnull=False)
        .prefetch_related(Prefetch("details", queryset=in_stock))
        .distinct()
        .filter(details__isnull=False)
        .order_by("id")[:10]
    )
    categories = set(product.category for product in products)
    context = {"products": products, "categories": categories}
    return render(request, "pages/home.html", context)
