from rest_framework import routers

from .viewsets import UserViewSet

app_name = "apiv1"

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls
