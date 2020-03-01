from django.conf.urls import url

from protocols import views

urlpatterns = [
    url(r"^dashboard/$", views.dashboard, name="protocol_dashboard"),
    url(r"^(?P<protocol>[-\w]+)/$", views.protocol_view, name="protocol_view"),
    url(r"^(?P<protocol>[-\w]+)/edit/$", views.protocol_edit, name="protocol_edit"),
    url(r"^create/$", views.protocol_create, name="protocol_create"),
]
