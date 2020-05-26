<template>
  <v-content>
    <v-container fluid  class="pa-0 ma-0 fill-height">
      <TankList/>
      <router-view/>
    </v-container>
  </v-content>
</template>

<script>
import TankList from './TankList'

export default {
  name: 'Tanks',

  components: {
    TankList,
  },
}
</script>

<style>

</style>