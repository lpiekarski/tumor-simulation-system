# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from OLN_application.models import UserProfileInfo, User, Article, CarouselItem

# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(Article)
admin.site.register(CarouselItem)
