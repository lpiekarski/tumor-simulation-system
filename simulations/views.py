from simulations.models import Protocol

from core.utils import render_with_context


def user_simulations_view(request, template_name="simulations/simulations.html"):
    return render_with_context(request, template_name, {})


def user_protocols_view(request, template_name="simulations/protocols.html"):
    return render_with_context(request, template_name, {})


def simulation_detail(request, simulation, template_name="simulations/simulation.html"):
    return render_with_context(request, template_name, {})
