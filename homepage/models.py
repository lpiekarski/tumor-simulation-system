from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from core.models import BaseModel
from core.utils import media_file_path


class Carousel(BaseModel):
    image = models.ImageField(
        upload_to=media_file_path,
        blank=True,
        null=True,
    )

    content = models.TextField(
        blank=True,
        null=True,
    )

    is_public = models.BooleanField(
        blank=True,
        null=True,
    )

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return settings.DEFAULT_CAROUSEL_IMAGE
