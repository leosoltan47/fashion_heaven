from django.urls import path, re_path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("wishlist/", views.empty_wishlist, name="wishlist"),
    re_path(
        r"wishlist/(?P<id_list>(?:ids\[\]=\d+&?)+)", views.wishlist, name="wishlist"
    ),
    path("bag/", views.bag, name="bag"),
    path("bag/<str:ids>", views.bag, name="bag"),
    path("catalog/<str:title>", views.catalog, name="catalog"),
    path("catalog/<str:title>/<str:search>", views.catalog, name="catalog"),
    path("products/<int:product_id>", views.product, name="product"),
    path(
        "product-detail/<int:product_id>",
        views.product_detail_page,
        name="product_detail_page",
    ),
    path("support/", views.support_page, name="support"),
    path("returns-exchanges/", views.returns_exchanges_view, name="returns_exchanges"),
]
