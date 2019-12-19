from django.conf.urls import url

from profiles import views

urlpatterns = [
#    url(r"^edit/$", views.ProfileEditUpdateView.as_view(), "profile_edit"),
    url(r"^(?P<username>[-\w]+)/$", views.profile_detail, name="profile_detail"),
]
