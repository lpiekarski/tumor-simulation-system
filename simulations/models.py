from django.db import models
from django.contrib.auth.models import User
from protocols.models import Protocol
from django.conf import settings
from datetime import datetime, timezone
import requests
from core.utils import media_file_path, media_dir_path
import subprocess
import threading
import os
from PIL import Image
import shutil


def save_state_as_image(statestr, minval, maxval):
    save_filename = media_file_path(None, "state.png")
    os.makedirs(os.path.dirname(save_filename), exist_ok=True)
    img = Image.new('RGB', (51, 51), (0, 0, 0))
    statevals = ",".split(statestr)
    id = 0
    for x in range(51):
        for y in range(51):
            stateval = float(statevals[id])
            id = id + 1
            color = (stateval - minval) / (maxval - minval) * 255.
            color = int(color)
            if color < 0:
                color = 0
            if color > 255:
                color = 255
            img.putpixel((x, y), color)
    img.save(save_filename, 'PNG')
    return save_filename


def run_simulation(**kwargs):
    simulation = kwargs['simulation']
    automaton_file = kwargs['automaton_file']
    protocol_file_path = media_file_path(None, 'protocol.json')
    results_dir_path = media_dir_path()
    os.makedirs(results_dir_path, exist_ok=True)
    Protocol.to_file(simulation.protocol, protocol_file_path)
    subprocess.run([settings.SIMULATION_EXECUTABLE, automaton_file, protocol_file_path, results_dir_path, simulation.time_duration, '1'])
    os.remove(automaton_file)
    os.remove(protocol_file_path)
    output_dir = os.path.join(results_dir_path, '1', 'states')
    for state_filename in os.listdir(output_dir):
        with open(state_filename) as f:
            lines = f.readlines()
            time = int(lines[0])
            _W = lines[1]
            _W_img = save_state_as_image(_W, settings._W_min, settings._W_max)
            _CHO = lines[2]
            _CHO_img = save_state_as_image(_CHO, settings._CHO_min, settings._CHO_max)
            _OX = lines[3]
            _OX_img = save_state_as_image(_OX, settings._OX_min, settings._OX_max)
            _GI = lines[4]
            _GI_img = save_state_as_image(_GI, settings._GI_min, settings._GI_max)
            _timeInRepair = lines[5]
            _timeInRepair_img = save_state_as_image(_timeInRepair, settings._timeInRepair_min, settings._timeInRepair_max)
            _irradiation = lines[6]
            _irradiation_img = save_state_as_image(_irradiation, settings._irradiation_min, settings._irradiation_max)
            _cellState = lines[7]
            _cellState_img = save_state_as_image(_cellState, settings._cellState_min, settings._cellState_max)
            _cellCycle = lines[8]
            _cellCycle_img = save_state_as_image(_cellCycle, settings._cellCycle_min, settings._cellCycle_max)
            _proliferationTime = lines[9]
            _proliferationTime_img = save_state_as_image(_proliferationTime, settings._proliferationTime_min, settings._proliferationTime_max)
            _cycleChanged = lines[10]
            _cycleChanged_img = save_state_as_image(_cycleChanged, settings._cycleChanged_min, settings._cycleChanged_max)
            _G1time = lines[11]
            _G1time_img = save_state_as_image(_G1time, settings._G1time_min, settings._G1time_max)
            _Stime = lines[12]
            _Stime_img = save_state_as_image(_Stime, settings._Stime_min, settings._Stime_max)
            _G2time = lines[13]
            _G2time_img = save_state_as_image(_G2time, settings._G2time_min, settings._G2time_max)
            _Mtime = lines[14]
            _Mtime_img = save_state_as_image(_Mtime, settings._Mtime_min, settings._Mtime_max)
            _Dtime = lines[15]
            _Dtime_img = save_state_as_image(_Dtime, settings._Dtime_min, settings._Dtime_max)
            simulation_state = SimulationState(
                simulation=simulation,
                time=time,
                _W=_W,
                _W_img=_W_img,
                _CHO=_CHO,
                _CHO_img=_CHO_img,
                _OX=_OX,
                _OX_img=_OX_img,
                _GI=_GI,
                _GI_img=_GI_img,
                _timeInRepair=_timeInRepair,
                _timeInRepair_img=_timeInRepair_img,
                _irradiation=_irradiation,
                _irradiation_img=_irradiation_img,
                _cellState=_cellState,
                _cellState_img=_cellState_img,
                _cellCycle=_cellCycle,
                _cellCycle_img=_cellCycle_img,
                _proliferationTime=_proliferationTime,
                _proliferationTime_img=_proliferationTime_img,
                _cycleChanged=_cycleChanged,
                _cycleChanged_img=_cycleChanged_img,
                _G1time=_G1time,
                _G1time_img=_G1time_img,
                _Stime=_Stime,
                _Stime_img=_Stime_img,
                _G2time=_G2time,
                _G2time_img=_G2time_img,
                _Mtime=_Mtime,
                _Mtime_img=_Mtime_img,
                _Dtime=_Dtime,
                _Dtime_img=_Dtime_img)
            simulation_state.save()
    shutil.rmtree(results_dir_path, ignore_errors=True)


class Simulation(models.Model):
    name = models.CharField(max_length=100, blank=False)  # TODO: add validation for correct protocol
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations', null=False)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='simulations', null=False)
    description = models.TextField(null=False)
    time_duration = models.IntegerField(null=False)

    class Meta:
        verbose_name = 'Tumor Simulation'

    def __str__(self):
        return self.name

    @staticmethod
    def create_and_run(name, author, protocol, description, time_duration, automaton_file):
        simulation = Simulation(name=name, author=author, protocol=protocol, description=description, time_duration=time_duration)
        simulation.save()
        thread = threading.Thread(target=run_simulation, args=(), kwargs={'simulation': simulation, 'automaton_file': automaton_file})
        thread.start()


class SimulationState(models.Model):
    simulation = models.ForeignKey(to='Simulation', on_delete=models.CASCADE, related_name='state', null=False)
    time = models.IntegerField(verbose_name='Time', null=False)
    _W = models.TextField(null=False)
    _W_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _CHO = models.TextField(null=False)
    _CHO_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _OX = models.TextField(null=False)
    _OX_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _GI = models.TextField(null=False)
    _GI_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _timeInRepair = models.TextField(null=False)
    _timeInRepair_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _irradiation = models.TextField(null=False)
    _irradiation_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _cellState = models.TextField(null=False)
    _cellState_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _cellCycle = models.TextField(null=False)
    _cellCycle_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _proliferationTime = models.TextField(null=False)
    _proliferationTime_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _cycleChanged = models.TextField(null=False)
    _cycleChanged_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _G1time = models.TextField(null=False)
    _G1time_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _Stime = models.TextField(null=False)
    _Stime_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _G2time = models.TextField(null=False)
    _G2time_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _Mtime = models.TextField(null=False)
    _Mtime_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    _Dtime = models.TextField(null=False)
    _Dtime_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)

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
                    sserver.status = 'Stopped'
                    sserver.save()
            except requests.exceptions.HTTPError as e:
                sserver.status = 'Exception: ' + e.response.text
                sserver.save()
            except:
                sserver.status = 'Stopped'
                sserver.save()
                return

    class Meta:
        verbose_name = 'Simulation Server'
