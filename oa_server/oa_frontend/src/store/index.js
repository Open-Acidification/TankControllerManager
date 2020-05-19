import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    devices: null
  },
  getters: {
    getDevice: (state) => (mac) => {
      return state.devices.find(device => device.mac == mac);
    }
  },
  mutations: {
    setDevices (state, devices) {
      state.devices = devices;
    },
  },
  actions: {
    updateDevices (context) {
      console.log("Reached updateDevices()");
      axios
        .get('http://localhost:8080/api/devices/')
        .then(response => (context.commit('setDevices', response.data)));
    }
  },
  modules: {
  }
})
