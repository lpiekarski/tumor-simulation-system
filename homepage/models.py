from django.db import models
from django.urls import reverse

from core.models import BaseModel
from core.utils import media_file_path


class Carousel(BaseModel):
    image = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    content = models.TextField()
    is_public = models.BooleanField()

