from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from tumors.models import Tumor

admin.site.register(Tumor)
