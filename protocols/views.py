from django.core.exceptions import MultipleObjectsReturned
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import get_object_or_404
from protocols.models import Protocol, ProtocolDose

from core.utils import render_with_context


def dashboard(request, template_name="protocols/dashboard.html"):
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
        }
        protocol_data.append(pd)
    return render_with_context(request, template_name, {"protocol_data": protocol_data})


def protocol_view(request, protocol, template_name="protocols/protocol.html"):
    try:
        protocol_object = get_object_or_404(Protocol, id=protocol)
    except MultipleObjectsReturned:
        protocol_object = Protocol.objects.filter(id=protocol).latest('pk')
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
        "protocol": protocol_object,
        "doses": doses,
        "total_radiation_intake": tri,
        "first_dose_time": first_dose_time,
        "last_dose_time": last_dose_time,
        "max_dose": max_dose,
    }
    return render_with_context(request, template_name, {'pd': pd})


def protocol_edit(request, protocol, template_name="protocols/edit.html"):
    return render_with_context(request, template_name, {})


def protocol_create(request, template_name="protocols/protocol_create.html"):
    return render_with_context(request, template_name, {})
