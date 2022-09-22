from django.urls import path
from modernrpc.views import RPCEntryPoint

from main.views import HomePageView

app_name = 'main'

urlpatterns = [
    path(r'', HomePageView.as_view()),
    path('rpc', RPCEntryPoint.as_view(enable_doc=True)),
]
