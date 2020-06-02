import Vue from 'vue'
import VueRouter from 'vue-router'

// Components
import Devices from '../components/devices/Devices.vue'
import DeviceConfig from '../components/devices/DeviceConfig.vue'
import DeviceCreate from '../components/devices/DeviceCreate.vue'
import Tanks from '../components/tanks/Tanks.vue'
import TankView from '../components/tanks/TankView.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
  },
  {
    path: '/devices',
    name: 'Devices',
    component: Devices,
    children: [
      {
        path: 'add',
        name: 'NewDevice',
        component: DeviceCreate,
      },
      {
        path: ':mac',
        name: 'Device',
        component: DeviceConfig,
      }
    ],
  },
  {
    path: '/tanks',
    name: 'Tanks',
    component: Tanks,
    children: [
      {
        path: ':tankid',
        name: 'Tank',
        component: TankView,
      }
    ],
  }
]

const router = new VueRouter({
  routes
})

export default router
