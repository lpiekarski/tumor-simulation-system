from django.contrib import admin

from homepage.models import Carousel


class CarouselAdmin(admin.ModelAdmin):
    class Meta:
        model = Carousel


admin.site.register(Carousel, CarouselAdmin)
