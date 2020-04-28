<template>
  <v-app-bar app color="primary" dark>
    <div class="d-flex align-center">
      <v-img
        alt="Open Acidification Logo"
        class="shrink mr-2"
        contain
        src="../assets/logo_inverted.png"
        transition="scale-transition"
        width="40"
      />

      <h1 class="display-1 condensed-light" contain min-width="100" width="100">CONTROL CENTER</h1>
    </div>
  </v-app-bar>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style>

</style>