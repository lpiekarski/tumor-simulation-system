from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import UserSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer