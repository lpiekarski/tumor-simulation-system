# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


#class CellularAutomatonState(models.Model):
#    pass


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    is_public = models.BooleanField()

    def __str__(self):
        return "Article[" + self.title.__str__() + ", " + self.author.__str__() + "]"
