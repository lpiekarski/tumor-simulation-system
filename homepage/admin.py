from django.contrib import admin

from homepage.models import Carousel


class CarouselAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups',)

    class Meta:
        model = Carousel


admin.site.register(Carousel, CarouselAdmin)
