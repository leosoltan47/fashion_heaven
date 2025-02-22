from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("bag/", views.bag, name="bag"),
]
