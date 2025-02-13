from django.shortcuts import render
from .models import Products


# TODO: Add HTML template to render main page
# TODO: Add search bar that renders page specified in the search
def home(request):
    products = Products.objects.all()
    context = {"enumerated_products": enumerate(products)}
    return render(request, "pages/home.html", context)
