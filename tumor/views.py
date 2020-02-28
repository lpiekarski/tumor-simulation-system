from django.shortcuts import render
from tumor.models import InitialTumor, Protocol


def simulation_view(request):
    return render(request, 'tumor/simulation.html', {})
