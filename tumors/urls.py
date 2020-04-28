from django.conf.urls import url

from tumors import views

urlpatterns = [
    url(r"^dashboard/$", views.dashboard, name="tumor_dashboard"),
    url(r"^(?P<tumor>[-\w]+)/$", views.tumor_view, name="tumor_view"),
]
