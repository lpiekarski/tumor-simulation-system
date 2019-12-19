from django.db import models

from core.fields import CreationDateTimeField, ModificationDateTimeField


class BaseModel(models.Model):
    created = CreationDateTimeField('created')
    modified = ModificationDateTimeField('modified')

    class Meta:
        abstract = True
