from django.core.exceptions import MultipleObjectsReturned
from guardian.shortcuts import get_objects_for_user
from simulations.models import Simulation, SimulationState, SimulationServer
from protocols.models import ProtocolDose, Protocol
from core.utils import render_with_context
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
from django.conf import settings
from homepage.views import error_401_view
from core.utils import media_file_path
from simulations.models import run_simulation
import os


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
        first_state = SimulationState.objects.filter(simulation=simulation).order_by('time').first()
        images1 = []
        images2 = []
        images3 = []
        if first_state is not None:
            images1.append(first_state._W_img)
            images1.append(first_state._CHO_img)
            images1.append(first_state._OX_img)
            images1.append(first_state._GI_img)
            images1.append(first_state._timeInRepair_img)
            images2.append(first_state._irradiation_img)
            images2.append(first_state._cellState_img)
            images2.append(first_state._cellCycle_img)
            images2.append(first_state._proliferationTime_img)
            images2.append(first_state._cycleChanged_img)
            images3.append(first_state._G1time_img)
            images3.append(first_state._Stime_img)
            images3.append(first_state._G2time_img)
            images3.append(first_state._Mtime_img)
            images3.append(first_state._Dtime_img)
        sd = {
            "simulation": simulation,
            "images1": images1,
            "images2": images2,
            "images3": images3,
            "pd": pd
        }
        simulation_data.append(sd)
    return render_with_context(request, template_name, {'simulation_data': simulation_data})


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


def simulation_create(request, template_name="simulations/create.html"):
    if not request.user.has_perm("protocols.create_simulation"):
        return error_401_view(request)
    if request.method == 'POST':
        protocol_id = request.POST.get("protocol_id")
        try:
            protocol = get_object_or_404(Protocol, id=protocol_id)
        except MultipleObjectsReturned:
            protocol = Protocol.objects.filter(id=protocol_id).latest('pk')
        name = request.POST.get("name")
        time_duration = request.POST.get("time_duration")
        description = request.POST.get("description")
        automaton_file = request.FILES.get("automaton_file")
        automaton_saved = os.path.join(settings.MEDIA_ROOT, media_file_path(None, "automaton.json"))
        with open(automaton_saved, 'wb+') as destination:
            for chunk in automaton_file.chunks():
                destination.write(chunk)
        Simulation.create_and_run(name, request.user, protocol, description, int(time_duration), automaton_saved)
        return redirect('simulation_dashboard')
    else:
        protocols = get_objects_for_user(
            request.user,
            "protocols.view_protocol"
        ).union(Protocol.objects.filter(author=request.user))
        protocol_data = []
        for protocol in protocols:
            tri = 0
            max_dose = 0
            first_dose_time = None
            last_dose_time = None
            doses = ProtocolDose.objects.filter(protocol=protocol)
            for dose in doses:
                tri += dose.dose
                if max_dose < dose.dose:
                    max_dose = dose.dose
                if first_dose_time is None or first_dose_time > dose.time:
                    first_dose_time = dose.time
                if last_dose_time is None or last_dose_time < dose.time:
                    last_dose_time = dose.time
            pd = {
                "protocol": protocol,
                "doses": doses,
                "total_radiation_intake": tri,
                "first_dose_time": first_dose_time,
                "last_dose_time": last_dose_time,
                "max_dose": max_dose,
                "time_step": settings.PROTOCOL_TIME_STEP,
            }
            protocol_data.append(pd)
        form_data = {
            "protocol_data": protocol_data
        }
        return render_with_context(request, template_name, form_data)
