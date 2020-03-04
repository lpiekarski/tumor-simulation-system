from django.core.exceptions import MultipleObjectsReturned
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import get_object_or_404, redirect
from protocols.models import Protocol, ProtocolDose
from django.conf import settings
from homepage.views import error_401_view

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
            "time_step": settings.PROTOCOL_TIME_STEP,
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
        "time_step": settings.PROTOCOL_TIME_STEP,
    }
    return render_with_context(request, template_name, {'pd': pd})


def protocol_edit(request, protocol, template_name="protocols/edit.html"):
    try:
        protocol_object = get_object_or_404(Protocol, id=protocol)
    except MultipleObjectsReturned:
        protocol_object = Protocol.objects.filter(id=protocol).latest('pk')
    if not request.user.has_perm("protocols.change_protocol", protocol_object):
        return error_401_view(request)
    if request.method == 'POST':
        doses = request.POST.getlist("dose[]")
        times = request.POST.getlist("time[]")
        name = request.POST.get("name") # TODO protocol validation
        protocol_object.name = name
        protocol_object.save()
        ProtocolDose.objects.filter(protocol=protocol).delete()
        for i in range(0, len(times)):
            ProtocolDose(protocol=protocol_object, time=times[i], dose=doses[i]).save()
        return redirect('protocol_view', protocol)
    else:
        doses = ProtocolDose.objects.filter(protocol=protocol)
        doses_table = []
        for dose in doses:
            doses_table.append({"time": dose.time, "dose": dose.dose})

        pd = {
            "protocol": protocol_object,
            "name": protocol_object.name,
            "doses": doses_table,
            "time_step": settings.PROTOCOL_TIME_STEP,
        }
        return render_with_context(request, template_name, {'pd': pd})


def protocol_create(request, template_name="protocols/create.html"):
    return render_with_context(request, template_name, {})
