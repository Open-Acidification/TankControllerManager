import Vue from 'vue'
import VueRouter from 'vue-router'

// Components
import Devices from '../components/devices/Devices.vue'
import DeviceConfig from '../components/devices/DeviceConfig.vue'
import DeviceCreate from '../components/devices/DeviceCreate.vue'
import Tanks from '../components/tanks/Tanks.vue'
import TankView from '../components/tanks/TankView.vue'
import TimeSeries from '../components/time_series/TimeSeries.vue'
import TimeSeriesCreateTemp from '../components/time_series/TimeSeriesCreateTemp.vue'
import TimeSeriesCreatePH from '../components/time_series/TimeSeriesCreatePH.vue'
import TankChart from '../components/tanks/TankChart.vue'

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
        name: 'New Device',
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
        children: [
          {
            path: 'graph',
            name: 'Chart',
            component: TankChart,
          }
        ],
      }
    ],
  },
  {
    path: '/time_series',
    name: 'Time Series',
    component: TimeSeries,
    children: [
      {
        path: 'temp/create',
        name: 'New Temp Time Series',
        component: TimeSeriesCreateTemp,
      },
      {
        path: 'ph/create',
        name: 'New pH Time Series',
        component: TimeSeriesCreatePH,
      }
    ],
  }
]

const router = new VueRouter({
  routes
})

export default router
