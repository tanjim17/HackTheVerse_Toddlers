from django.shortcuts import render
from .models import *
from healthcare_workers.models import *
from datetime import datetime, timedelta

# Create your views here.
def func():

    # bedID =
    # heartrate =
    # sys_bp =
    # dia_bp =
    # body_temp =
    # oxygen_level =
    # breathing_rate =
    # timestamp =

    # bed = Bed.objects.get(bedID=bedID)

    # recentDate = RecentMedicalData.objects.create(bed=bed, heartrate=heartrate, sys_bp=sys_bp, dia_bp=dia_bp, body_temp=body_temp, oxygen_level=oxygen_level, breathing_rate=breathing_rate, timestamp=timestamp)

    # result = HistoricalMedicalData.objects.filter(bed=bed)
    # if len(result) == 0 or result.latest('timestamp').timestamp + timedelta(seconds=900) < datetime.now():
    #     pass
