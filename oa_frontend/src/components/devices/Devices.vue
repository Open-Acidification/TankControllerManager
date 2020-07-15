<template>
  <v-content>
    <v-container fluid  class="pa-0 ma-0 fill-height">
      <DeviceList/>
      <router-view/>
    </v-container>
  </v-content>
</template>

<script>
import DeviceList from './DeviceList'

export default {
  name: 'Devices',

  components: {
    DeviceList,
  },
}
</script>

<style>

</style>