"""modernrpc_demo URL Configuration"""

from django.urls import path, include

from core import settings


urlpatterns = [
    path("", include("main.urls")),
]

if "django_browser_reload" in settings.INSTALLED_APPS:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
