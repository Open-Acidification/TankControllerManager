<template>
  <v-app-bar app color="primary" dark>
    <router-link to="/">
      <v-img
        alt="Open Acidification Logo"
        class="shrink mr-2"
        contain
        src="../assets/logo_inverted.png"
        transition="scale-transition"
        width="40"
      />
    </router-link>
    <v-tabs fixed-tabs>
      <v-tab to="/tanks">Tanks</v-tab>
      <v-tab to="/devices">Devices</v-tab>
      <v-tab to="/time_series">Time Series</v-tab>
    </v-tabs>
    <v-spacer/>
  </v-app-bar>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style>

</style>