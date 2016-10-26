
from django.conf.urls import url, include

from main_app.views import HomePageView

urlpatterns = [
    url(r'^', HomePageView.as_view()),
]
