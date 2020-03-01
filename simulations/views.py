from guardian.shortcuts import get_objects_for_user

from core.utils import render_with_context


def dashboard(request, template_name="simulations/dashboard.html"):
    return render_with_context(request, template_name, {})


def simulation_view(request, simulation, template_name="simulations/simulation.html"):
    return render_with_context(request, template_name, {})
