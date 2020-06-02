from django.conf.urls import url

from profiles import views

urlpatterns = [
    url(r"^edit/$", views.profile_edit, name="profile_edit"),
    url(r"^(?P<username>[-\w]+)/$", views.profile_view, name="profile_view"),
]
