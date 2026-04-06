<script setup>
import { onMounted } from 'vue'
import { useSensorStore } from './stores/sensorStore'
import { initDataService } from './services/dataService'
import Layout from './components/Layout.vue'

const store = useSensorStore()

onMounted(() => {
  initDataService(store)
})
</script>

<template>
  <Layout />
</template>