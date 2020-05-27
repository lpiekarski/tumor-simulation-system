from django.db import models
from django.contrib.auth.models import User
from protocols.models import Protocol
from django.conf import settings
from datetime import datetime, timezone
import requests


class Simulation(models.Model):
    name = models.CharField(max_length=100, blank=False)  # TODO: add validation for correct protocol
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations', null=False)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='simulations', null=False)
    description = models.TextField(null=False)
    time_duration = models.FloatField(null=False)

    class Meta:
        verbose_name = 'Tumor Simulation'

    def __str__(self):
        return self.name


class SimulationState(models.Model):
    simulation = models.ForeignKey(to='Simulation', on_delete=models.CASCADE, related_name='state', null=False)
    time = models.IntegerField(verbose_name='Time', null=False)
    _W = models.TextField(null=False)
    _CHO = models.TextField(null=False)
    _OX = models.TextField(null=False)
    _GI = models.TextField(null=False)
    _timeInRepair = models.TextField(null=False)
    _irradiation = models.TextField(null=False)
    _cellState = models.TextField(null=False)
    _cellCycle = models.TextField(null=False)
    _proliferationTime = models.TextField(null=False)
    _cycleChanged = models.TextField(null=False)
    _G1time = models.TextField(null=False)
    _Stime = models.TextField(null=False)
    _G2time = models.TextField(null=False)
    _Mtime = models.TextField(null=False)
    _Dtime = models.TextField(null=False)

    class Meta:
        verbose_name = 'Simulation State'


class SimulationServer(models.Model):
    name = models.CharField(max_length=100, blank=False)
    url = models.CharField(max_length=255, blank=False)
    status = models.CharField(max_length=255, blank=True, null=True, default='Stopped')
    status_update_time = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def refresh_status(sserver):
        refresh_time = datetime.now(timezone.utc)
        if sserver.status_update_time is None or (refresh_time - sserver.status_update_time).total_seconds() >= settings.SSERVER_REFRESH_RATE:
            try:
                url = sserver.url
                if not url.startswith('http'):
                    url = 'http://' + url
                if not url.endswith('/'):
                    url = url + '/'
                url = url + 'status'
                print(url)
                response = requests.post(url=url, data='[]')
                if response.status_code == 200 and response.json()['status'] == 'ok':
                    if response.json()['result']['status'] == 'idle':
                        sserver.status = 'Running'
                    elif response.json()['result']['status'] == 'running':
                        sserver.status = 'Running'
                    elif response.json()['result']['status'] == 'finished':
                        sserver.status = 'Running'
                    else:
                        sserver.status = 'Stopped'
                    sserver.status_update_time = refresh_time
                    sserver.save()
                else:
                    sserver.status = 'Code: ' + str(response.status_code)
                    sserver.save()
            except requests.exceptions.HTTPError as e:
                sserver.status = 'Exception: ' + e.response.text
                sserver.save()
            except:
                sserver.status = 'Unknown exception'
                sserver.save()
                return

    class Meta:
        verbose_name = 'Simulation Server'
