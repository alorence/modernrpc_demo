from django.conf import settings
from django.http import HttpRequest


def main(_: HttpRequest) -> dict:
    global_context = {
        "debug": settings.DEBUG,
        "sentry_loader_script": getattr(settings, "SENTRY_LOADER_SCRIPT", ""),
    }
    return global_context
