import { defineStore } from 'pinia';

export const useSensorStore = defineStore('sensor', {
  state: () => ({
    sensors: []
  }),

  actions: {
    updateSensors(sensors) {
      this.sensors = sensors
    },

    updateSensor(sensor) {
      const index = this.sensors.findIndex(s => s.id === sensor.id)

      if (index !== -1) {
        this.sensors[index] = sensor
      } else {
        this.sensors.push(sensor)
      }
    },
    async fetchSensors() {
      const response = await fetch('http://localhost:3000/sensor/data')
      const data = await response.json()

      this.updateSensors(data.sensors)
    }
  }
})