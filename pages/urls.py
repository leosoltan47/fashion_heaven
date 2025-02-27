from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("bag/", views.bag, name="bag"),
    path("featured/", views.blank_featured, name="blank_featured"),
    path("men/", views.blank_men, name="blank_men"),
    path("women/", views.blank_women, name="blank_women"),
    path("kids/", views.blank_kids, name="blank_kids"),
    path("shoes/", views.blank_shoes, name="blank_shoes"),
    path("outlet/", views.blank_outlet, name="blank_outlet"),
    path("products/<int:product_id>", views.product, name="product"),
]
