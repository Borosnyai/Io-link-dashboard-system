import { getMockSensors } from './mockDataServices';
import { startMQTT } from './mqttDataService';

const useMockData = true

export function initDataService(store) {
  if (useMockData) {
    store.updateSensors(getMockSensors())

    setInterval(() => {
      store.updateSensors(getMockSensors())
    }, 2000)
  } else {
    startMQTT((sensor) => {
      store.updateSensor(sensor)
    })
  }
}