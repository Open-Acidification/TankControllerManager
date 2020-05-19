<template>
  <v-app>
    <Header/>
    <router-view/>
  </v-app>
</template>

<script>
import Header from './components/Header.vue';

export default {
  name: 'App',

  components: {
    Header,
  },

  data: () => ({
    //
  }),

  created() {
    this.$store.dispatch('updateDevices');

    setInterval(function () {
      this.$store.dispatch('updateDevices');
    }.bind(this), 30000); 
  }
};
</script>

<style>
  html {
    overflow-y: hidden;
  }
</style>