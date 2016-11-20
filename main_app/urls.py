
from django.conf.urls import url, include
from modernrpc.views import RPCEntryPoint

from main_app.views import HomePageView

urlpatterns = [
    url(r'^$', HomePageView.as_view()),
    url(r'^rpc', RPCEntryPoint.as_view(enable_doc=True)),
]
