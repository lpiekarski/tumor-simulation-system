from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from core.models import BaseModel
from core.utils import media_file_path


class Profile(BaseModel):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, **kwargs):
        user_obj = User.objects.get(username=self.user.username)
        if self.email is not None:
            user_obj.email = self.email.strip()
        if self.first_name is not None:
            user_obj.first_name = self.first_name
        if self.last_name is not None:
            user_obj.last_name = self.last_name

        user_obj.save()
        super(Profile, self).save(**kwargs)
