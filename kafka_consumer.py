# File: consumer.py

from confluent_kafka import Consumer, KafkaError

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'iris_consumer_group',
    'auto.offset.reset': 'earliest'  # Consume from the beginning
}

# Create Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
topic = "iris_clean_topic"
consumer.subscribe([topic])

print(f"Listening to topic '{topic}'... Press Ctrl+C to stop.\n")

try:
    while True:
        msg = consumer.poll(1.0)  # Wait for 1 second
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue  # End of partition event
            else:
                print(f"Error: {msg.error()}")
        else:
            print("Received message:")
            print(msg.value().decode('utf-8'))  # Decode JSON string

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:
    # Clean up
    consumer.close()
