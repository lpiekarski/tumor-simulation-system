from django.conf import settings
from django.urls import reverse
from django.db.models import Max


def core_values(request):
    data = {
        'SITE_TITLE': getattr(settings, "SITE_TITLE", "Tumour Treatment Optimisation - Web App For Doctors"),
    }
    return data


def current_path(request):
    context = {}
    if request.path.strip() != reverse('logout'):
        context['current_path'] = request.path
    return context
