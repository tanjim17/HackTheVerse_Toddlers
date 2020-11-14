from kafka import KafkaProducer
import json
import random
import time
from itertools import islice


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=json_serializer,
                         api_version=(0, 10, 1))


def fluctuate(cond):
    controller = random.random()
    if controller < 0.25 and cond == 0:
        cond = 1
    elif controller < 0.4 and cond == 1:
        cond = cond + random.choice([-1, 1])
    elif controller < 0.6 and cond == 2:
        cond = cond + random.choice([-1, 1])
    elif controller < 0.80 and cond == 3:
        cond = cond + random.choice([0, (random.random() >= 0.80)*-1])
    return cond


normal_condition = {
    'hbeat': ((60,90), (60, 90)),
    'bpres': ((78, 82), (118, 122)),
    'body_temp': (97, 99),
    'oxygenL': (0.95, 0.98),
    'brRate': (12, 16)
}

moderate_condition = {
    'hbeat': ((55, 60), (90, 95)),
    'bpres': ((70, 80), (120, 135)),
    'body_temp': (99, 101),
    'oxygenL': (0.90, 0.95),
    'brRate': (14, 17)
}

critical_condition = {
    'hbeat': ((50, 55), (95, 100)),
    'bpres': ((65, 70), (130, 145)),
    'body_temp': (101, 103),
    'oxygenL': (0.85, 0.90),
    'brRate': (14, 17)
}

very_critical_condition = {
    'hbeat': ((40, 50), (95, 105)),
    'bpres': ((55, 60), (140, 175)),
    'body_temp': (101, 105),
    'oxygenL': (0.83, 0.87),
    'brRate': (16, 20)
}


conditions = [normal_condition, moderate_condition,
              critical_condition, very_critical_condition]


def get_sensor_data(cond, bed_id):
    cond = fluctuate(cond)
    state_dict = conditions[cond]
    heart_beat_l_range, heart_beat_h_range = state_dict['hbeat']
    dias_pres_range, sys_pres_range = state_dict['bpres']
    body_temp_range = state_dict['body_temp']
    oxygen_level_range = state_dict['oxygenL']
    breathing_rate_range = state_dict['brRate']

    heartbeat = str(random.choice([random.randint(heart_beat_l_range[0], heart_beat_l_range[1]),
                                  random.randint(heart_beat_h_range[0], heart_beat_h_range[1])])) 
    sys_blood_pressure = str(random.randint(sys_pres_range[0], sys_pres_range[1])) 
    dias_blood_pressure = str(random.randint(dias_pres_range[0], dias_pres_range[1])) 

    body_temp = str(round(random.uniform(body_temp_range[0], body_temp_range[1]), 2)) 
    oxygen_level = str(round(random.uniform(oxygen_level_range[0], oxygen_level_range[1]), 3)) 
    breathing_rate = str(random.randint(breathing_rate_range[0], breathing_rate_range[1])) 

    return {
        'bed_id': bed_id,
        'heartbeat': heartbeat,
        'sys_blood_pressure': sys_blood_pressure,
        'dias_blood_pressure': dias_blood_pressure,
        'body_temp': body_temp,
        'oxygen_level': oxygen_level,
        'breathing_rate': breathing_rate,
    }, cond


if __name__ == '__main__':
    bedlist = []
    for i in range(0, 90):
        bedlist.append(i)
    random.shuffle(bedlist)
    length_to_split = [30, 40, 15, 5]
    Inputt = iter(bedlist)
    partition_list = [list(islice(Inputt, elem)) for elem in length_to_split]
    init_data_list = [0]*90
    normal = partition_list[0]
    moderate = partition_list[1]
    critical = partition_list[2]
    very_critical = partition_list[3]

    for i in moderate:
        init_data_list[i] = 1
    for i in critical:
        init_data_list[i] = 2
    for i in very_critical:
        init_data_list[i] = 3
    serial = range(0, 90)

    while 1 == 1:

        for i in random.sample(range(0, 90), 90):
            condition = init_data_list[i]
            sensor_data, condition = get_sensor_data(condition, i)
            init_data_list[i] = condition
            #print(sensor_data)
            producer.send("SensorData", sensor_data)
            time.sleep(0.3)
        #time.sleep(0.3)