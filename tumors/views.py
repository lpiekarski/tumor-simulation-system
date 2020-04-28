from guardian.shortcuts import get_objects_for_user
from simulations.models import Simulation, SimulationState, SimulationServer
from core.utils import render_with_context
from datetime import datetime
from django.conf import settings


def dashboard(request, template_name="tumors/dashboard.html"):
    tumors = get_objects_for_user(
        request.user,
        "tumors.view_tumor"
    ).union(Simulation.objects.filter(author=request.user))
    return render_with_context(request, template_name, {"tumors": tumors})


def tumor_view(request, tumor, template_name="tumors/tumor.html"):
    return render_with_context(request, template_name, {})

