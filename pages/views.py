# TODO: Add logger and profiler to monitor performance
from django.shortcuts import render
from .models import Products


# TODO: Add search bar that renders page specified in the search
def home(request):
    # Home page is designed to show 10 products
    # FIXME: Severe performance hit due to this query
    products = Products.objects.prefetch_related("productdetails_set").all()[:10]
    context = {"products": products}
    return render(request, "pages/home.html", context)
