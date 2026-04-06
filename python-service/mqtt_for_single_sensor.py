import paho.mqtt.client as mqtt

# Konfiguration
BROKER_IP = "localhost"  # Da Broker und Skript auf demselben Rechner
PORT = 1883
TOPIC = "sensor1/data"

# Callback-Funktion: Wird aufgerufen, wenn eine Nachricht eintrifft
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Empfangen auf {message.topic}: {payload}")

# Callback-Funktion: Bestätigung der Verbindung
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Erfolgreich mit Broker verbunden.")
        # Nach dem Verbinden das Topic abonnieren
        client.subscribe(TOPIC)
    else:
        print(f"Verbindungsfehler. Rückgabecode: {rc}")

# Client-Instanz erstellen
client = mqtt.Client()

# Callbacks zuweisen
client.on_connect = on_connect
client.on_message = on_message

# Verbindung aufbauen
client.connect(BROKER_IP, PORT, 60)

# Endlosschleife zum Verarbeiten der Netzwerk-Events
client.loop_forever()