import importlib.metadata

from django.views.generic.base import TemplateView

from modernrpc.core import registry


class HomePageView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        ctx = super(HomePageView, self).get_context_data(**kwargs)
        ctx.update({
            "modernrpc_version": importlib.metadata.metadata("django-modern-rpc")["Version"],
            "methods": registry.get_all_methods(sort_methods=True),
        })
        return ctx
