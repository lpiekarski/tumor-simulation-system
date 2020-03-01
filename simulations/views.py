from guardian.shortcuts import get_objects_for_user

from simulations.models import Protocol, ProtocolDose

from core.utils import render_with_context


def user_simulations_view(request, template_name="simulations/simulations.html"):
    return render_with_context(request, template_name, {})


def user_protocols_view(request, template_name="simulations/protocols.html"):
    protocols = get_objects_for_user(
        request.user,
        "simulations.view_protocol"
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
        }
        protocol_data.append(pd)
    return render_with_context(request, template_name, {"protocol_data": protocol_data})


def simulation_detail(request, simulation, template_name="simulations/simulation.html"):
    return render_with_context(request, template_name, {})
