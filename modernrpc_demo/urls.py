"""modernrpc_demo URL Configuration"""
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('__reload__/', include('django_browser_reload.urls')))
