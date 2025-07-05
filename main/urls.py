from django.urls import path

from main.views import HomePageView
from main.rpc.server import server

app_name = 'main'

urlpatterns = [
    path(r'', HomePageView.as_view()),
    path('rpc', server.view),
]
