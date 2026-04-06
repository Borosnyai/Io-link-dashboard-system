// This file will handle real MQTT communication later
// For now it is only a placeholder (no broker, no connection)

export function startMQTT(onMessage) {
  console.log('MQTT service started (placeholder)')

  // Later this is where we will:
  // - connect to Mosquitto broker
  // - subscribe to MQTT topics
  // - receive messages
  // - parse JSON payloads
  // - call onMessage(sensorData)
}
