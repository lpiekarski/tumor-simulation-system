from django.conf import settings
from django.urls import reverse
from django.db.models import Max


def core_values(request):
    data = {
        'SITE_TITLE': getattr(settings, "SITE_TITLE", "CML"),
        'SITE_TITLE_FULL': getattr(settings, "SITE_TITLE_FULL", "Cancer Modeling Lab"),
        'MEDIA_PREFIX': getattr(settings, "MEDIA_URL", "/media/")
    }
    return data


def current_path(request):
    context = {}
    if request.path.strip() != reverse('logout'):
        context['current_path'] = request.path
    return context
