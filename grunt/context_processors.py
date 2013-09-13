from django.conf import settings

from .conf import grunt_conf


def grunt_config(request):
    return grunt_conf(
        key=getattr(settings, "GRUNT_TEMPLATE_CONTEXT_KEY", None))
