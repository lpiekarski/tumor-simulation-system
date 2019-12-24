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
    full_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, **kwargs):
        user_obj = User.objects.get(username=self.user.username)
        if self.email is not None:
            user_obj.email = self.email.strip()

        user_obj.save()
        super(Profile, self).save(**kwargs)
