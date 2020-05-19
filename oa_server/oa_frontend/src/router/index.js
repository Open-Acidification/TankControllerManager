import Vue from 'vue'
import VueRouter from 'vue-router'

// Components
import Devices from '../components/devices/Devices.vue'
import DeviceConfig from '../components/devices/DeviceConfig.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    redirect: '/devices',
  },
  {
    path: '/devices',
    name: 'Devices',
    component: Devices,
    children: [
      {
        path: ':mac/configure',
        name: 'Device Configuration',
        component: DeviceConfig,
      }
    ],
  }
]

const router = new VueRouter({
  routes
})

export default router
