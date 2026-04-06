import paho.mqtt.client as mqtt
import json
import requests

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("RECEIVED:", data)

    # towards  NestJS
    requests.post("http://localhost:3000/sensor", json=data)

client = mqtt.Client()
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.subscribe("sensor/data")

client.loop_forever()