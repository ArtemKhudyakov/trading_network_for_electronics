from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("users/", include("users.urls", namespace="users")),
]
