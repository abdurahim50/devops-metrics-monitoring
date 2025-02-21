# app/producer.py
from confluent_kafka import Producer
import json
import psutil
import time
import os

conf = {'bootstrap.servers': os.getenv("KAFKA_BROKER")}
producer = Producer(conf)

def produce_metrics():
    while True:
        data = {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "timestamp": time.time()
        }
        producer.produce("metrics", json.dumps(data))
        time.sleep(5)