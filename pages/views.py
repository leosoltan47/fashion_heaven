from django.shortcuts import render


# TODO: Add HTML template to render main page
# TODO: Add function to randomly (for now) select products to showcase on the main page
# TODO: Add search bar that renders page specified in the search
def home(request):
    return render(request, "pages/home.html")
