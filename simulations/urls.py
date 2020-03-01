from django.conf.urls import url

from simulations import views

urlpatterns = [
    url(r"^dashboard/$", views.user_simulations_view, name="user_simulations_view"),
    url(r"^protocols/$", views.user_protocols_view, name="user_protocols_view"),
    url(r"^(?P<simulation>[-\w]+)/$", views.simulation_detail, name="simulation_detail"),
]
