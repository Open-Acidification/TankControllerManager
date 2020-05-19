<template>
  <v-content class="pa-2 ma-2 fill-height">
    <v-progress-circular v-if="loading"
      indeterminate
      color="primary"
    />
    <div v-else>

    </div>
  </v-content>
</template>

<script>

export default {
  name: 'DeviceConfig',
  data () {
    return {
      loading: false,
      device: null,
      error: null
    }
  },
  created () {
    // fetch the data when the view is created and the data is
    // already being observed
    this.fetchData()
  },
  watch: {
    // call again the method if the route changes
    '$route': 'fetchData'
  },
  methods: {
    createDevice () {
      this.error = this.device = null
      this.loading = true
      this.axios
      .get('http://localhost:8080/api/devices/'+this.$route.params.mac)
      .then(response => {
        this.device = response.data;
        this.loading = false;
      }).catch(error => (this.error = error));
    }
  }
}
</script>

<style>

</style>