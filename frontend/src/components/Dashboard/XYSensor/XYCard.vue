 <script setup>
import { computed } from 'vue'
import ParameterPanel from './XYPanel.vue'

const { sensor } = defineProps({ sensor: Object })

const statusClass = computed(() => {
  if (sensor.status === 'CRITICAL') return 'bg-danger'
  if (sensor.status === 'WARN') return 'bg-warning'
  return 'bg-success'
})
</script>

<template>
  <div class="col-12 col-md-6 col-lg-4">
    <div class="sensor-card text-center">
      <h4 class="mb-3">{{ sensor.title }}</h4>

      <span class="badge mt-2" :class="statusClass">
        {{ sensor.status }}
      </span>

      <ParameterPanel :sensor="sensor" />
    </div>
  </div>
</template>

<style scoped>
.sensor-card {
  background: #2c5883;
  color: white;
  padding: 12px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
