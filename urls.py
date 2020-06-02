from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.views.generic.base import TemplateView, RedirectView
from homepage.views import homepage, error_404_view, error_401_view, error_500_view, health_check_view
from profiles.views import user_login, user_logout, register


urlpatterns = [
    url(r"^$", homepage, name="home"),
    url(r"^401$", error_401_view, name="401"),
    url(r"^404$", error_404_view, name="404"),
    url(r"^500$", error_500_view, name="500"),
    url(r"^health_check/$", health_check_view, name="health_check"),

    # user related pages
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout',),
    url(r'^register/$', register, name='register'),

    # submodule pages
    url(r"^profiles/", include("profiles.urls")),
    url(r"^simulations/", include("simulations.urls")),
    url(r"^protocols/", include("protocols.urls")),

    # admin
    url(settings.ADMIN_URL_BASE, admin.site.urls),

    # programming APIs
    url(r"^api/v1/", include('apiv1.urls', namespace="apiv1")),
    url(r'^api-auth/', include('rest_framework.urls')),

    # static pages
    url(r"^about/$", TemplateView.as_view(template_name='pages/faq.html'), name="about"),
    url(r"^terms/$", TemplateView.as_view(template_name='pages/terms.html'), name="terms"),
    url(r"^faq/$", TemplateView.as_view(template_name='pages/faq.html'), name="faq"),
    url(r"^help/$", TemplateView.as_view(template_name='pages/help.html'), name="help"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
