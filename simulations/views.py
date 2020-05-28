from django.core.exceptions import MultipleObjectsReturned
from guardian.shortcuts import get_objects_for_user
from simulations.models import Simulation, SimulationState, SimulationServer
from protocols.models import ProtocolDose
from core.utils import render_with_context
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
from django.conf import settings


def dashboard(request, template_name="simulations/dashboard.html"):
    simulations = get_objects_for_user(
        request.user,
        "simulations.view_simulation"
    ).union(Simulation.objects.filter(author=request.user))
    simulation_data = []
    for simulation in simulations:
        tri = 0
        max_dose = 0
        first_dose_time = None
        last_dose_time = None
        doses = ProtocolDose.objects.filter(protocol=simulation.protocol)
        for dose in doses:
            tri += dose.dose
            if max_dose < dose.dose:
                max_dose = dose.dose
            if first_dose_time is None or first_dose_time > dose.time:
                first_dose_time = dose.time
            if last_dose_time is None or last_dose_time < dose.time:
                last_dose_time = dose.time
        pd = {
            "protocol": simulation.protocol,
            "doses": doses,
            "total_radiation_intake": tri,
            "first_dose_time": first_dose_time,
            "last_dose_time": last_dose_time,
            "max_dose": max_dose,
            "time_step": settings.PROTOCOL_TIME_STEP,
        }
        sd = {
            "simulation": simulation,
            "pd": pd
        }
        simulation_data.append(sd)
    return render_with_context(request, template_name, {"simulation_data": simulation_data})


def simulation_view(request, simulation, template_name="simulations/simulation.html"):
    try:
        simulation_object = get_object_or_404(Simulation, id=simulation)
    except MultipleObjectsReturned:
        simulation_object = Simulation.objects.filter(id=simulation).latest('pk')
    sd = {
    }
    return render_with_context(request, template_name, {'sd': sd})


def sserver_dashboard(request, template_name="simulations/sserver_dashboard.html"):
    sservers = get_objects_for_user(
        request.user,
        "simulations.view_simulationserver"
    )
    refresh_time = datetime.now()
    for sserver in sservers:
        SimulationServer.refresh_status(sserver)

    return render_with_context(request, template_name, {"sservers": sservers})
