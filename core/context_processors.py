from django.conf import settings
from django.urls import reverse
from django.db.models import Max


def core_values(request):
    data = {
        'SITE_TITLE': getattr(settings, "SITE_TITLE", "TSS"),
        'SITE_TITLE_FULL': getattr(settings, "SITE_TITLE_FULL", "Tumor Simulation System"),
        'MEDIA_PREFIX': getattr(settings, "MEDIA_URL", "/media/")
    }
    return data


def current_path(request):
    context = {}
    if request.path.strip() != reverse('logout'):
        context['current_path'] = request.path
    return context
