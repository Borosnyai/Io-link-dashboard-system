import './mockBackend'
import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from '../App.vue'
import DashboardView from '../views/DashboardView.vue'
import SensorListView from '../views/SensorListView.vue'
import SensorView from '../views/SensorView.vue'
import '@coreui/coreui/dist/css/coreui.min.css'

// Hash routing, so the single HTML file also works when opened from disk.
const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: DashboardView },
    { path: '/live/sensors', component: SensorListView },
    { path: '/demo/sensors', component: SensorListView },
    { path: '/live/sensor/:port', component: SensorView },
    { path: '/demo/sensor/:port', component: SensorView },
  ],
})

createApp(App).use(router).mount('#app')

const badge = document.createElement('div')
badge.textContent = 'Standalone demo · simulated sensor data'
badge.style.cssText = 'position:fixed;right:12px;bottom:10px;z-index:99999;padding:4px 10px;' +
  'border-radius:999px;font:600 11px system-ui,sans-serif;letter-spacing:.03em;' +
  'background:rgba(15,23,42,.88);color:#e2e8f0;pointer-events:none'
document.body.appendChild(badge)
