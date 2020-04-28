from django.db import models
from core.utils import media_file_path


class Tumor(models.Model):
    name = models.CharField(max_length=100, blank=False)
    file = models.FileField(upload_to='media_file_path')  # TODO: add validation check for correct tumor file

    class Meta:
        verbose_name = 'Tumor'

    def __str__(self):
        return self.name
