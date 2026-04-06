<script setup>
const { sensor } = defineProps({ sensor: Object })
</script>

<template>
  <div class="parameter-panel">
    <h2 class="text-center">Parameters</h2>
    <!--Here come the parameters!-->
  </div>
</template>

<style scoped>
.parameter-section {
  background: #2b4a6f;
  padding: 20px;
  border-radius: 10px;
  margin-top: 10px;
}

.sensor-card h4 {
  font-size: 20px;
  font-weight: 500;
}
</style> 
