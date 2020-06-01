from django.conf.urls import url

from simulations import views

urlpatterns = [
    url(r"^dashboard/$", views.dashboard, name="simulation_dashboard"),
    url(r"^create/$", views.simulation_create, name="simulation_create"),
    url(r"^servers/$", views.sserver_dashboard, name="sserver_dashboard"),
    url(r"^(?P<simulation>[-\w]+)/$", views.simulation_view, name="simulation_view"),
]
