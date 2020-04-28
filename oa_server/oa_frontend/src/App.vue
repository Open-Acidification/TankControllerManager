<template>
  <v-app>
    <Header/>

    <v-content>
      <Devices/>
    </v-content>
  </v-app>
</template>

<script>
import Header from './components/Header.vue';
import Devices from './components/devices/Devices'

export default {
  name: 'App',

  components: {
    Header,
    Devices,
  },

  data: () => ({
    //
  }),
};
</script>
