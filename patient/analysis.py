from healthcare_workers.models import *
from kafka import KafkaProducer
import json


def doctor_nurse(bed_id):
    bed_id = int(bed_id)
    doctorID = Bed.objects.get(bedID=bed_id).doctor_fk.doctorID
    nurseID = Bed.objects.get(bedID=bed_id).nurse_fk.nurseID

    return doctorID, nurseID


def send_emergency_data(bed_id, score):
    print('function called')
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                             api_version=(0, 10, 1))
    doctor_id, nurse_id = doctor_nurse(bed_id)
    msg = f'Patient at bed number: {bed_id} needs immediate attention.' \
          f'Level of Seriousness: {score}/5 . Targeted Doctor ID : {doctor_id}, Targeted Nurse ID: {nurse_id}'
    producer.send("EmergencyCall", msg)


def score_calculator(heartbeat, sys_bp, dia_bp, body_temp, oxygen_level, breathing_rate):
    score = 0
    if heartbeat > 93.0 or heartbeat < 55.0:
        score = score + 1
    if sys_bp > 140.0 :
        score = score + 1
    if dia_bp < 65.0 :
        score = score + 1
    if body_temp < 97.0 or body_temp > 103.0:
        score = score + 1
    if oxygen_level < 0.88:
        score = score + 1
    if breathing_rate > 17.0 or breathing_rate < 13.0:
        score = score + 1
    return score


def condition_analyst(bed_id, heartbeat, sys_bp, dia_bp, body_temp, oxygen_level, breathing_rate):
    score = score_calculator(heartbeat, sys_bp, dia_bp, body_temp, oxygen_level, breathing_rate)

    if score >= 3:
        last_five = RecentMedicalData.objects.all().filter(bed_id=bed_id).order_by('-id')[:5]
        list_hrate = []
        list_sys_bp = []
        list_dia_bp = []
        list_body_temp = []
        list_olevel = []
        list_brate = []
        for data in last_five:
            list_hrate.append(data.heartrate)
            list_brate.append(data.breathing_rate)
            list_olevel.append(data.oxygen_level)
            list_sys_bp.append(data.sys_bp)
            list_dia_bp.append(data.dia_bp)
            list_body_temp.append(data.body_temp)
        avg_hrate = sum(list_hrate)/5
        avg_sys_bp = sum(list_sys_bp)/5
        avg_dia_bp = sum(list_dia_bp)/5
        avg_body_temp = sum(list_body_temp)/5
        avg_oxy_level = sum(list_olevel)/5
        avg_brate = sum(list_brate)/5
        score_avg = score_calculator(avg_hrate, avg_sys_bp, avg_dia_bp, avg_body_temp, avg_oxy_level, avg_brate)
        print(score_avg)
        if score_avg >= 3.5:
            total_score = (score_avg + score)/2
            send_emergency_data(bed_id, total_score)
