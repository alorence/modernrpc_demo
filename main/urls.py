from django.urls import path

from main.rpc.server import server
from main.views import HomePageView


app_name = "main"

urlpatterns = [
    path(r"", HomePageView.as_view()),
    path("rpc", server.view),
    path("async-rpc", server.async_view),
]
