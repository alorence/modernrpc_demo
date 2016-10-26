from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = 'main_app/home.html'
