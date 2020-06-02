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
    save_media_path = media_file_path(None, "state.png")
    save_filename = os.path.join(settings.MEDIA_ROOT, save_media_path)
    img = Image.new('RGB', (51, 51), (0, 0, 0))
    statevals = statestr.split(",")
    #print(statevals)
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
            img.putpixel((x, y), (color, color, color))
    img.save(save_filename, 'PNG')
    return save_media_path


def run_simulation(**kwargs):
    simulation = kwargs['simulation']
    automaton_file = kwargs['automaton_file']
    protocol_file_path = os.path.join(settings.MEDIA_ROOT, media_file_path(None, 'protocol.json'))
    results_dir_path = os.path.join(settings.MEDIA_ROOT, media_dir_path())
    os.makedirs(results_dir_path, exist_ok=True)
    Protocol.to_file(simulation.protocol, protocol_file_path)
    subprocess.run([settings.SIMULATION_EXECUTABLE, automaton_file, protocol_file_path, results_dir_path, str(simulation.time_duration), '1'])
    os.remove(automaton_file)
    os.remove(protocol_file_path)
    output_dir = os.path.join(results_dir_path, '1', 'states')
    for state_filename in os.listdir(output_dir):
        with open(os.path.join(output_dir, state_filename)) as f:
            lines = f.readlines()
            time = int(lines[0])
            W = lines[1]
            W_img = save_state_as_image(W, settings.SIMULATION_IMAGE_SETTINGS['SIMW_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMW_max'])
            CHO = lines[2]
            CHO_img = save_state_as_image(CHO, settings.SIMULATION_IMAGE_SETTINGS['SIMCHO_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMCHO_max'])
            OX = lines[3]
            OX_img = save_state_as_image(OX, settings.SIMULATION_IMAGE_SETTINGS['SIMOX_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMOX_max'])
            GI = lines[4]
            GI_img = save_state_as_image(GI, settings.SIMULATION_IMAGE_SETTINGS['SIMGI_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMGI_max'])
            timeInRepair = lines[5]
            timeInRepair_img = save_state_as_image(timeInRepair, settings.SIMULATION_IMAGE_SETTINGS['SIMtimeInRepair_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMtimeInRepair_max'])
            irradiation = lines[6]
            irradiation_img = save_state_as_image(irradiation, settings.SIMULATION_IMAGE_SETTINGS['SIMirradiation_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMirradiation_max'])
            cellState = lines[7]
            cellState_img = save_state_as_image(cellState, settings.SIMULATION_IMAGE_SETTINGS['SIMcellState_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMcellState_max'])
            cellCycle = lines[8]
            cellCycle_img = save_state_as_image(cellCycle, settings.SIMULATION_IMAGE_SETTINGS['SIMcellCycle_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMcellCycle_max'])
            proliferationTime = lines[9]
            proliferationTime_img = save_state_as_image(proliferationTime, settings.SIMULATION_IMAGE_SETTINGS['SIMproliferationTime_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMproliferationTime_max'])
            cycleChanged = lines[10]
            cycleChanged_img = save_state_as_image(cycleChanged, settings.SIMULATION_IMAGE_SETTINGS['SIMcycleChanged_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMcycleChanged_max'])
            G1time = lines[11]
            G1time_img = save_state_as_image(G1time, settings.SIMULATION_IMAGE_SETTINGS['SIMG1time_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMG1time_max'])
            Stime = lines[12]
            Stime_img = save_state_as_image(Stime, settings.SIMULATION_IMAGE_SETTINGS['SIMStime_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMStime_max'])
            G2time = lines[13]
            G2time_img = save_state_as_image(G2time, settings.SIMULATION_IMAGE_SETTINGS['SIMG2time_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMG2time_max'])
            Mtime = lines[14]
            Mtime_img = save_state_as_image(Mtime, settings.SIMULATION_IMAGE_SETTINGS['SIMMtime_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMMtime_max'])
            Dtime = lines[15]
            Dtime_img = save_state_as_image(Dtime, settings.SIMULATION_IMAGE_SETTINGS['SIMDtime_min'], settings.SIMULATION_IMAGE_SETTINGS['SIMDtime_max'])
            simulation_state = SimulationState(
                simulation=simulation,
                time=time,
                W=W,
                W_img=W_img,
                CHO=CHO,
                CHO_img=CHO_img,
                OX=OX,
                OX_img=OX_img,
                GI=GI,
                GI_img=GI_img,
                timeInRepair=timeInRepair,
                timeInRepair_img=timeInRepair_img,
                irradiation=irradiation,
                irradiation_img=irradiation_img,
                cellState=cellState,
                cellState_img=cellState_img,
                cellCycle=cellCycle,
                cellCycle_img=cellCycle_img,
                proliferationTime=proliferationTime,
                proliferationTime_img=proliferationTime_img,
                cycleChanged=cycleChanged,
                cycleChanged_img=cycleChanged_img,
                G1time=G1time,
                G1time_img=G1time_img,
                Stime=Stime,
                Stime_img=Stime_img,
                G2time=G2time,
                G2time_img=G2time_img,
                Mtime=Mtime,
                Mtime_img=Mtime_img,
                Dtime=Dtime,
                Dtime_img=Dtime_img)
            simulation_state.save()
    shutil.rmtree(results_dir_path, ignore_errors=True)
    print('simulation done.')


class Simulation(models.Model):
    name = models.CharField(max_length=100, blank=False)
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
    simulation = models.ForeignKey(to='Simulation', on_delete=models.CASCADE, related_name='states', null=False)
    time = models.IntegerField(verbose_name='Time', null=False)
    W = models.TextField(null=False)
    W_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    CHO = models.TextField(null=False)
    CHO_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    OX = models.TextField(null=False)
    OX_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    GI = models.TextField(null=False)
    GI_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    timeInRepair = models.TextField(null=False)
    timeInRepair_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    irradiation = models.TextField(null=False)
    irradiation_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    cellState = models.TextField(null=False)
    cellState_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    cellCycle = models.TextField(null=False)
    cellCycle_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    proliferationTime = models.TextField(null=False)
    proliferationTime_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    cycleChanged = models.TextField(null=False)
    cycleChanged_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    G1time = models.TextField(null=False)
    G1time_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    Stime = models.TextField(null=False)
    Stime_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    G2time = models.TextField(null=False)
    G2time_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    Mtime = models.TextField(null=False)
    Mtime_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)
    Dtime = models.TextField(null=False)
    Dtime_img = models.ImageField(upload_to=media_file_path, blank=True, null=True)

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
