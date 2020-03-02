from django.conf.urls import url

from simulations import views

urlpatterns = [
    url(r"^dashboard/$", views.dashboard, name="simulation_dashboard"),
    url(r"^(?P<simulation>[-\w]+)/$", views.simulation_view, name="simulation_view"),
]