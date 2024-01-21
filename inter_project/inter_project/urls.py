from django.contrib import admin
from django.urls import path, include
from banking_app.views import homepage


urlpatterns = [
    path("", homepage),
    path("api/", include("banking_app.urls")),
    path("admin/", admin.site.urls),
]
