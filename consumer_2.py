# File: consumer_with_model.py

import json
import joblib
import numpy as np
import pandas as pd
from confluent_kafka import Consumer, KafkaError

# === Load the pre-trained regression model using joblib ===
try:
    model = joblib.load("iris_model.pkl")
    print("Model loaded successfully.\n")
except Exception as e:
    print(f"Failed to load model: {e}")
    exit()

# === Kafka consumer configuration ===
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'iris_consumer_group',
    'auto.offset.reset': 'earliest'  # Start from beginning if new consumer group
}

# Create Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
topic = "iris_clean_topic"
consumer.subscribe([topic])

print(f"Listening to topic '{topic}'... Press Ctrl+C to stop.\n")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Kafka Error: {msg.error()}")
        else:
            # === Parse the message ===
            data_json = msg.value().decode('utf-8')
            data_dict = json.loads(data_json)

            print("Received message:")
            print(data_dict)

            try:
                # === Create DataFrame for prediction ===
                new_data = pd.DataFrame([{
                    'sepal_length': float(data_dict["sepal_length"]),
                    'sepal_width': float(data_dict["sepal_width"]),
                    'petal_length': float(data_dict["petal_length"]),
                    'petal_width': float(data_dict["petal_width"])
                }])

                # Make prediction using the loaded model
                prediction = model.predict(new_data)[0]

                print(f"Predicted value: {prediction}\n")
            except Exception as e:
                print(f"Error during prediction: {e}\n")

except KeyboardInterrupt:
    print("\n Stopping consumer...")

finally:
    consumer.close()
