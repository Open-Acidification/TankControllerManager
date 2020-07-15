<template>
  <v-content>
    <v-container fluid class="pa-0 ma-0 fill-height">
      <TimeSeriesList/>
      <router-view/>
    </v-container>
  </v-content>
</template>

<script>
import TimeSeriesList from './TimeSeriesList'

export default {
  name: 'TimeSeries',

  components: {
    TimeSeriesList,
  },
}
</script>

<style>

</style>