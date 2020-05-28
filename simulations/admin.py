from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from simulations.models import SimulationServer, Simulation

admin.site.register(Simulation)
admin.site.register(SimulationServer)
