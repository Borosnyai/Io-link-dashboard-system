<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({ sensor: Object })

// This stores the options loaded from the API
const options = ref([])

// this stores the options loaded from API
const switchpointLogicOptions = ref([])

// This stores the currently selected value
const selectedValue = ref(0)
// This stores the currently selected SwitchpointLogic
const selectedSwitchpointLogic = ref(0)

// This function fetches the dropdown options from the API
// When the backend is ready, replace the URL with the real endpoint
async function loadOptions() {
  try {
    const response = await fetch(`http://localhost/iolink-master/sensor${props.sensor.id}/sensorPrinciple/options`)
    const data = await response.json()
    options.value = data
  } catch (error) {
    // API not ready yet → use hardcoded fallback
    console.warn('API not available, using fallback options')
    options.value = [
      { label: 'Diffuse', value: 0 },
      { label: 'Diffuse with background suppression', value: 1 },
      { label: 'Retro-reflective', value: 2 },
      { label: 'Through-beam emitter', value: 3 },
      { label: 'Through-beam receiver', value: 4 }
    ]
  }
}

async function loadSwitchpointLogic() {       // async waiting for the API
  try {
    const response = await fetch(`http://localhost/iolink-master/sensor${props.sensor.id}/switchpointLogic/options`)
    const data = await response.json()
    switchpointLogicOptions.value = data
  } catch (error) {
    switchpointLogicOptions.value = [
      { label: 'N.O.', value: 0 },
      { label: 'N.C.', value: 1 }
    ]
  }

}

// Runs automatically when the component loads
onMounted(() => {
  loadOptions()
  loadSwitchpointLogic()
})

function onValueChange() {
  console.log('New SensorPrinciple value:', selectedValue.value)
  // Later: send value to IO-Link Master via REST API
}

/*BDC1*/
// Switchpoint Logic
function onSwitchpointLogicChange() {
  console.log('Switchpoint Logic changed to:', selectedSwitchpointLogic.value)
  // Later: send value to IO-Link Master via REST API
}
</script>

<template>
  <div class="parameter-panel">
    <h2 class="text-center">Parameters</h2>

    <!-- Sensor Principle -->
    <h6 class="section-title">Sensor Principle</h6>
    <select v-model="selectedValue" @change="onValueChange">
      <option v-for="opt in options" :key="opt.value" :value="opt.value">
        {{ opt.label }} [{{ opt.value }}]
      </option>
    </select>

    <!-- BDC1 -->
    <h6 class="section-title mt-3">BDC1</h6>

    <!-- Switchpoint Logic -->
    <label class="mt-2">Switch Point Configuration BDC1:Switchpoint Logic</label>
    <select v-model="selectedSwitchpointLogic" @change="onSwitchpointLogicChange">
      <option v-for="opt in switchpointLogicOptions" :key="opt.value" :value="opt.value">
        {{ opt.label }} [{{ opt.value }}]
      </option>
    </select>

  </div>
</template>

<style scoped>

.parameter-panel {
  background: #1e3a5f;
  color: white;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.9rem;
  opacity: 0.8;
}

select {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  background: #668bb9;
  color: white;
  border: 1px solid #2c3e58;
}

.sensor-card h4 {
  font-size: 20px;
  font-weight: 500;
}
</style>