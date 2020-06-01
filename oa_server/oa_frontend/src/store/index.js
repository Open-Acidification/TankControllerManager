import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    devices: null,
    tanks: null
  },
  getters: {
    getDevice: (state) => (mac) => {
      return state.devices.find(device => device.mac == mac);
    },
    getTank: (state) => (id) => {
      return state.tanks.find(tank => tank.tankid == id);
    }
  },
  mutations: {
    setDevices (state, devices) {
      state.devices = devices;
    },
    setTanks (state, tanks) {
      state.tanks = tanks;
    }
  },
  actions: {
    updateDevices (context) {
      axios
        .get('http://localhost:8080/api/devices/')
        .then(response => (context.commit('setDevices', response.data)));
    },
    updateTanks (context) {
      axios
        .get('http://localhost:8080/api/tanks/')
        .then(function(response) {
          var tanks = response.data;
          var sparklineRequests = [];
          // Format date and define Sparkline requests
          tanks.forEach(tank => {
            tank.last_update = new Date(tank.last_update + " UTC");
            sparklineRequests.push(axios.get('http://localhost:8080/api/tanks/'+tank.tankid+'/sparklines'))
          });
          axios.all(sparklineRequests).then(axios.spread((...responses) => {
            for (var i = 0; i < tanks.length; i++) {
              tanks[i].sparklines = responses[i].data.sparklines;
            }
            context.commit('setTanks', tanks);
          }));
        });
    }
  },
  modules: {
  }
})
