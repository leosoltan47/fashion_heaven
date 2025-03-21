from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("wishlist/", views.empty_wishlist, name="wishlist"),
    path("wishlist/<str:id_list>", views.wishlist, name="wishlist"),
    path("bag/", views.bag, name="bag"),
    path("catalog/<str:title>", views.catalog, name="catalog"),
    path("products/<int:product_id>", views.product, name="product"),
]
