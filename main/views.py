import importlib.metadata

from django.views.generic.base import TemplateView

from main.rpc.server import server


class HomePageView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        ctx = super(HomePageView, self).get_context_data(**kwargs)
        dmr_version = importlib.metadata.metadata("django-modern-rpc")["Version"]
        ctx.update(
            {
                "modernrpc_version": dmr_version,
                "methods": sorted(
                    server.procedures.values(), key=lambda proc: proc.name
                ),
            }
        )
        return ctx
