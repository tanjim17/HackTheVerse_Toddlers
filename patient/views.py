from django.shortcuts import render
from .models import *
from healthcare_workers.models import *
from datetime import datetime, timedelta
from django.http import HttpResponse
import logging
import threading
import time
from kafka import KafkaConsumer
import json

# Create your views here.
def func():
    print("Initializing Thread")
    consumer = KafkaConsumer('SensorData', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for msg in consumer:
        bed_id = msg.value['bed_id']
        heartbeat = msg.value['heartbeat']
        sys_bp = msg.value['sys_blood_pressure']
        dia_bp = msg.value['dias_blood_pressure']
        body_temp = msg.value['body_temp']
        oxygen_level = msg.value['oxygen_level']
        breathing_rate = msg.value['breathing_rate']
        timestamp = msg.timestamp

    # bed = Bed.objects.get(bedID=bedID)

    # recentDate = RecentMedicalData.objects.create(bed=bed, heartrate=heartrate, sys_bp=sys_bp, dia_bp=dia_bp, body_temp=body_temp, oxygen_level=oxygen_level, breathing_rate=breathing_rate, timestamp=timestamp)

    # result = HistoricalMedicalData.objects.filter(bed=bed)
    # if len(result) == 0 or result.latest('timestamp').timestamp + timedelta(seconds=900) < datetime.now():
    #     pass


def run_consumer_thread(request):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=func, daemon=True)
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    time.sleep(10)
    #x.join() # join would make the main thread to wait for the thread to end
    logging.info("Main    : all done")
    return HttpResponse('hello')