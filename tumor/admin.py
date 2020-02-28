from django.contrib import admin

from tumor.models import InitialTumor


class InitialTumorAdmin(admin.ModelAdmin):

    class Meta:
        model = InitialTumor


admin.site.register(InitialTumor, InitialTumorAdmin)
