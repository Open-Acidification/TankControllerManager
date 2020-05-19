<template>
  <v-content>
    <v-container fluid  class="pa-0 ma-0 fill-height">
      <DeviceList :devices="devices"/>
      <router-view/>
    </v-container>
  </v-content>
</template>

<script>
import DeviceList from './DeviceList'
// import DeviceDetails from './components/devices/DeviceDetails'

export default {
  name: 'Devices',

  components: {
    DeviceList,
  },

  data() {
    return {
      devices: null
    }
  },
  mounted() {
    this.axios
      .get('http://localhost:8080/api/devices/')
      .then(response => (this.devices = response.data));
  }
}
</script>

<style>

</style>