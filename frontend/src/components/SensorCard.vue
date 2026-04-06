Cseréld le a teljes `SensorCard.vue` fájlt erre:

```vue
<script setup>
import { computed } from 'vue'

const props = defineProps({
  sensor: Object
})

const statusClass = computed(() => {
  if (props.sensor.status === 'CRITICAL') return 'bg-danger'
  if (props.sensor.status === 'WARN') return 'bg-warning'
  return 'bg-success'
})
</script>

<template>
  <div class="sensor-card">
    <h3>{{ sensor.title }}</h3>

    <div class="sensor-value">{{ sensor.value }} <span class="sensor-unit">{{ sensor.unit }}</span></div>

    <div v-if="sensor.details" class="sensor-details">
      <div v-for="(val, key) in sensor.details" :key="key" class="detail-item">
        <span>{{ key }}:</span>
        <span>{{ val }}</span>
      </div>
    </div>

    <span class="status-badge" :class="statusClass.replace('bg-', '')">
      {{ sensor.status }}
    </span>
  </div>
</template>

<style scoped>
.sensor-card {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  min-height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.sensor-card h3 {
  font-size: 1rem;
  font-weight: 500;
  color: #94a3b8;
  text-align: center;
  margin-bottom: 1rem;
}

.sensor-value {
  font-size: 3rem;
  font-weight: 700;
  text-align: center;
  margin: 1rem 0;
  color: #fff;
}

.sensor-unit {
  font-size: 1.25rem;
  color: #94a3b8;
  margin-left: 0.5rem;
}

.sensor-details {
  margin: 1rem 0;
  flex-grow: 1;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  font-size: 0.875rem;
  color: #94a3b8;
}

.status-badge {
  display: block;
  padding: 0.25rem 1rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  margin: 0 auto;
  text-align: center;
  width: fit-content;
}

.status-badge.success {
  background: #22c55e;
  color: #000;
}

.status-badge.warning {
  background: #eab308;
  color: #000;
}

.status-badge.danger {
  background: #ef4444;
  color: #fff;
}
</style>