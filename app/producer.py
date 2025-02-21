# app/producer.py
# from kafka import KafkaProducer  # Replace confluent_kafka with kafka
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
        producer.produce("metrics_topic", json.dumps(data))
        time.sleep(5)

if __name__ == "__main__":
    produce_metrics()