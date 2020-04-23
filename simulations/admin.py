from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from simulations.models import InitialTumor, SimulationServer


class InitialTumorAdmin(GuardedModelAdmin):

    class Meta:
        model = InitialTumor


admin.site.register(InitialTumor, InitialTumorAdmin)
admin.site.register(SimulationServer)