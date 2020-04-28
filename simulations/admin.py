from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from simulations.models import SimulationServer

admin.site.register(SimulationServer)
