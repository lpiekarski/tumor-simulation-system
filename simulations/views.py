from guardian.shortcuts import get_objects_for_user
from simulations.models import Simulation, SimulationState, SimulationServer
from core.utils import render_with_context
from datetime import datetime
from django.conf import settings


def dashboard(request, template_name="simulations/dashboard.html"):
    simulations = get_objects_for_user(
        request.user,
        "simulations.view_simulation"
    ).union(Simulation.objects.filter(author=request.user))
    return render_with_context(request, template_name, {"simulations": simulations})


def simulation_view(request, simulation, template_name="simulations/simulation.html"):
    return render_with_context(request, template_name, {})


def sserver_dashboard(request, template_name="simulations/sserver_dashboard.html"):
    sservers = get_objects_for_user(
        request.user,
        "simulations.view_simulationserver"
    )
    refresh_time = datetime.now()
    for sserver in sservers:
        SimulationServer.refresh_status(sserver)

    return render_with_context(request, template_name, {"sservers": sservers})
