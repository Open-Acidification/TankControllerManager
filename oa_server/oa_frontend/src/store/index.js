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
    },
    setSparklines (state, sparklines) {
      var tank = state.tanks.find(tank => tank.tankid == sparklines.tankid);
      tank.sparklines = sparklines.sparklines;
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
          context.commit('setTanks', response.data);
          // Add the sparklines to each tank
          context.state.tanks.forEach(tank => {
            tank.last_update = new Date(tank.last_update + " UTC");
            axios
              .get('http://localhost:8080/api/tanks/'+tank.tankid+'/sparklines')
              .then(response => (tank.sparklines = response.data.sparklines));
          });
        });
    }
  },
  modules: {
  }
})
