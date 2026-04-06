<script setup>
import { computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useSensorStore } from '../stores/sensorStore'

import LightBarrierCard from './Dashboard/LightBarrier/LightBarrierCard.vue'
import XYCard from './Dashboard/XYSensor/XYCard.vue'
import ControlPanel from './Dashboard/MasterControl/ControlPanel.vue'

const store = useSensorStore()
const { sensors } = storeToRefs(store)

onMounted(() => {
  store.fetchSensors()
})

const lightSensor = computed(() =>
  sensors.value.find(sensor => sensor.type === 'light')
)

const xySensor = computed(() =>
  sensors.value.find(sensor => sensor.type === 'xy')
)
</script>

<template>
  <div class="container py-4">
    <h1 class="text-white mb-4 text-center">Sensor Dashboard</h1>

    <div class="three-column-row">
      <div class="card-slot">
        <LightBarrierCard v-if="lightSensor" :sensor="lightSensor" />
      </div>

      <div class="card-slot">
        <XYCard v-if="xySensor" :sensor="xySensor" />
      </div>

      <div class="card-slot">
        <ControlPanel />
      </div>
    </div>
  </div>
</template>