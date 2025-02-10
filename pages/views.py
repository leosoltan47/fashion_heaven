from django.http import HttpResponse


# TODO: Add HTML template to render main page
# TODO: Add function to randomly (for now) select products to showcase on the main page
# TODO: Add search bar that renders page specified in the search
def index(request):
    return HttpResponse(b"You're on the index page hooray")
