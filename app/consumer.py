# app/consumer.py
from confluent_kafka import Consumer
import json
import os

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BROKER"),
    'group.id': 'metrics_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(["metrics_topic"])

def consume_metrics():
    while True:
        msg = consumer.poll(1.0)
        if msg:
            print(f"Received: {json.loads(msg.value())}")

if __name__ == "__main__":
    consume_metrics()
    