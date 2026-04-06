# mqtt_test_publisher.py
import json
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "sensors/light-barrier/data"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="python-test-publisher")
client.connect(BROKER_HOST, BROKER_PORT, 60)

while True:
    payload = {
        "sensorId": "light-barrier-1",
        "value": 1,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Published:", payload)
    time.sleep(2)