from django.shortcuts import render
from .models import *
from healthcare_workers.models import *
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
import logging
import threading
import time
from kafka import KafkaConsumer
import json
from django.shortcuts import reverse
from django.utils import timezone
import warnings
import pytz
from patient.analysis import condition_analyst

def check_usertype(request):
    if request.user.is_authenticated:
        if Doctor.objects.filter(user=request.user.id).exists():
            return 'doctor', Doctor.objects.get(user=request.user.id)
        elif Nurse.objects.filter(user=request.user.id).exists():
            return 'nurse', Nurse.objects.get(user=request.user.id)
        elif Reception.objects.filter(user=request.user.id).exists():
            return 'reception', Reception.objects.get(user=request.user.id)
        else:
            return 'admin', ' '
    else:
        return ' ', ' '

def doctor_nurse(bed_id):
    bed_id = int(bed_id)
    doctorID = Bed.objects.get(bedID=bed_id).doctor_fk.doctorID
    nurseID = Bed.objects.get(bedID=bed_id).nurse_fk.nurseID

    return doctorID, nurseID

def consumerUtil():
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    print("Initializing Thread")
    consumer = KafkaConsumer('SensorData', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    for msg in consumer:
        bed_id = int(msg.value['bed_id'])
        heartrate = int(msg.value['heartbeat'])
        sys_bp = int(msg.value['sys_blood_pressure'])
        dia_bp = int(msg.value['dias_blood_pressure'])
        body_temp = float(msg.value['body_temp'])
        oxygen_level = float(msg.value['oxygen_level'])*100
        breathing_rate = int(msg.value['breathing_rate'])
        timestamp = msg.timestamp/1000
        dt_obj = datetime.fromtimestamp(timestamp)

        condition_analyst(bed_id, heartrate, sys_bp, dia_bp, body_temp, oxygen_level, breathing_rate)

        bed = Bed.objects.get(bedID=bed_id)

        recentData = RecentMedicalData.objects.create(bed=bed, heartrate=heartrate, sys_bp=sys_bp, dia_bp=dia_bp, body_temp=body_temp, oxygen_level=oxygen_level, breathing_rate=breathing_rate, timestamp=dt_obj)

        result = RecentMedicalData.objects.filter(bed=bed)
        if len(result)==11:
            earliestData = result.earliest('timestamp')
            earliestData.delete()

        result = HistoricalMedicalData.objects.filter(bed=bed)

        if len(result) == 0 or result.latest('timestamp').timestamp + timedelta(seconds=1800) < pytz.utc.localize(datetime.now()):
            HistoricalMedicalData.objects.create(bed=bed, heartrate=heartrate, sys_bp=sys_bp, dia_bp=dia_bp, body_temp=body_temp, oxygen_level=oxygen_level, breathing_rate=breathing_rate, timestamp=dt_obj)

def run_consumer_thread(request):

    usertype, user = check_usertype(request)

    if usertype=='admin':

        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")

        logging.info("Main    : before creating thread")
        x = threading.Thread(target=consumerUtil, daemon=True)
        logging.info("Main    : before running thread")
        x.start()
        logging.info("Main    : wait for the thread to finish")
        #x.join() # join would make the main thread to wait for the thread to end
        logging.info("Main    : all done")
        return HttpResponseRedirect(reverse('dashboard'))

    else:
        return HttpResponseRedirect(reverse('home_page'))
