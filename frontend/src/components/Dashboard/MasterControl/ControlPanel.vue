<script setup>
import { ref } from 'vue'

const sensorCount = ref(2)
const savePath = ref('')

function readSensorsFromMaster() {
  console.log('Read sensors:', sensorCount.value)
}

function downloadIODDs() {
  console.log('Download to:', savePath.value)
}
</script>

<template>
  <div class="control-panel">
    <h4 class="mb-3 text-center">Master Controls</h4>

    <label class="form-label">Anzahl Sensoren am Master</label>
    <input v-model="sensorCount" type="number" min="1" class="form-control mb-3" />

    <button class="btn btn-primary w-100 mb-3" @click="readSensorsFromMaster">
      Sensoren vom Master einlesen
    </button>

    <label class="form-label">Speicherpfad für ZIP-Dateien</label>
    <input v-model="savePath" type="text" class="form-control mb-3" placeholder="/home/user/iodd-downloads" />

    <button class="btn btn-success w-100" @click="downloadIODDs">
      IODDs herunterladen
    </button>
  </div>
</template>

<style scoped>
.control-panel {
  background: #2c3e50;
  color: white;
  padding: 16px;
  border-radius: 10px;
}
</style>