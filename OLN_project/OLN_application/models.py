# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import hashlib
import os

# Create your models here.


def avatar_directory_path(instance, filename):
    sha_signature = hashlib.sha256(instance.user.username.encode()).hexdigest()
    _, ext = os.path.splitext(filename)
    return 'upload/{0}/{1}/avatar{2}'.format(sha_signature[:2], sha_signature[2:], ext)


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=avatar_directory_path, blank=True, null=True)

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


def carousel_image_directory_path(instance, filename):
    sha_signature = hashlib.sha256(instance.__str__().encode()).hexdigest()
    return 'image/{0}/{1}/carousel_item_{2}'.format(sha_signature[:2], sha_signature[2:], filename)


class CarouselItem(models.Model):
    image = models.ImageField(upload_to=carousel_image_directory_path, blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    is_public = models.BooleanField()

    def __str__(self):
        return "CarouselItem[" + self.image.__str__() + ", " + self.content.__str__() + "]"
