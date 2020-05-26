<template>
  <v-content v-if="tank" class="pa-4 ma-0 fill-height">
    <h3>
      View data from tank #{{ tank.tankid }}:
    </h3>

    <span class="subtitle-2">Device: {{tank.device_name}}</span>
    <v-btn :to="{path: '/devices/'+tank.device_mac}" icon>
      <v-icon>mdi-cog</v-icon>
    </v-btn>
  </v-content>
</template>

<script>

export default {
  name: 'TankView',
  data () {
    return {
      tank: null,
    }
  },
  created () {
    this.fetchTank()
  },
  watch: {
    '$route': 'fetchTank'
  },
  methods: {
    fetchTank () {
      this.tank = this.$store.getters.getTank(this.$route.params.tankid);
    }
  }
}
</script>

<style>
  html {
    overflow-y: hidden;
  }
</style>