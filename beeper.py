# keep this in beeper.py file
from kafka import KafkaConsumer
import json


if __name__ == '__main__':
    consumer = KafkaConsumer('EmergencyCall', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for msg in consumer:
       print(msg.value)