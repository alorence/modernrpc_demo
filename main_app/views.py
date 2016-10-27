import modernrpc
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = 'main_app/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomePageView, self).get_context_data(**kwargs)
        ctx.update({
            'modernrpc_version': modernrpc.__version__
        })
        return ctx