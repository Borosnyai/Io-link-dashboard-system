<script setup>
import { computed, ref } from 'vue'
import ParameterPanel from './LightBarrierPanel.vue'

const { sensor } = defineProps({ sensor: Object })


const statusClass = computed(() => {
  if (sensor.status === 'CRITICAL') return 'bg-danger'
  if (sensor.status === 'WARN') return 'bg-warning'
  return 'bg-success'
})

</script>

<template>
  <div class="col-12 col-md-6">
    <div class="sensor-card text-center">

      <!-- TITLE -->
      <h4 class="mb-3">{{ sensor.title }}</h4>

      <!-- STATUS -->
      <span class="badge mt-2 mb-3" :class="statusClass">
        {{ sensor.status }}
      </span>

      <!-- PARAMETERS-->
      <div class="parameter-section">

        <h5>Parameters</h5>

        <label class="form-label">Sensor Principle</label>
        <select class="form-select mb-3">
          <option>Diffuse [0]</option>
          <option>Diffuse with background suppression [1]</option>
          <option>Retro-reflective [2]</option>
          <option>Through-beam emitter [3]</option>
          <option>Through-beam receiver [4]</option>
        </select>

        <!-- BDC1 GROUP -->
        <div class="bdc-block">

          <h6 class="mb-3">BDC1</h6>

          <!-- SP1 -->
          <label class="form-label">Setpoint values BDC1:SP1</label>
          <input type="number" class="form-control mb-2" min="0" max="4095" />

          <!-- SP2 -->
          <label class="form-label">Setpoint values BDC1:SP2</label>
          <input type="number" class="form-control mb-2" min="0" max="4095" />

          <!-- Logic -->
          <label class="form-label">Switchpoint Logic</label>
          <select class="form-select mb-2">
            <option>N.O. [0]</option>
            <option>N.C. [1]</option>
          </select>

          <!-- Mode -->
          <label class="form-label">Switchpoint Mode</label>
          <select class="form-select mb-2">
            <option>Single Point Mode [1]</option>
            <option>Window Mode [2]</option>
            <option>Two Point Mode [3]</option>
          </select>

          <!-- Hysteresis -->
          <label class="form-label">Switchpoint Hysteresis</label>
          <input type="number" class="form-control" min="0" max="10" />

        </div>

      </div>

    </div>
  </div>
</template>

<style scoped>
.sensor-card {
  background: #2c3e50;
  color: white;
  padding: 12px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}


.parameter-section {
  background: #2b4a6f;
  
  padding: 20px;
  border-radius: 10px;
  margin-top: 10px;
}

/*Title*/
.parameter-section h5 {
  font-size: 22px;
  margin-bottom: 15px;
  text-align: center;
}

/* inputs */
.form-select {
  background-color: #1c196a;
  color: rgb(240, 240, 240);
  border: none;
}

.form-label {
  color: #dcdcdc;
}
</style>