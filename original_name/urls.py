from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from .views import log_in, register

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("pages.urls")),
        path("login/", log_in, name="login"),
        path("register/", register, name="register"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + debug_toolbar_urls()
)
