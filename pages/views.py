from django.shortcuts import render
from .models import Products


# TODO: Add search bar that renders page specified in the search
def home(request):
    products = Products.objects.all()[:10]
    context = {"products": products}
    return render(request, "pages/home.html", context)
