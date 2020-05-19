<template>
  <v-content class="pa-2 ma-2 fill-height">
    <div v-if="device != null">
      {{ device.mac }}
    </div>
  </v-content>
</template>

<script>

export default {
  name: 'DeviceConfig',
  data () {
    return {
      device: null,
    }
  },
  created () {
    this.fetchDevice()
  },
  watch: {
    '$route': 'fetchDevice'
  },
  methods: {
    fetchDevice () {
      this.device = this.$store.getters.getDevice(this.$route.params.mac);
    }
  }
}
</script>

<style>

</style>