# File: topic.py

import json
from confluent_kafka import Producer
from Rest_API import get_cleaned_sample_data

# Kafka configuration
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

topic = "iris_clean_topic"

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Get cleaned data
cleaned_data = get_cleaned_sample_data()

# Publish to Kafka
for record in cleaned_data:
    producer.produce(
        topic=topic,
        value=json.dumps(record),
        callback=delivery_report
    )

producer.flush()
