import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    devices: null,
    tanks: null,
    timeSeries: {
      temp: [],
      pH: [],
    }
  },
  getters: {
    getDevice: (state) => (mac) => {
      if (state.devices) {
        return state.devices.find(device => device.mac == mac);
      }
      return undefined;
    },
    getTank: (state) => (id) => {
      if (state.tanks) {
        return state.tanks.find(tank => tank.tankid == id);
      }
      return undefined;
    },
  },
  mutations: {
    setDevices (state, devices) {
      state.devices = devices;
    },
    removeDevice (state, device) {
      var index = state.devices.indexOf(device);
      // Only remove if we actually found it
      if (index >= 0) {
        state.devices.splice(index, 1);
      }
    },
    setTanks (state, tanks) {
      state.tanks = tanks;
    },
    setTimeSeries (state, ts) {
      state.timeSeries = ts;
    },
    removeTimeSeriesTemp (state, ts) {
      var index = state.timeSeries.temp.indexOf(ts);
      // Only remove if we actually found it
      if (index >= 0) {
        state.timeSeries.temp.splice(index, 1);
      }
    },
    removeTimeSeriesPH (state, ts) {
      var index = state.timeSeries.pH.indexOf(ts);
      // Only remove if we actually found it
      if (index >= 0) {
        state.timeSeries.pH.splice(index, 1);
      }
    },
  },
  actions: {
    getDeviceWhenAvailable (context, mac) {
      return new Promise((resolve, reject) => {
        function waitForDevice(times=0) {
          var device = context.getters.getDevice(mac)
          if (device) {
            return resolve(device);
          }
          if (times > 75) {
            return reject(new Error("Could not find Device with specified MAC address "+mac));
          }
          setTimeout(function() {
            waitForDevice(times+1);
          }, 100);
        }
        waitForDevice(0);
      });
    },
    waitForTanks (context) {
      return new Promise((resolve) => {
        function waitForTanks() {
          if (context.state.tanks) return resolve();
          setTimeout(waitForTanks, 100);
        }
        waitForTanks();
      });
    },
    updateDevices (context) {
      axios
        .get('http://'+location.host+'/api/devices/')
        .then(response => (context.commit('setDevices', response.data)));
    },
    updateTanks (context) {
      axios
        .get('http://'+location.host+'/api/tanks/')
        .then(function(response) {
          var tanks = response.data;
          var sparklineRequests = [];
          // Format date and define Sparkline requests
          tanks.forEach(tank => {
            tank.last_update = new Date(tank.last_update + " UTC");
            sparklineRequests.push(axios.get('http://'+location.host+'/api/tanks/'+tank.tankid+'/sparklines'))
          });
          axios.all(sparklineRequests).then(axios.spread((...responses) => {
            for (var i = 0; i < tanks.length; i++) {
              tanks[i].sparklines = responses[i].data.sparklines;
            }
            context.commit('setTanks', tanks);
          }));
        });
    },
    updateTimeSeries (context) {
      var tempRequest = axios.get('http://'+location.host+'/api/time_series/temp/');
      var pHRequest = axios.get('http://'+location.host+'/api/time_series/pH/');
      axios.all([tempRequest, pHRequest]).then(axios.spread((...responses) => {
        context.commit('setTimeSeries', {temp: responses[0].data, pH: responses[1].data});
      }));
    },
  },
  modules: {
  }
})
