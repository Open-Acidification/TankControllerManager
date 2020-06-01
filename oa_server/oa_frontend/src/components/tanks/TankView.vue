<template>
  <v-content class="pa-4 ma-0 fill-height">
    <div v-if="tank">
      <h3>
        View data from tank #{{ tank.tankid }}:
      </h3>

      <span class="subtitle-2">Device: {{tank.device_name}}</span>
      <v-btn :to="{path: '/devices/'+tank.device_mac}" icon>
        <v-icon>mdi-cog</v-icon>
      </v-btn>
    </div>
    <CenteredProgress v-else/>
  </v-content>
</template>

<script>
import CenteredProgress from '../CenteredProgress.vue';

export default {
  name: 'TankView',

  components: {
    CenteredProgress,
  },

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
      this.$store.dispatch('waitForTanks').then(() => {
        this.tank = this.$store.getters.getTank(this.$route.params.tankid);
      });
    }
  }
}
</script>

<style>
  html {
    overflow-y: hidden;
  }
</style>