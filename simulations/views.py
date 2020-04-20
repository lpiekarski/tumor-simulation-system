from guardian.shortcuts import get_objects_for_user
from simulations.models import Simulation, SimulationState
from core.utils import render_with_context


def dashboard(request, template_name="simulations/dashboard.html"):
    simulations = get_objects_for_user(
        request.user,
        "simulations.view_simulation"
    ).union(Simulation.objects.filter(author=request.user))
    return render_with_context(request, template_name, {"simulations": simulations})


def simulation_view(request, simulation, template_name="simulations/simulation.html"):
    return render_with_context(request, template_name, {})
